from typing import Callable, TypeAlias

from .generic import T

Predicate: TypeAlias = Callable[[T], bool]
