"""@Author: Rayane AMROUCHE

Ftp source.
"""

from typing import Any, Optional
from urllib.parse import quote


from datachain.sources.files._pandas import read_pandas
from datachain.sources._utils import login
from datachain.sources.utils.utils import PandasUtils
from datachain import DataSource


def _read_ftp(
    path: str,
    server: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
    username_env: str = "",
    password_env: str = "",
):  # pylint: disable=too-many-arguments
    username, password = login(username, password, username_env, password_env)
    ftp_path = f"ftp://{quote(username)}:{quote(password)}@{quote(server)}/{path}"
    return read_pandas(ftp_path)


class TabularSource(DataSource):  # pylint: disable=too-few-public-methods
    """Pandas implementation of DataSource being able to read dataframes from an ftp
    server"""

    schema = {
        "path": "file_path",
        "server": "ftp_server_address",
        "username_env": "server_username_environment_variable_name",
        "password_env": "server_password_environment_variable_name",
    }

    def __init__(self, **kwds: Any) -> None:
        super().__init__(_read_ftp, **kwds)
    utils = PandasUtils()
