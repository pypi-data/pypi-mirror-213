import hashlib
import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, ClassVar, List, Union

ProductOrPath = Union["Product", Path, str]


logger = logging.getLogger(__name__)


@dataclass
class Workspace:
    directory: Path = None


@dataclass
class PathExpression:
    expression: str

    def __str__(self):
        return self.expression


@dataclass
class Product:
    """
    Base class for data products.

    Data products are evaluated in a lazy fashion.
    """

    generated_using: Union[str, Callable] = None
    """Template to be evaluated to a shell command to generate the product"""

    input: Any = None
    name: str = None
    output: str = None
    piped: bool = None
    pipable: bool = None
    materialized: bool = None
    built: bool = None
    _runner: "Runner" = None

    uses_md5: bool = None

    def __str__(self):
        if self.output is None:
            return super().__str__()
        else:
            return self.output

    def _ensure_built(self):
        if not self.built:
            from funrun.runner import Runner

            runner = Runner()
            runner.make(self)

    def _internal_key(self, k: str) -> bool:
        return k in ["md5", "timestamp"]

    def all_params(self):
        return {k: getattr(self, k) for k in vars(self) if not self._internal_key(k)}

    def match(self, pattern: str):
        return re.match(pattern, self.content())

    def set_output(self, workspace: Workspace = None):
        # if self.output is None:
        #    self.output = self.name
        if self.output is None:
            wsdir = workspace.directory if workspace else Path(".")
            wsdir.mkdir(parents=True, exist_ok=True)
            p = "_".join(
                [
                    f"{k}={v}"
                    for k, v in self.all_params().items()
                    if not k.startswith("_") and k != "generated_using"
                ]
            )
            name = hashlib.md5(p.encode("utf-8")).hexdigest()
            self.output = str(wsdir / f"{self.__class__.__name__}.{name}")

    def make(self, runner: "Runner"):
        """
        generates the product using a runner
        """
        obj = runner.make(self)
        return obj

    def dump(self, path: str) -> None:
        """
        dumps the product to a file
        """
        self._ensure_built()
        Path(path).write_text(self.content())

    def content(self) -> str:
        self._ensure_built()
        return Path(self.output).read_text()

    def content_preview(self, n=200) -> str:
        return self.content()[0:n]

    def lines(self) -> List[str]:
        return self.content().split("\n")

    @property
    def md5(self) -> str:
        content = str(self.content())
        return hashlib.md5(content.encode("utf-8")).hexdigest()

    def path(self) -> Path:
        return Path(self.output)

    @property
    def timestamp(self) -> float:
        return os.path.getmtime(self.output)

    def timestamp_fn(self) -> float:
        return os.path.getmtime(self.output)

    def exists(self) -> int:
        return self.path().exists()

    def commands_executed(self) -> List[str]:
        return [activity.command for activity in self._runner.activities]
