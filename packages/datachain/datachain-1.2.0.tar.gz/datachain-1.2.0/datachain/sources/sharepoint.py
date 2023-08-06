"""@Author: Rayane AMROUCHE

Sharepoint source.
"""

import io

from typing import Any, Optional

from shareplum import Site  # type: ignore # pylint: disable=import-error
from shareplum import Office365  # type: ignore # pylint: disable=import-error
from shareplum.site import Version  # type: ignore # pylint: disable=import-error

# type: ignore # pylint: disable=import-error
from shareplum.site import _Site365


from datachain.sources.bytes._pandas import read_pandas
from datachain.sources._utils import login
from datachain.sources.utils.utils import PandasUtils
from datachain import DataSource


def _read_sharepoint(
    url: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
    username_env: str = "",
    password_env: str = "",
    **kwds
):  # pylint: disable=too-many-arguments
    username, password = login(username, password, username_env, password_env)

    path_split = url.split("/")
    authcookie = Office365(
        "/".join(path_split[:3]),
        username=username,
        password=password,
    ).GetCookies()
    site = Site(
        "/".join(path_split[:5]),
        version=Version.v365,
        authcookie=authcookie,
    )
    if not isinstance(site, _Site365):
        return None
    folder = site.Folder("/".join(path_split[5:-1]))
    file = folder.get_file(path_split[-1])

    # handle csv files
    if path_split[-1].split(".")[-1].lower() == "csv":
        file = io.StringIO(file.decode(encoding=kwds.get("encoding", "utf-8")))

    data = read_pandas(file, path_split[-1].split(".")[-1].lower(), **kwds)
    return data


class TabularSource(DataSource):  # pylint: disable=too-few-public-methods
    """Pandas implementation of DataSource being able to read dataframes"""

    def __init__(self, **kwds: Any) -> None:
        super().__init__(_read_sharepoint, **kwds)

    schema = {
        "username_env": "onedrive_username_environment_variable_name",
        "password_env": "onedrive_password_environment_variable_name",
        "path": "https://sharepoint_address.sharepoint.com/sites/site_name/"
        "folder/file.xlsx",
    }
    utils = PandasUtils()
