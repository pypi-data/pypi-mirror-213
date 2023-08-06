"""@Author Rayane AMROUCHE

Async tools.
"""

import functools
import asyncio

from typing import Any, Optional, Callable, Tuple

from concurrent.futures import ThreadPoolExecutor

import nest_asyncio  # type: ignore

nest_asyncio.apply()


def force_async(func: Any) -> Any:
    """Turns a sync function to async function using threads.

    Args:
        func (Any): Function to wrap.

    Returns:
        Any: Function wrapped with async transparency.
    """

    pool = ThreadPoolExecutor()

    @functools.wraps(func)
    async def wrapper(*args, **kwds) -> asyncio.Future:
        future = pool.submit(func, *args, **kwds)
        return await asyncio.wrap_future(future)  # make it awaitable

    return wrapper


def force_sync(func: Any) -> Any:
    """Turn an async function to sync function.

    Args:
        func (Any): Function to wrap.

    Returns:
        Any: Function wrapped with sync transparency.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwds):
        res = func(*args, **kwds)
        if asyncio.iscoroutine(res):
            return asyncio.get_event_loop().run_until_complete(res)
        return res

    return wrapper


@force_sync
async def batch_load_async(async_calls: Tuple) -> Any:
    """Launch a batch of asynchronous data loader.

    Args:
        async_calls (Tuple): Asynchronous calls as a tuple of function, arguments
            and keyword arguments.

    Returns:
        Any: All the datas loaded in an array.
    """
    return await asyncio.gather(*async_calls)


def unwrap_async(func: Callable, target: Optional[str]):
    """Wraps an async function to automatically await a single argument or keyword
    argument.

    Args:
        func (Callable): The async function to wrap.
        target (Optional[str]): The name of the keyword argument to await (if given).

    Returns:
        Callable: The wrapped function.
    """
    functools.wraps(func)

    if target is None:

        async def wrapper_target(obj, *args, **kwds):
            obj = await obj
            return func(obj, *args, **kwds)

        return wrapper_target

    async def wrapper(*args, **kwds):
        kwds[target] = await kwds[target]
        return func(*args, **kwds)

    return wrapper
