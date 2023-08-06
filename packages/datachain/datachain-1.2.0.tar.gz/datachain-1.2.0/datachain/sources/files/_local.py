"""@Author: Rayane AMROUCHE

Local source.
"""

import io


def local_to_file(file_path: str) -> io.BytesIO:
    """Reads bytes from a local file.

    Args:
        file_path (str): The path to the file to read.

    Returns:
        io.BytesIO: A file-like object containing the bytes read from the file.
    """
    with open(file_path, "rb") as infile:
        data_bytes = infile.read()
    data = io.BytesIO(data_bytes)
    return data
