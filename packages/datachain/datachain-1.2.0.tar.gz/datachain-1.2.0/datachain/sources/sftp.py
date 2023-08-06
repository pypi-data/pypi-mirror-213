"""@Author: Rayane AMROUCHE

Sftp source.
"""

from typing import Any, Optional
from urllib.parse import quote


from datachain.sources.files._pandas import read_pandas
from datachain.sources._utils import login
from datachain.sources.utils.utils import PandasUtils
from datachain import DataSource


def _read_sftp(
    path: str,
    server: str,
    port: Optional[int] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    username_env: str = "",
    password_env: str = "",
):  # pylint: disable=too-many-arguments
    username, password = login(username, password, username_env, password_env)
    server = quote(server)
    if port:
        server += ":" + str(port)
    sftp_path = f"sftp://{quote(username)}:{quote(password)}@{server}/{path}"
    return read_pandas(sftp_path)


class TabularSource(DataSource):  # pylint: disable=too-few-public-methods
    """Pandas implementation of DataSource being able to read dataframes"""

    def __init__(self, **kwds: Any) -> None:
        super().__init__(_read_sftp, **kwds)

    schema = {
        "path": "file_path",
        "server": "ftp_server_address",
        "port": "port_if_needed",
        "username_env": "server_username_environment_variable_name",
        "password_env": "server_password_environment_variable_name",
    }
    utils = PandasUtils()
