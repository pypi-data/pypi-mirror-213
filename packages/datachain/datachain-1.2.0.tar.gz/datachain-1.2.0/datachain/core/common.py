"""@Author: Rayane AMROUCHE

Common classes.
"""

from __future__ import annotations

import json
import uuid
import inspect

try:
    from IPython.display import display  # type: ignore
except ImportError:
    pass

from typing import Any, Union, Optional, Tuple, Dict, List, Callable

from datachain.core.lazy import Lazy, LazyLoadingRequired
from datachain.core.sync import unwrap_async

from datachain.config.logging import Logger
from datachain.config.params import Params

session_uuid = uuid.uuid4()


class Pipe:
    """A class representing a transformation function."""

    def __init__(self, func: Callable, *args: Any, **kwds: Any) -> None:
        """Initialize a Pipe object.

        Args:
            func (Callable): The transformation function.
            *args (Any): Positional arguments to pass to the transformation function.
            **kwds (Any): Keyword arguments to pass to the transformation function.
        """
        self.func = func
        self.args = args
        self.kwds = kwds
        self.leaf = False
        self.name = "Default"

    def set_leaf(self) -> Any:
        """Set the Pipe object as a leaf node in a chain.

        Returns:
            Any: The current Pipe object.
        """
        self.leaf = True
        return self

    def rename(self, name: str) -> Any:
        """Rename the Pipe object.

        Args:
            name (str): The new name of the Pipe object.

        Returns:
            Any: The current Pipe object.
        """
        self.name = name
        return self


class DataCache:
    """A data storage class that can be accessed through attributes.

    Args:
        extractor (callable): Function to extract data.
        loader (callable): Function to load data.

    Attributes:
        __keys (list): List of keys.
    """

    def __init__(self, extractor, loader) -> None:
        self.extractor = extractor
        self.loader = loader
        self.__keys: List = []

    def keys(self):
        """Return a list of keys.

        Returns:
            list: List of keys.
        """
        return self.__keys

    def __getitem__(self, __name: str) -> Any:
        return self.extractor(__name)

    def __setitem__(self, __name: str, __value: Any) -> None:
        self.__keys.append(__name)
        self.loader(__name, __value)


class DataSource:
    """Data Source class."""

    def __init__(self, func: Any = None, **kwds) -> None:
        self.func = func
        self._cache = {}  # type: dict
        self.to_cache = None #type: Optional[str]
        self.params = kwds

    def preload(self, **kwds) -> Any:
        """Preload parameters for a given source.

        Args:
            **kwds: Arbitrary keyword arguments to feed parameters.

        Returns:
            Any: Returns the data source object.
        """
        self.params.update(kwds)
        return self

    def register(self, func: Callable) -> Any:
        """Register a function as the main source extractor.

        Args:
            func (Callable): The extractor function.

        Returns:
            Any: Returns the data source object.
        """
        self.func = func
        return self

    def cache(self, name: Optional[str]) -> DataSource:
        """Cache data or access cached data.

        Args:
            name (str): Name of the data in cache or to cache.

        Returns:
            DataSource: Returns self to use during extraction.
        """
        self.to_cache = name
        return self

    def clear_cache(self):
        """Clear the cache of the DataSource"""
        self._cache = {}

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        params = self.params.copy()
        params.update(kwds)
        if self.func:
            if self.to_cache in self._cache:
                res = self._cache[self.to_cache]
                self.to_cache = None
                return res
            data = self.func(*args, **params)
            if self.to_cache:
                self._cache[self.to_cache] = data
                self.to_cache = None
            return data
        return None


