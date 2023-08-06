"""Return a valid config object from a json file for the application."""

import json
from termcolor import cprint
import colorama

from .config import Config
from .constants import ERROR_COLOUR, LOCATION_ERR_MSG, INVALID_JSON_MSG

colorama.init()


class JsonConfig(Config):
    """
        A class to handle config files in json format
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _read_config(self) -> dict[str, object]:
        # Open the config file and return the contents as a dict
        try:
            with open(self.path, 'r') as f_config:
                try:
                    return json.load(f_config)
                except json.decoder.JSONDecodeError:
                    cprint(f"{INVALID_JSON_MSG} {self.path }", ERROR_COLOUR)
        except FileNotFoundError:
            if self.create:
                return self._create_config()
            else:
                cprint(f"{LOCATION_ERR_MSG} {self.path}", ERROR_COLOUR)
                return None
        return {}

    def _create_config(self):
        config = {}
        for key, attr in self.attrs.items():
            if int in attr:
                config[key] = 0
            elif float in attr:
                config[key] = 0.0
            elif str in attr:
                config[key] = ''
            elif list in attr:
                config[key] = []

        with open(self.path, 'w') as f_config:
            json.dump(config, f_config)
        return config
