"""@Author: Rayane AMROUCHE

Json source.
"""

import json

from datachain.sources.files._file import get_file


def read_json(file_path: str) -> dict:
    """Reads and loads JSON data from a file as a Python dictionary.

    Args:
        file_path (str): The path or file url to the JSON file to be read.

    Returns:
        dict: The JSON data loaded as a Python dictionary.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        JSONDecodeError: If the JSON data in the file is not valid.
    """
    with get_file(file_path) as file:
        data = json.load(file)
    return data