def _transform(obj: Any, func: Any, args: Tuple, kwds: Dict) -> Any:
    """Apply a given function to transform data using the given arguments.

    Args:
        obj (Any): Data to transform.
        func (Callable): Transforming function.
        args (Tuple): Arguments to pass to the transforming function.
        kwds (Dict): Keyword arguments to pass to the transforming function.

    Raises:
        ValueError: If the pipe target and a keyword argument have the same name.

    Returns:
        Any: Transformed data.
    """
    data = obj.data
    args = [arg.data if isinstance(arg, Data) else arg for arg in args]
    kwds = {k: (v.data if isinstance(v, Data) else v) for k, v in kwds.items()}

    target = None

    # If the function is a string, get the method with that name from the data object
    if isinstance(func, str):
        # Put a value in target because data is in the method
        target = func
        kwds["__target"] = target

        def get_attr(__data, *args, **kwargs):
            func = getattr(__data, kwargs["__target"])
            # If the attribute is not callable then it is not a method so it is returned
            if not callable(func):
                # Check if args and kwds are given while func is not callable
                if not args and not kwargs:
                    raise TypeError(f"'{type(func)}' object is not callable")
                Logger.logger.info("Reading attribute '%s'", kwargs["__target"])
                return func
            del kwargs["__target"]
            return func(*args, **kwargs)

        func = get_attr
        target = None

    elif isinstance(func, tuple):
        func, target = func
        # If the pipe target name is the same as a keyword argument name, raise an error
        if target in kwds:
            msg = f"{target} is both the pipe target and a keyword argument"
            raise ValueError(msg)
        # Add the data to the keyword arguments
        kwds[target] = data

    # If the data is awaitable then await it
    if inspect.isawaitable(data):
        func = unwrap_async(func, target)

    # If no target is given then obj is the first argument
    if target is None:
        return Logger.log_func(func)(data, *args, **kwds)
    # Otherwhise
    return Logger.log_func(func)(*args, **kwds)


