from typing import Any


def kwarg_opts(**kwargs) -> str:
    def _opt(
        k: str,
    ) -> str:
        if len(k) == 1:
            return f"-{k}"
        else:
            return f"--{k}"

    def _v(v: Any) -> str:
        if isinstance(v, bool):
            return ""
        else:
            return f"{v}"

    return " ".join([f"{_opt(k)} {_v(v)}" for k, v in kwargs.items()])
