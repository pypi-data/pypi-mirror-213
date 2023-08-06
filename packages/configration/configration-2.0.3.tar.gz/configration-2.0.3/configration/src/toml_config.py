"""Return a valid config object from a toml file for the application."""

import tomli
import tomli_w
from termcolor import cprint
import colorama

from .config import Config
from .constants import ERROR_COLOUR, LOCATION_ERR_MSG, INVALID_TOML_MSG

colorama.init()


class TomlConfig(Config):
    """
        A class to handle config files in toml format
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _read_config(self) -> dict[str, object]:
        # Open the config file and return the contents as a dict
        try:
            with open(self.path, 'rb') as f_config:
                try:
                    return tomli.load(f_config)
                except tomli.TOMLDecodeError:
                    cprint(f"{INVALID_TOML_MSG} {self.path }", ERROR_COLOUR)
        except FileNotFoundError:
            if self.create:
                return self._create_config()
            else:
                cprint(f"{LOCATION_ERR_MSG} {self.path}", ERROR_COLOUR)
        return {}

    def _create_config(self):
        config_list = []
        config = {}
        for key, attr in self.attrs.items():
            if int in attr:
                config_list.append(f'{key} = 0')
                config[key] = 0
            elif float in attr:
                config_list.append(f'{key} = 0.0')
                config[key] = 0.0
            elif str in attr:
                config_list.append(f'{key} = ""')
                config[key] = ''
            elif list in attr:
                config_list.append(f'{key} = []')
                config[key] = []

        with open(self.path, 'w') as f_config:
            f_config.write('\n'.join(config_list))
        return config

    # def _dumps_value(self, value):
    #     if isinstance(value, bool):
    #         return "true" if value else "false"
    #     elif isinstance(value, (int, float)):
    #         return str(value)
    #     elif isinstance(value, str):
    #         return f'"{value}"'
    #     elif isinstance(value, list):
    #         return f"[{', '.join(self._dumps_value(v) for v in value)}]"
    #     else:
    #         raise TypeError(f"{type(value).__name__} {value!r} is not supported")

    # def dumps(self, toml_dict, table=""):
    #     toml = []
    #     for key, value in toml_dict.items():
    #         if isinstance(value, dict):
    #             table_key = f"{table}.{key}" if table else key
    #             toml.append(f"\n[{table_key}]\n{self.dumps(value, table_key)}")
    #         else:
    #             toml.append(f"{key} = {self._dumps_value(value)}")
    #     return "\n".join(toml)

    def save(self):
        with open(self.path, mode="wb") as f_config:
            tomli_w.dump(self.__dict__['config'], f_config)
