"""@Author: Rayane AMROUCHE

Pandas source.
"""

from urllib.parse import quote
from typing import Any

import pandas as pd  # type: ignore
import sqlalchemy  # type: ignore


def read_pandas(  # pylint: disable=too-many-arguments
    dialect: str = "",
    username: str = "",
    password: str = "",
    address: str = "",
    database: str = "",
    query: str = "",
    table_name: str = "",
    **kwds: Any,
) -> pd.DataFrame:
    """Query an SQL database into a pandas DataFrame.

    Parameters:
        dialect (str): Sqlalchemy dialect for the SQL server.
        username (str): Username to access the SQL server.
        password (str): Password to access the SQL server.
        address (str): Address of the SQL server.
        database (str): Database to access in the SQL server.
        query (str, optional): SQL query. Defaults to "".
        table_name (str, optional): Table name to query. Defaults to "".
        **kwds (Any): Keyword arguments to pass to the reading method.

    Returns:
        pandas.DataFrame: The DataFrame created from the query or table.
    """
    if len(dialect) == 0:
        for _d in ["mysql", "postgresql", "snowflake", "oracle", "mssql", "sqlite"]:
            try:
                uri = f"{_d}://{username}:{quote(password)}@{address}/{database}"
                _ = sqlalchemy.create_engine(uri).connect().close()
                dialect = _d
                break
            except Exception as _:  # pylint: disable=broad-except
                pass
    uri = f"{dialect}://{username}:{quote(password)}@{address}/{database}"
    engine = sqlalchemy.create_engine(uri)
    if query:
        conn = engine.connect()
        data = pd.read_sql_query(query, conn, **kwds)
        conn.close()
    elif table_name:
        conn = engine.connect()
        data = pd.read_sql_table(table_name, conn, **kwds)
        conn.close()
    else:
        data = engine

    return data


def write_pandas(  # pylint: disable=too-many-arguments
    data: Any,
    dialect: str = "",
    username: str = "",
    password: str = "",
    address: str = "",
    database: str = "",
    table_name: str = "",
    **kwds: Any,
) -> None:
    """Save a pandas DataFrame in a database as with a given table name.

    Parameters:
        data (pandas.DataFrame): The DataFrame to save.
        dialect (str): Sqlalchemy dialect for the sql server.
        username (str): Username to access the sql server.
        password (str): Password to access the sql server.
        address (str): Address of the sql server.
        database (str): Database to access in the sql server.
        table_name (str, optional): Table name to query. Defaults to "".
        **kwds (Any): Keyword arguments to pass to the writing method.
    """
    uri = f"{dialect}://{username}:{quote(password)}@{address}/{database}"
    engine = sqlalchemy.create_engine(uri)
    conn = engine.connect()
    if data:
        data.to_sql(
            table_name,
            con=conn,
            **kwds,
        )
    conn.close()