class Data(Lazy):
    """Data class."""

    def __init__(
        self,
        extractor: Optional[Callable] = None,
        args: Optional[List] = None,
        kwds: Optional[Dict] = None,
        cached: bool = True,
    ) -> None:
        """Initializes a new Data instance.

        Args:
            extractor (Optional[Callable]): The data extraction function to use.
            params (Optional[Dict]): Parameters to pass to the extraction function.
            cached (bool): Whether the data should be cached or loaded on demand.
        """
        self.extractor = extractor
        if args is None:
            args = []
        if kwds is None:
            kwds = {}
        if extractor is None:
            self.params = inspect.signature(lambda: 1).bind()
        else:
            self.params = inspect.signature(extractor).bind(*args, **kwds)
        self.cached = cached

    @Lazy.property
    def data(self) -> Any:
        """Returns the value of the `_data` attribute, loading it lazily if necessary.

        Raises:
            LazyLoadingRequired: If the `_data` attribute has not yet been loaded.

        Returns:
            Any: The value of the `_data` attribute.
        """
        if not self.cached:
            self.__load__("data")
        try:
            return self._data  # type: ignore
        except AttributeError as err:
            raise LazyLoadingRequired from err

    def __load__(self, attr: Any) -> None:
        if attr == "data":
            if self.extractor is None:
                return None

            self._data = (  # pylint: disable=attribute-defined-outside-init
                self.extractor(*self.params.args, **self.params.kwargs)
            )
            return self._data
        return None

    def force_data(self, value: Any):
        """Force the data value of the instance.

        Args:
            value (Any): The new value to set for the data.
        """
        self._data = value  # pylint: disable=attribute-defined-outside-init
        return self

    def load_data(self):
        """Force the data value of the instance.

        Args:
            value (Any): The new value to set for the data.
        """
        self.__load__("data")
        return self

    def load_cache(self, datamanager: DataManager, key: str):
        """Load data to a DataManager cache

        Args:
            datamanager (DataManager): A DataManager object used to load data in cache.
            key (str): A string key used to retrieve cached data from the DataManager.

        Returns:
            self: The instance which is now cached.
        """
        datamanager.load_cache(self, key)
        return self

    def __repr__(self) -> str:
        try:
            return repr(self._data)
        except AttributeError:
            return "<Data not loaded>"

    def serialize(self):
        """Serialize the data, extractor, and parameters into a UUID string.

        Returns:
            str: A UUID string representing the serialized data, extractor, and
            parameters.
        """
        return f"<{repr(self.extractor)}{repr(self.params)}>"

    def _ipython_display_(self):
        try:
            display(self._data)
        except AttributeError:
            print("<Data not loaded>")

    def transform(self, func: Any, *args: Any, **kwds: Any) -> Data:
        """Transforms the current instance's data by applying a function to it and
        returns a new Data instance.

        Args:
            func (Any): The function to apply to the data.
            *args (Any): Additional positional arguments to pass to the function.
            **kwds (Any): Additional keyword arguments to pass to the function.

        Returns:
            Any: A new Data instance with the transformed data.
        """
        sign = inspect.signature(_transform).bind(self, func, args, kwds)
        return Data(_transform, list(sign.args), sign.kwargs, self.cached)

    def chain(self, *pipes: Pipe) -> Union[Any, Tuple[Any, List[Any]]]:
        """Chains multiple transformation functions together and applies them
        sequentially to the data stored in the current instance of Data.

        Args:
            *pipes (Pipe): One or more Pipe objects representing transformation
            functions to be applied.

        Returns:
            Union[Any, Tuple[Any, List[Any]]]: A tuple containing the transformed data
            from the last pipe and a list of transformed data from any leaf pipes
            encountered in the chain. If no leaf pipes are present, only the transformed
            data from the last pipe is returned.
        """
        res = self
        leaves = []
        for pipe in pipes:
            transformed_data = res.transform(pipe.func, *pipe.args, **pipe.kwds)
            if pipe.leaf:
                leaves.append(transformed_data)
            else:
                res = transformed_data
        return (res, leaves) if leaves else res

    def decorate(
        self,
        decorator: Callable,
        func: Callable,
        *args: Any,
        **kwds: Any,
    ) -> Data:
        """Apply a decorator to a transforming function and call it on the current
        instance data.

        Args:
            decorator (Callable): The decorator function to apply.
            func (Callable): The transforming function.
            *args (Any): Positional arguments to pass to the transforming function.
            **kwds (Any): Keyword arguments to pass to the transforming function.

        Returns:
            Any: The original Data instance.
        """
        decorator(_transform(self, func, args, kwds))
        return self

    @staticmethod
    def __setup_extract(
        extractor: Callable, key: Optional[str], args: Any, kwds: Any
    ) -> Any:
        """Set up the extraction process.

        Args:
            extractor (Callable): A function or class that extracts data from a source.
            *args (Any): Positional arguments for the extractor.
            **kwds (Any): Keyword arguments for the extractor.

        Returns:
            Any: The arguments to pass to the extractor function.
        """
        if key is not None:
            try:
                params = Params.config[key]
            except KeyError as _:
                params = {}
        else:
            params = {}
        params.update(kwds)
        extractor_func = getattr(extractor, "func", extractor)
        sign = inspect.signature(extractor_func).bind(*args, **params)
        if Logger.logger:
            Logger.logger.info(
                "Extract data from extractor '%s' using these arguments: %s",
                extractor_func.__name__,
                str(sign.arguments),
            )
        return sign

    @staticmethod
    def extract(
        extractor: Callable, *args: Any, key: Optional[str] = None, **kwds: Any
    ) -> Any:
        """Extract data from a data source using the config and an appropriate
        extractor.

        Args:
            extractor (Callable): A function or class that extracts data from a source.
            *args (Any): Positional arguments for the extractor.
            key (Optional[str], optional): Optional config key to access config params.
            Defaults to None.
            **kwds (Any): Keyword arguments for the extractor.

        Returns:
            Any: The extracted data.
        """
        params = Data.__setup_extract(extractor, key, args, kwds)
        data = Data(extractor, params.args, params.kwargs, True)
        return data

    def load(
        self, loader: Callable, *args: Any, key: Optional[str] = None, **kwds: Any
    ) -> Any:
        """Load data to a data source using the config and an appropriate loader.

        Args:
            loader (Callable): A function or class that load data to a source.
            *args (Any): Positional arguments for the extractor.
            key (Optional[str], optional): Optional config key to access config params.
            Defaults to None.
            **kwds (Any): Keyword arguments for the extractor.

        Returns:
            Any: The original data.
        """
        if key is not None:
            try:
                params = Params.config[key]
            except KeyError as _:
                params = {}
        else:
            params = {}
        params.update(kwds)
        loader_func = getattr(loader, "func", loader)
        sign = inspect.signature(_transform).bind(self, loader_func, args, params)
        _transform(*sign.args, **sign.kwargs)
        return self


