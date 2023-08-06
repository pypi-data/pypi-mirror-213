"""@Author: Rayane AMROUCHE

DataFrame informations methods for the Utils class for the DataManager.
"""

from typing import List, Callable, Optional

import pandas as pd  # type: ignore
import numpy as np  # type: ignore

from datachain.sources._utils import camel_to_snake
from datachain.sources._utils import remove_special
from datachain.sources._utils import remove_spaces


class DataFrameUtils:
    """DataFrameUtils class brings utils tools for the data manager."""

    @staticmethod
    def unique(__df: pd.DataFrame) -> pd.DataFrame:
        """Print unique values of each column of a pandas DataFrame.

        Args:
            __df (pd.DataFrame): DataFrame whose columns' uniques are to be displayed.

        Returns:
            pd.DataFrame: Returns original DataFrame.
        """
        return (
            pd.DataFrame()
            .assign(**{"rank": range(len(__df))})
            .assign(**{col: pd.Series(__df[col].unique()) for col in __df.columns})
        )

    @staticmethod
    def describe(__df: pd.DataFrame) -> pd.DataFrame:
        """Print DataFrame description.

        Args:
            __df (pd.DataFrame): DataFrame whose description is to be described.

        Returns:
            pd.DataFrame: Returns DataFrame description.
        """
        cat_cols = __df.select_dtypes(exclude=["number"]).columns
        num_cols = __df.select_dtypes(include=["number"]).columns

        return (
            pd.DataFrame()
            .assign(
                **{
                    "count": __df.count(axis=0),
                    "dtypes": __df.dtypes,
                    "numeric": [
                        pd.api.types.is_numeric_dtype(dtype) for dtype in __df.dtypes
                    ],
                }
            )
            .assign(
                **{
                    "nunique": __df.nunique(),
                    "mode": __df.mode(dropna=False).iloc[0],
                    # "freq": stats.mode(__df, keepdims=True).count[0]
                }
            )
            .assign(
                **{
                    "mean": np.mean(
                        __df.assign(**{cat: np.nan for cat in cat_cols}), axis=0
                    ),
                    "std": np.std(
                        __df.assign(**{cat: np.nan for cat in cat_cols}), axis=0
                    ),
                    "median": np.median(
                        __df.assign(**{cat: np.nan for cat in cat_cols}), axis=0
                    ),
                    "quartile_1": np.percentile(
                        __df.assign(**{cat: np.nan for cat in cat_cols}), 25, axis=0
                    ),
                    "quartile_3": np.percentile(
                        __df.assign(**{cat: np.nan for cat in cat_cols}), 75, axis=0
                    ),
                    "min": np.min(
                        __df.assign(**{cat: np.nan for cat in cat_cols}), axis=0
                    ),
                    "max": np.max(
                        __df.assign(**{cat: np.nan for cat in cat_cols}), axis=0
                    ),
                    "skew": __df.assign(**{cat: np.nan for cat in cat_cols}).skew(),
                    "kurtosis": __df.assign(
                        **{cat: np.nan for cat in cat_cols}
                    ).kurtosis(),
                    "sem": __df.assign(**{cat: np.nan for cat in cat_cols}).sem(),
                }
            )
            .T.filter(items=list(num_cols) + list(cat_cols))
        )

    @staticmethod
    def clean_columns(
        __df: pd.DataFrame, new_steps: Optional[List[Callable]] = None
    ) -> pd.DataFrame:
        """Transform the columns names of a given dataframe.

        Args:
            __df (pd.DataFrame): DataFrame which columns are to be cleaned.
            new_steps (List[Callable], optional): List of functions to apply on columns
                names. Defaults to None.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        if new_steps is None:
            new_steps = []
        new_cols = []
        for col in __df.columns:
            cur_col = camel_to_snake(remove_spaces(remove_special(str(col))))
            for step in new_steps:
                cur_col = step(cur_col)
            if not cur_col:
                cur_col = "column"
            i = 1
            col_name = cur_col
            while col_name in new_cols:
                col_name = cur_col + f"_{i}"
                i += 1
            new_cols.append(col_name)

        return __df.set_axis(new_cols, axis=1)
