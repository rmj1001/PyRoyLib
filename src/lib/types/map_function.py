from typing import Callable, TypeAlias

from .generic import T, R

MapFunc: TypeAlias = Callable[[T], R]
