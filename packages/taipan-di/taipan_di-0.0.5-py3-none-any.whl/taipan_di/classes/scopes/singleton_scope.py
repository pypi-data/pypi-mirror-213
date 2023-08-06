from typing import Any, Callable, Type, TypeVar, cast

from taipan_di.interfaces import BaseDependencyProvider, BaseScope

__all__ = ["SingletonScope"]

T = TypeVar("T")


class SingletonScope(BaseScope):
    def __init__(self, creator: Callable[[BaseDependencyProvider], Any]) -> None:
        self._creator = creator
        self._memoized_instance = None

    def get_instance(self, type: Type[T], container: BaseDependencyProvider) -> T:
        if self._memoized_instance is None:
            self._memoized_instance = self._creator(container)

        result = cast(type, self._memoized_instance)
        return result
