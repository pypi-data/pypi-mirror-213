"""@Author: Rayane AMROUCHE

Pandas source.
"""

from typing import Any

import pandas as pd  # type: ignore


def read_pandas(data_bytes: Any, file_extension: str, **kwds: Any) -> pd.DataFrame:
    """Read a file into a pandas DataFrame.

    Parameters:
        data_bytes (Any): The data to read into a DataFrame.
        file_extension (str): The file extension indicating the file format.
        **kwds (Any): Keyword arguments to pass to the reading method.

    Returns:
        pandas.DataFrame: The DataFrame created from the file.
    """

    readers = {
        "csv": pd.read_csv,
        "xls": pd.read_excel,
        "xlsx": pd.read_excel,
        "xlsm": pd.read_excel,
        "xlsb": pd.read_excel,
        "odf": pd.read_excel,
        "ods": pd.read_excel,
        "odt": pd.read_excel,
        "pkl": pd.read_pickle,
        "feather": pd.read_feather,
        "parquet": pd.read_parquet,
        "dta": pd.read_stata,
        "sas7bdat": pd.read_sas,
        "txt": pd.read_fwf,
        "h5": pd.read_hdf,
        "json": pd.read_json,
        "html": pd.read_html,
    }

    if file_extension in readers:
        reader = readers[file_extension]
        data = reader(data_bytes, **kwds)
        return data

    raise NotImplementedError(
        f"Error: {file_extension} format not supported by pandas."
    )
