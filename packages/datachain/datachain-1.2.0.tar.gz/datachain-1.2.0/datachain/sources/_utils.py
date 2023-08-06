"""@Author: Rayane AMROUCHE

Utils for sources.
"""

import re

from typing import Optional, Tuple
from dotenv import dotenv_values

from datachain.config import Params


def login(
    username: Optional[str] = None,
    password: Optional[str] = None,
    username_env: str = "",
    password_env: str = "",
) -> Tuple[str, str]:
    """Login function to retrieve username and password.

    Args:
        username (Optional[str], optional): The username. Defaults to None.
        password (Optional[str], optional): The password. Defaults to None.
        username_env (str, optional): The environment variable name for the username.
        Defaults to "".
        password_env (str, optional): The environment variable name for the password.
        Defaults to "".

    Raises:
        AttributeError: Raised when neither the username nor the name of the username in
        the environment was given.
        AttributeError: Raised when neither the password nor the name of the password in
        the environment was given.

    Returns:
        Tuple[str, str]: A tuple containing the username and password.
    """
    try:
        if not username:
            username = dotenv_values(Params.env_path)[username_env]
    except KeyError as _:
        raise AttributeError(
            "Neither the username nor a valid username in the environment was given."
        ) from _

    try:
        if not password:
            password = dotenv_values(Params.env_path)[password_env]
    except KeyError as _:
        raise AttributeError(
            "Neither the password nor a valid password in the environment was given."
        ) from _

    if username is None:
        username = ""
    if password is None:
        password = ""

    return username, password


def camel_to_snake(__str: str) -> str:
    """Transform a camel case name to a snake case one.

    Args:
        __str (str): String to transform.

    Returns:
        str: Transformed string.
    """
    __str = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", __str)
    __str = re.sub("([a-z0-9])([A-Z])", r"\1_\2", __str).lower()
    return re.sub("_+", "_", __str)


def remove_special(__str: str) -> str:
    """Transform special characters to their meaning or to space.

    Args:
        __str (str): String to transform.

    Returns:
        str: Transformed string.
    """
    __str = __str.replace("%", " Percent ")
    __str = __str.replace("@", " At ")
    __str = __str.replace("/w ", " With ")
    return re.sub(r"\W+", " ", __str)


def remove_spaces(__str: str) -> str:
    """Transform spaces to simple underscore.

    Args:
        __str (str): String to transform.

    Returns:
        str: Transformed string.
    """
    __str = re.sub(" +", " ", __str)
    __str = __str.strip(" ")
    return __str.replace(" ", "_")


def filter_request_params(kwds: dict) -> Tuple[dict, dict]:
    """Filter request arguments from kwds.

    Args:
        kwds (dict): keyword arguments dict.

    Returns:
        Tuple[dict, dict]: request params, non-request params.
    """
    read_file_params = {}
    for param in kwds.items():
        if param in [
            "params",
            "data",
            "headers",
            "cookies",
            "files",
            "auth",
            "timeout",
            "allow_redirects",
            "proxies",
            "hooks",
            "stream",
            "verify",
            "cert",
            "json",
        ]:
            read_file_params[param] = kwds[param]
            del kwds[param]
    return read_file_params, kwds


def missing_lib(m_lib: str, m_source: str):
    """_summary_

    Args:
        missing_lib (str): _description_
        missing_source (str): _description_
    """

    def raise_error(*_, **_2):
        raise ImportError(
            f"Module '{m_lib}' is missing. It is needed to execute {m_source} requests."
        )

    return raise_error
