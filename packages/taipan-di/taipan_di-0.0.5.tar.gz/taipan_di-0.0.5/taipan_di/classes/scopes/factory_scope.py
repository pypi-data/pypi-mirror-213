from typing import Any, Callable, Type, TypeVar, cast

from taipan_di.interfaces import BaseDependencyProvider, BaseScope

__all__ = ["FactoryScope"]

T = TypeVar("T")


class FactoryScope(BaseScope):
    def __init__(self, creator: Callable[[BaseDependencyProvider], Any]) -> None:
        self._creator = creator

    def get_instance(self, type: Type[T], container: BaseDependencyProvider) -> T:
        instance = self._creator(container)
        result = cast(type, instance)
        return result
