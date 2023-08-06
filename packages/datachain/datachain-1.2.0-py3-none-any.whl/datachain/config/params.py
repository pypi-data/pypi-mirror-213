"""@Author: Rayane AMROUCHE

Params class.
"""

import json


class Params:
    """Params class."""

    config = {}  # type: dict
    env_path = ".env"

    @classmethod
    def reset_config(cls):
        """Reset the shared config dictionnary."""
        cls.config = {}

    @classmethod
    def load_config(cls, path: str, encoding: str = "utf-8"):
        """Load a json file in the shared config dictionnary.

        Args:
            path (str): Path of the json file.
            encoding (str, optional): Encoding of the json file. Defaults to "utf-8".
        """
        with open(path, encoding=encoding) as json_file:
            data = json.load(json_file)
        for key_, value_ in data.items():
            cls.config[key_] = value_
