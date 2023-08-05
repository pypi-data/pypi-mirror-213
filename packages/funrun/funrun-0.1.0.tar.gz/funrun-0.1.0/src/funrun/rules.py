"""Configuration rules."""
from copy import deepcopy
from dataclasses import dataclass
from typing import Optional


@dataclass
class DependencyRuleConfiguration:
    """Configuration for a dependency rule."""

    use_cached: Optional[bool] = None
    """If set, use previously generated products where possible rather than re-generating them."""

    use_md5: Optional[bool] = None
    """If set, use MD5 hash changes to determine if a product needs to be regenerated."""

    timeout: Optional[float] = None
    """If set, then any product older than this is considered stale."""

    def combine(self, other: Optional["DependencyRuleConfiguration"]):
        """
        Combine this configuration with another.

        The non-None values in the other take priority.

        :param other:
        :return:
        """
        combined = deepcopy(self)
        if other is None:
            return combined
        for k in ["use_cached", "use_md5", "timeout"]:
            v = getattr(other, k)
            if v is not None:
                setattr(combined, k, v)
        return combined
