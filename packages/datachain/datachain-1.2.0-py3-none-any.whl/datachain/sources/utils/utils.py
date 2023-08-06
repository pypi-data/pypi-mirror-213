"""@Author: Rayane AMROUCHE

Utils for DataManager.
"""

from datachain.sources.utils._dataframe import DataFrameUtils
from datachain.sources.utils._column import ColumnUtils


class PandasUtils:  # pylint: disable=too-few-public-methods
    """Utils class brings utils tools for the data manager."""

    def __init__(self) -> None:
        """Init class Utils with an empty local storage.

        Args:
            __dm (Any): DataManager from which these utils are called.
        """
        self.column = ColumnUtils()
        self.dataframe = DataFrameUtils()
