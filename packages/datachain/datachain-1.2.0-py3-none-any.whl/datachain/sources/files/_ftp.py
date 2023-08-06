"""@Author: Rayane AMROUCHE

Ftp source.
"""

import io
import ftplib

from urllib.parse import unquote


def ftp_to_file(ftp_url: str) -> io.BytesIO:
    """Retrieves bytes from an FTP path.

    Args:
        ftp_url (str): The URL of the FTP server.

    Returns:
        io.BytesIO: A file-like object containing the bytes read from the FTP path.

    Raises:
        ftplib.all_errors: If an error occurs while accessing the FTP server.
    """
    # Split the FTP URL into its components
    parts = ftp_url.split("/")
    username_password = parts[2].split("@")[0]
    username, password = username_password.split(":")
    server = parts[2].split("@")[1]
    path = "/" + "/".join(parts[3:])

    # Connect to the FTP server and retrieve the file
    with ftplib.FTP(unquote(server)) as ftp:
        ftp.login(user=unquote(username), passwd=unquote(password))
        def _nothing(_: bytes):
            return
        ftp_path = f"RETR {path}"
        with ftp.retrbinary(ftp_path, callback=_nothing) as file: #type: ignore
            data_bytes = file.read()
            data = io.BytesIO(data_bytes)
            return data
