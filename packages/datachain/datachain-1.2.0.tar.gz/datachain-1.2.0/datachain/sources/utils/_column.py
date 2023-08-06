"""@Author: Rayane AMROUCHE

Column transformation methods for the Utils class for the DataManager.
"""

from typing import Any, List, Optional

import pandas as pd  # type: ignore


class ColumnUtils:
    """ColumnUtils class brings utils tools for the data manager."""

    def __init__(self) -> None:
        pass

    @staticmethod
    def onehot_encode(__df: pd.DataFrame, column: str, **kwargs: Any) -> pd.DataFrame:
        """Encode a column using the onehot method.

        Args:
            __df (pd.DataFrame): DataFrame which column are to be onehot encoded.
            column (str): Column to onehot encode.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        return __df.assign(**pd.get_dummies(__df[column], prefix=column, **kwargs))

    @staticmethod
    def onehot_decode(__df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Decode a list of columns using the onehot method.

        Args:
            __df (pd.DataFrame): DataFrame which columns are the result of a onehot
            encoding.
            columns (str): Column to onehot decode.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        return __df.assign(**pd.from_dummies(__df[columns]))

    @staticmethod
    def column_spliter(
        __df: pd.DataFrame,
        column: str,
        columns: Optional[List[str]] = None,
        prefix: Any = None,
    ) -> pd.DataFrame:
        """Split a column which contain a dict or a list.

        Args:
            __df (pd.DataFrame): Dataframe from which a column will be splited.
            column (str): Column to split.
            columns (List[str]): Name of the columns after split.
            prefix (str): Prefix for splited columns.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        if prefix is None:
            prefix = column + "_"
        if columns is None:
            return __df.assign(
                **pd.DataFrame(__df[column].to_list()).add_prefix(prefix)
            )
        return __df.assign(
            **pd.DataFrame(__df[column].to_list(), columns=columns).add_prefix(prefix)
        )
