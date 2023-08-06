"""@Author: Rayane AMROUCHE

FTP source.
"""

import io
from urllib.parse import unquote
import paramiko  # type: ignore


def sftp_to_file(sftp_url: str) -> io.BytesIO:
    """Retrieves bytes from an SFTP path.

    Args:
        sftp_url (str): The URL of the SFTP server.

    Raises:
        paramiko.SSHException: If an error occurs while accessing the SFTP server.

    Returns:
        io.BytesIO: A file-like object containing the bytes read from the SFTP path.
    """
    # Split the SFTP URL into its components
    parts = sftp_url.split("/")
    username_password = parts[2].split("@")[0]
    username, password = username_password.split(":")
    server_port = parts[2].split("@")[1]
    server = server_port.split(":")[0]
    port = int(server_port.split(":")[1]) if ":" in server_port else 22
    path = "/" + "/".join(parts[3:])

    # Connect to the SFTP server and retrieve the file
    with paramiko.Transport((unquote(server), port)) as transport:
        transport.connect(username=unquote(username), password=unquote(password))
        with paramiko.SFTPClient.from_transport(transport) as sftp:
            with sftp.open(path, "rb") as file:
                data_bytes = file.read()
                data = io.BytesIO(data_bytes)
                return data
