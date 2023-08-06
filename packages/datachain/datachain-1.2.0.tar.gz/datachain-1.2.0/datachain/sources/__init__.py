"""@Author: Rayane AMROUCHE
"""

try:
    from datachain.sources import file
except ImportError:
    pass

try:
    from datachain.sources import ftp
except ImportError:
    pass

try:
    from datachain.sources import http
except ImportError:
    pass

try:
    from datachain.sources import sftp
except ImportError:
    pass
try:
    from datachain.sources import sharepoint
except ImportError:
    pass

try:
    from datachain.sources import sql
except ImportError:
    pass
