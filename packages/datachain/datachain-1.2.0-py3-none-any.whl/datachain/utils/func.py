"""@Author: Rayane AMROUCHE

Utils functions.
"""

from typing import Any, Dict


def format_dict(dico: Dict, formatting: Any) -> None:
    """Format a dict that contain formattable strings.

    Args:
        dico (Dict): Dict where keys have to be formated.
        formatting (Dict): Formatting dictionary.

    """
    if formatting is None:
        return
    for key_, value_ in dico.items():
        if isinstance(value_, str) and any(k in value_ for k in formatting.keys()):
            dico[key_] = value_.format(**formatting)
        if isinstance(value_, dict):
            format_dict(value_, formatting)
