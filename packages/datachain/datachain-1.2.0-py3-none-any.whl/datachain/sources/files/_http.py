"""@Author: Rayane AMROUCHE

Http source.
"""

from typing import Any
import io
import requests  # type: ignore


def http_to_file(
    url: str,
    *args: Any,
    request_type: str = "get",
    **kwds: Any,
) -> io.BytesIO:
    """Reads bytes from an HTTP(S) URL.

    Args:
        url (str): The URL of the file to read.
        request_type (str, optional): The HTTP request method to use. Defaults to "get".
        *args (Any): Variable length argument list passed to the HTTP request method.
        **kwds (Any): Arbitrary keyword arguments passed to the HTTP request method.

    Returns:
        io.BytesIO: A file-like object containing the bytes read from the URL.
    """
    response = getattr(requests, request_type)(  # pylint: disable=missing-timeout
        url, *args, **kwds
    )
    data = io.BytesIO(response.content)
    return data
