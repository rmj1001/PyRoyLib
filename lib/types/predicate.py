from typing import Callable, TypeVar

T = TypeVar('T')
Predicate = Callable[[T], bool]
