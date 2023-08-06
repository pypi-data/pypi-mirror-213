"""@Author: Rayane AMROUCHE

Pandas source.
"""

from typing import Any

from datachain.sources.files._file import get_file
from datachain.sources._utils import filter_request_params
from datachain.sources.bytes._pandas import read_pandas as read_bytes


def read_pandas(path: str, **kwds: Any) -> Any:
    """Read a file into a pandas DataFrame.

    Parameters:
        path (str): The path to the input file.
        **kwds (Any): Keyword arguments to pass to the reading method.

    Returns:
        pandas.DataFrame: The DataFrame created from the file.
    """

    file_extension = path.split(".")[-1].lower()

    read_file_params, kwds = filter_request_params(kwds)

    return read_bytes(get_file(path, **read_file_params), file_extension, **kwds)


def write_pandas(data: Any, path: str, **kwds: Any) -> None:
    """Save a pandas DataFrame to the specified file format.

    Parameters:
        data (pandas.DataFrame): The DataFrame to save.
        path (str): The path to the output file.
        encoding (str, optional): The character encoding to use when writing the
        file. Defaults to "utf-8".
        **kwds (Any): Keyword arguments to pass to the writing method.
    """

    supported_formats = {
        "csv": {"writer": "to_csv", "params": {"index": False}},
        "xls": {"writer": "to_excel", "params": {"index": False}},
        "xlsx": {"writer": "to_excel", "params": {"index": False}},
        "xlsm": {"writer": "to_excel", "params": {"index": False}},
        "xlsb": {"writer": "to_excel", "params": {"index": False}},
        "odf": {"writer": "to_excel", "params": {"index": False}},
        "ods": {"writer": "to_excel", "params": {"index": False}},
        "odt": {"writer": "to_excel", "params": {"index": False}},
        "json": {"writer": "to_json", "params": {"orient": "records"}},
        "html": {"writer": "to_html", "params": {"index": False}},
        "pkl": {"writer": "to_pickle", "params": {}},
        "parquet": {"writer": "to_parquet", "params": {"index": False}},
        "feather": {"writer": "to_feather", "params": {}},
        "dta": {"writer": "to_stata", "params": {"write_index": False}},
        "sas7bdat": {"writer": "to_sas", "params": {"index": False}},
        "h5": {"writer": "to_hdf", "params": {"key": "", "mode": "w"}},
        "txt": {"writer": "to_fwf", "params": {"index": False}},
        "blosc": {"writer": "to_blosc", "params": {"index": False}},
    }  # type: dict[str, dict]

    file_extension = path.split(".")[-1].lower()

    if file_extension not in supported_formats:
        raise ValueError(f"Error: {file_extension} format not supported.")

    params = supported_formats[file_extension]["params"]
    params.update(kwds)

    writer = getattr(data, supported_formats[file_extension]["writer"])
    writer(path, **params)
