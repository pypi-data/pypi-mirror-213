"""@Author: Rayane AMROUCHE

Sql sources.
"""

from typing import Any, Optional


from datachain.sources.query._pandas import read_pandas, write_pandas
from datachain.sources._utils import login
from datachain.sources.utils.utils import PandasUtils
from datachain import DataSource


def _read_sql(
    dialect: str = "",
    username: Optional[str] = None,
    password: Optional[str] = None,
    username_env: str = "",
    password_env: str = "",
    address: str = "",
    database: str = "",
    query: str = "",
    table_name: str = "",
    **kwds: Any,
):  # pylint: disable=too-many-arguments
    username, password = login(username, password, username_env, password_env)
    return read_pandas(
        dialect, username, password, address, database, query, table_name, **kwds
    )


def _write_sql(
    data: Any = None,
    dialect: str = "",
    username: Optional[str] = None,
    password: Optional[str] = None,
    username_env: str = "",
    password_env: str = "",
    address: str = "",
    database: str = "",
    table_name: str = "",
    **kwds: Any,
):  # pylint: disable=too-many-arguments
    username, password = login(username, password, username_env, password_env)
    return write_pandas(
        data, dialect, username, password, address, database, table_name, **kwds
    )


class TabularSource(DataSource):  # pylint: disable=too-few-public-methods
    """Pandas implementation of DataSource being able to query tables"""

    def __init__(self, **kwds: Any) -> None:
        super().__init__(_read_sql, **kwds)

    schema = {
        "dialect": "postgresql | mysql | snowflake | ...",
        "username_env": "sql_username_environment_variable_name",
        "password_env": "sql_password_environment_variable_name",
        "address": "sql_host:port",
        "database": "database_name",
        "query|table_name": "SELECT * from TABLE | TABLE",
    }
    utils = PandasUtils()


class TabularSink(DataSource):  # pylint: disable=too-few-public-methods
    """Pandas implementation of DataSource being able to write tables"""

    def __init__(self, **kwds: Any) -> None:
        super().__init__(_write_sql, **kwds)

    schema = {
        "dialect": "postgresql | mysql | snowflake | ...",
        "username_env": "sql_username_environment_variable_name",
        "password_env": "sql_password_environment_variable_name",
        "address": "sql_host:port",
        "database": "database_name",
        "table_name": "TABLE",
    }
