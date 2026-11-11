from abc import ABC, abstractmethod


class IMath(ABC):
    @abstractmethod
    def __add__(self, other):
        """self + other"""

    @abstractmethod
    def __iadd__(self, other):
        """self += other"""

    @abstractmethod
    def __sub__(self, other):
        """self - other"""

    @abstractmethod
    def __isub__(self, other):
        """self -= other"""

    @abstractmethod
    def __mul__(self, other):
        """self * other"""

    @abstractmethod
    def __imul__(self, other):
        """self *= other"""

    @abstractmethod
    def __truediv__(self, other):
        """self / other"""

    @abstractmethod
    def __itruediv__(self, other):
        """self /= other"""

    @abstractmethod
    def __floordiv__(self, other):
        """self // other"""

    @abstractmethod
    def __ifloordiv__(self, other):
        """self //= other"""

    @abstractmethod
    def __mod__(self, other):
        """self % other"""

    @abstractmethod
    def __imod__(self, other):
        """self %= other"""

    @abstractmethod
    def __pow__(self, other):
        """self ** other"""

    @abstractmethod
    def __ipow__(self, other):
        """self **= other"""
