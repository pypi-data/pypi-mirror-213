import abc
from typing import Callable, Generic, TypeVar

__all__ = ["PipelineLink"]

T = TypeVar("T")
U = TypeVar("U")


class PipelineLink(Generic[T, U], metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self._next = None

    def _set_next(self, next: "PipelineLink[T, U]") -> "PipelineLink[T, U]":
        self._next = next
        return self._next

    def exec(self, request: T) -> U:
        next_function = self._next.exec if self._next is not None else lambda req: None

        return self._handle(request, next_function)

    @abc.abstractmethod
    def _handle(self, request: T, next: Callable[[T], U]) -> U:
        return next(request)