class DataManager:
    """
    Data Manager class.

    Args:
        metadata (Dict): A dictionary of data metadata.
        cache (Optional): A data cache to store cached data. Defaults to None.

    """

    def __init__(self, metadata: Optional[Dict] = None, cache: Any = None) -> None:
        """Initialize a Data Manager instance."""
        if metadata is None:
            metadata = {}
        self.config = metadata
        if cache is None:
            cache = {}
        self.__cache: Any = cache
        self.__params: Dict = {}

    def __getitem__(self, key: str):
        self.__params = self.config[key]
        return self

    def __repr__(self) -> str:
        """Return the string representation of the Data Manager instance."""
        return json.dumps(self.config, indent=4)

    def __setup_extract(self, extractor: Callable, args: Any, kwds: Any) -> Any:
        """Set up the extraction process.

        Args:
            extractor (Callable): A function or class that extracts data from a source.
            *args (Any): Positional arguments for the extractor.
            **kwds (Any): Keyword arguments for the extractor.

        Returns:
            Any: The arguments to pass to the extractor function.
        """
        self.__params.update(kwds)
        extractor_func = getattr(extractor, "func", extractor)
        sign = inspect.signature(extractor_func).bind(*args, **self.__params)
        self.__params = {}
        if Logger.logger:
            Logger.logger.info(
                "Extract data from extractor '%s' using these arguments: %s",
                extractor_func.__name__,
                str(sign.arguments),
            )
        return sign

    def extract(self, extractor: Callable, *args: Any, **kwds: Any) -> Any:
        """Extract data from a data source using the config and an appropriate
        extractor.

        Args:
            extractor (Callable): A function or class that extracts data from a source.
            *args (Any): Positional arguments for the extractor.
            **kwds (Any): Keyword arguments for the extractor.

        Returns:
            Any: The extracted data.
        """
        params = self.__setup_extract(extractor, args, kwds)
        data = Data(extractor, params.args, params.kwargs, True)
        cache_key = str(uuid.uuid5(session_uuid, data.serialize()))
        if cache_key in self.__cache.keys():
            if Logger.logger:
                Logger.logger.info("Load data from cache")
            data.force_data(self.__cache[cache_key])
        else:
            self.load_cache(data, data.serialize())
        return data

    def uncached_extract(self, extractor: Callable, *args: Any, **kwds: Any) -> Data:
        """Extract data from a data source using the config and an appropriate
        extractor.

        Args:
            extractor (Callable): A function or class that extracts data from a source.
            *args (Any): Positional arguments for the extractor.
            **kwds (Any): Keyword arguments for the extractor.

        Returns:
            Any: The extracted data.
        """
        params = self.__setup_extract(extractor, args, kwds)
        data = Data(extractor, params.args, params.kwargs, False)
        return data

    def load_cache(self, data: Any, key: str) -> None:
        """Load data into the cache.

        Args:
            data (Any): The data to be cached.
            key (str): A string key used to retrieve cached data from the DataManager.

        Raises:
            NotImplementedError: If the data is an awaitable object, as these cannot be
            cached.
        """
        if Logger.logger:
            Logger.logger.info("Load data to cache")
        if not inspect.isawaitable(data.data):
            key = str(uuid.uuid5(session_uuid, key))
            self.__cache[key] = data.data
        else:
            raise NotImplementedError("Awaitable extraction is not cacheable")
