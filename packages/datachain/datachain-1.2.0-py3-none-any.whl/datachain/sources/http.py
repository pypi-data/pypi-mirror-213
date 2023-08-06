"""@Author: Rayane AMROUCHE

Http source.
"""

import json
from typing import Any


from datachain.sources._utils import missing_lib
try:
    from datachain.sources.files._http import http_to_file
except ImportError:
    http_to_file = missing_lib("requests", "HTTP")

from datachain.sources.files._pandas import read_pandas
from datachain.sources.utils.utils import PandasUtils
from datachain.sources._utils import filter_request_params
from datachain import DataSource

source_schema = {
    "path": "http_uri",
    "request_type": "get | post",
    "data": "optional_argument",
    "json": "optional_argument",
    "params": "optional_argument",
    "headers": "optional_argument",
    "cookies": "optional_argument",
    "files": "optional_argument",
    "auth": "optional_argument",
    "timeout": "optional_argument",
    "allow_redirects": "optional_argument",
    "proxies": "optional_argument",
    "hooks": "optional_argument",
    "stream": "optional_argument",
    "verify": "optional_argument",
    "cert": "optional_argument",
}

def _read_json(path: str, **kwds: Any) -> dict:
    read_file_params, kwds = filter_request_params(kwds)
    with http_to_file(path, **read_file_params) as file:
        data = json.load(file)
    return data


class TabularSource(DataSource):  # pylint: disable=too-few-public-methods
    """Pandas implementation of DataSource being able to read dataframes"""

    def __init__(self, **kwds: Any) -> None:
        super().__init__(read_pandas, **kwds)

    schema = source_schema
    utils = PandasUtils()


class JsonSource(DataSource):  # pylint: disable=too-few-public-methods
    """Pandas implementation of DataSource being able to read dataframes"""

    def __init__(self, **kwds: Any) -> None:
        super().__init__(_read_json, **kwds)

    schema = source_schema
    # utils = JsonUtils()
