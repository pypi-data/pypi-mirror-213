import abc
from typing import Type, TypeVar

__all__ = ["BaseDependencyProvider"]

T = TypeVar("T")


class BaseDependencyProvider(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "contains")
            and callable(subclass.contains)
            and hasattr(subclass, "resolve")
            and callable(subclass.resolve)
            or NotImplemented
        )

    @abc.abstractmethod
    def contains(self, type: Type[T]) -> bool:
        """
        Checks if the requested type is registered in the provider's services
        """
        raise NotImplementedError

    @abc.abstractmethod
    def resolve(self, type: Type[T]) -> T:
        """
        Resolve a service along with its dependencies if it is registered in the provider.
        It it isn't, a TaipanUnregisteredError is raised.

        Warning : Depending on how the services were registered, the instance provided might
        not be of the requested type.
        """
        raise NotImplementedError
