"""Main runner."""
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional, Tuple, Union

from funrun.engine import Engine, ShellEngine
from funrun.product import Product, Workspace
from funrun.rules import DependencyRuleConfiguration

MAKE_OUTPUT = Union[str, Product, List[Product]]


@dataclass
class Activity:
    """Activity that was performed."""

    generated: List[Product] = None
    used: List[Product] = None
    started_at_time: float = None
    ended_at_time: float = None
    command: str = None


@dataclass
class History:
    """History of activities."""

    activities: List[Activity]


@dataclass
class Runner:
    """Engine for running commands."""

    engine: Engine = None
    activities: List[Activity] = None
    use_md5: Optional[bool] = None
    use_cached: Optional[bool] = None
    configuration: Optional[DependencyRuleConfiguration] = None
    workspace: Optional[Workspace] = None

    def __post_init__(self):
        """Initialize the runner."""
        if self.activities is None:
            self.activities = []
        if self.engine is None:
            self.engine = ShellEngine()
        if self.configuration is None:
            self.configuration = DependencyRuleConfiguration()
        if self.use_md5 is not None:
            self.configuration.use_md5 = self.use_md5
        if self.use_cached is not None:
            self.configuration.use_cached = self.use_cached

    def make(
        self,
        product: Union[Product, str, Tuple[Callable, Product], list],
        depth=0,
        parent=None,
        configuration: DependencyRuleConfiguration = None,
        verbose: bool = False,
        **kwargs,
    ) -> MAKE_OUTPUT:
        """
        Materialize a product by making its dependencies and then running its command.

        :param product:
        :param depth:
        :param parent:
        :param configuration:
        :param verbose:
        :param kwargs:
        :return:
        :raises: NotImplementedError
        """
        if not configuration:
            configuration = DependencyRuleConfiguration(**kwargs)
        configuration = self.configuration.combine(configuration)
        if not self.workspace:
            self.workspace = Workspace(directory=Path.cwd() / ".funrun")
        use_cached = configuration.use_cached
        use_md5 = configuration.use_md5
        kwargs = {"configuration": configuration}

        def info(msg):
            if verbose:
                indent = "    " * depth
                print(f":: {indent}{msg}")

        if isinstance(product, tuple) and callable(product[0]):
            f, dependencies = product[0], product[1:]
            for d in dependencies:
                self.make(d, depth + 1, product, **kwargs)
            return self.make(f(), depth + 1, **kwargs)
        if isinstance(product, list):
            return [self.make(p, depth + 1, product, **kwargs) for p in product]
        if not isinstance(product, Product):
            return product
        dependencies = self._get_dependencies(product)
        info(f"Checking Dependencies for command: {product.generated_using}")
        # TODO: if a single dependency and it is pipable, pipe it
        for d in dependencies.values():
            self.make(d, depth + 1, product, **kwargs)
        command = product.generated_using
        if isinstance(command, Callable):
            command = command()
        params = {k: getattr(product, k) for k in dir(product) if not product._internal_key(k)}
        if not product.output:
            product.set_output(self.workspace)
        else:
            product.output = product.output.format(**params)
        params["output"] = product.output
        if command is None:
            info(f"NO ACTION for {product.__repr__()}")
        else:
            if use_cached and self._exists_and_not_stale(
                product, dependencies=list(dependencies.values()), use_md5=use_md5, info=info
            ):
                info(f"Product is up to date: {product}")
            else:
                if product.piped is not None:
                    if not product.piped:
                        command += " > {output}"
                    else:
                        raise NotImplementedError("Piped commands not yet implemented")
                else:
                    if "{output}" not in command:
                        command += " > {output}"
                command_inst = command.format(**params)
                self.engine.execute(command_inst, info=info)
                product.materialized = True
                used = [d for d in dependencies.values() if isinstance(d, Product)]
                activity = Activity(command=command_inst, generated=[product], used=used)
                self.add_activity(activity)
        if use_md5:
            self._save_md5_dependencies(product, dependencies=list(dependencies.values()))
        if depth == 0:
            info(f"COMPLETE: out={product.output}")
        product.built = True
        product._runner = self
        return product

    def add_activity(self, activity: Activity):
        """Add an activity to the history."""
        self.activities.append(activity)

    def _get_dependencies(self, product):
        d = {}
        if not isinstance(product, Product):
            return d
        for k in dir(product):
            if product._internal_key(k):
                continue
            # currently assumes all attributes are potentially dependencies
            v = getattr(product, k)
            if isinstance(v, Product) or k == "input":
                if v is not None:
                    d[k] = v
        return d

    def _md5_dependency_cache(self, product: Product) -> str:
        return f"{str(product)}.__dependencies__"

    def _md5s_of_dependencies(self, product: Product) -> Optional[dict]:
        path = self._md5_dependency_cache(product)
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        else:
            return {}

    def _save_md5_dependencies(self, product: Product, dependencies: List = None):
        path = self._md5_dependency_cache(product)
        d_map = {}
        for d in dependencies:
            if isinstance(d, Product):
                dependency_md5 = d.md5
                d_map[d.output] = dependency_md5
        with open(path, "w") as f:
            json.dump(d_map, f)

    def _exists_and_not_stale(
        self, product: Product, dependencies: List = None, use_md5=None, info: Callable = None
    ):
        if info is None:
            info = lambda _x: None
        if (not product.materialized) and (not product.exists()):
            info(f">>> NOT MATERIALIZED: {product}")
            return False
        elif use_md5:
            t = product.timestamp_fn()
            info(f"*** T={t}: {product.output} // {product}")
            d_map = self._md5s_of_dependencies(product)
            for d in dependencies:
                if isinstance(d, Product):
                    dependency_md5 = d.md5
                    last_md5 = d_map.get(d.output, None)
                    if dependency_md5 != last_md5:
                        info(f"*** MD5 MISMATCH: {d.output} // {d}")
                        return False
            return True
        else:
            product_timestamp = product.timestamp_fn()
            for d in dependencies:
                dpath = Path(str(d))
                if dpath.exists():
                    dependency_timestamp = os.path.getmtime(dpath)
                    # info(
                    #    f"*** ?stale= {dependency_timestamp > product_timestamp} // COMPARE {dependency_timestamp}>{product_timestamp} for {dpath} > {product}"
                    # )
                    if dependency_timestamp > product_timestamp:
                        return False
            return True
