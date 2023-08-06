import abc
from typing import Generic, TypeVar

__all__ = ["ChainOfResponsibilityLink"]

T = TypeVar("T")
U = TypeVar("U")


class ChainOfResponsibilityLink(Generic[T, U], metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self._next = None

    def _set_next(
        self, next: "ChainOfResponsibilityLink[T, U]"
    ) -> "ChainOfResponsibilityLink[T, U]":
        self._next = next
        return self._next

    @abc.abstractmethod
    def handle(self, request: T) -> U:
        if self._next is not None:
            return self._next.handle(request)

        return None
