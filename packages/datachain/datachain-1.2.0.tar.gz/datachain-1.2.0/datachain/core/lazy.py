"""@Author: Rayane AMROUCHE

Lazy class.
"""

from functools import wraps
from typing import Callable, Any
from abc import abstractmethod


def lazy(method: Callable) -> Callable:
    """Decorator to make a method lazy-loaded.

    Args:
        method (Callable): The method to be made lazy-loaded.

    Returns:
        Callable: The wrapped method that caches the result of the original method call
        on the first invocation, and then returns the cached result on all subsequent
        invocations.
    """

    @wraps(method)
    def wrapper(self) -> Any:
        lazy_name = f"_lazy__{method.__name__}"
        try:
            return getattr(self, lazy_name)
        except AttributeError:
            value = method(self)
            setattr(self, lazy_name, value)
            return value

    return wrapper


def lazy_property(method: Callable) -> property:
    """Decorator to make a property lazy-loaded.

    Args:
        method (Callable): The method to be made lazy-loaded.

    Returns:
        property: The wrapped property object that caches the result of the original
        method call on the first invocation, and then returns the cached result on all
        subsequent invocations.
    """
    return property(lazy(method))


class LazyLoadingRequired(Exception):
    """Exception raised when an attempt is made to access a lazy-loaded attribute that
    has not been loaded yet."""


class Lazy:
    """_summary_"""

    @abstractmethod
    def __load__(self, attr: Any) -> None:
        """Load the attribute with the given name.

        Args:
            attr (Any): The name of the attribute to be loaded.
        """

    class _property(property):
        """Subclass of property to support lazy-loading of attributes."""

        def __get__(self, instance: Any, _: Any = None) -> Any:
            if instance is None:
                return self
            if self.fget is None:
                raise AttributeError("Unreadable attribute")

            try:
                return self.fget(instance)
            except LazyLoadingRequired:
                attr = getattr(self.fget, "_Lazy__attr")
                instance.__load__(attr)
                return self.fget(instance)

    @staticmethod
    def property(attr_or_method: Any) -> Any:
        """Decorator to make a class attribute lazy-loaded.

        Args:
            attr_or_method (Any): The name of the attribute to be loaded or the method
            that loads the attribute.

        Returns:
            Any: The decorated method or the decorated property object.
        """

        def decorator(method: Callable) -> property:
            attr = attr_or_method if not callable(attr_or_method) else method.__name__
            setattr(method, "_Lazy__attr", attr)
            prop = Lazy._property(method)
            setattr(prop, "_Lazy__attr", attr)
            return prop

        if callable(attr_or_method) and not isinstance(attr_or_method, type):
            return decorator(attr_or_method)
        return decorator
