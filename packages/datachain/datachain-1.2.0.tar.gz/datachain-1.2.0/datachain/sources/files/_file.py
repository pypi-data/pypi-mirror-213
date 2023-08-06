"""@Author: Rayane AMROUCHE

File source.
"""

import io

from typing import Any
from datachain.sources.files._ftp import ftp_to_file
from datachain.sources.files._local import local_to_file
from datachain.sources._utils import missing_lib
try:
    from datachain.sources.files._sftp import sftp_to_file
except ImportError:
    sftp_to_file = missing_lib("paramiko", "SFTP")

try:
    from datachain.sources.files._http import http_to_file
except ImportError:
    http_to_file = missing_lib("requests", "HTTP")


def get_file(path: str, *args: Any, **kwds: Any) -> io.BytesIO:
    """Reads bytes from a path or file server URL.

    Args:
        path (str): The path or file URL to the file to read.

    Returns:
        io.BytesIO: The bytes read from the file.
    """
    if path.startswith(("http://", "https://")):
        return http_to_file(path, *args, **kwds)
    if path.startswith("ftp://"):
        return ftp_to_file(path)
    if path.startswith("sftp://"):
        return sftp_to_file(path)
    return local_to_file(path)
