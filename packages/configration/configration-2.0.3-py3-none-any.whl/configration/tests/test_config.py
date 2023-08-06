import os
from pathlib import Path

from ..src.json_config import JsonConfig
from ..src.toml_config import TomlConfig

CONFIG_ATTRS = {
    'month': [int],
    'payment': [float],
    'transactions': [list],
}
ANSI_COLOR_RED = "\x1b[31m"
ANSI_COLOR_RESET = "\x1b[0m"
ANSI_COLOR_RED = ""
ANSI_COLOR_RESET = ""


def test_all(capsys):
    for index, config_class in enumerate([JsonConfig, TomlConfig]):
        extension = ['json', 'toml'][index]
        config_structure(config_class, extension)
        config_missing(capsys, config_class, extension)
        config_invalid_attrs(capsys, config_class, extension)
        config_invalid_json(capsys, config_class, extension)
        config_missing_attr(capsys, config_class, extension)
        config_create(config_class, extension)


def config_structure(config_class, extension):
    path = Path('tests', 'test_data', f'config.{extension}')
    config = config_class(path)
    assert isinstance(config.config, dict)
    assert len(config.config) == 3


def config_missing(capsys, config_class, extension):
    path = Path('tests', 'test_data', f'not_a_file.{extension}')
    err_msg = f'The config file is not in the expected location: {path}'
    config_class(path)
    captured = capsys.readouterr()
    assert captured.out.strip() == f'{ANSI_COLOR_RED}{err_msg}{ANSI_COLOR_RESET}'


def config_invalid_attrs(capsys, config_class, extension):
    path = Path('tests', 'test_data', f'config_invalid_attrs.{extension}')
    err_msg = "Corrupt config file. month not of type [<class 'int'>]"
    config_class(path, CONFIG_ATTRS)
    captured = capsys.readouterr()
    assert captured.out.strip() == f'{ANSI_COLOR_RED}{err_msg}{ANSI_COLOR_RESET}'


def config_invalid_json(capsys, config_class, extension):
    path = Path('tests', 'test_data', f'config_invalid_{extension}.{extension}')
    err_msg = f"Invalid {extension} format in {path}"
    config_class(path)
    captured = capsys.readouterr()
    assert captured.out.strip() == f'{ANSI_COLOR_RED}{err_msg}{ANSI_COLOR_RESET}'


def config_missing_attr(capsys, config_class, extension):
    path = Path('tests', 'test_data', f'config_missing_attr.{extension}')
    err_msg = "Corrupt config file. Missing attribute: transactions"
    config_class(path, CONFIG_ATTRS)
    captured = capsys.readouterr()
    assert captured.out.strip() == f'{ANSI_COLOR_RED}{err_msg}{ANSI_COLOR_RESET}'


def config_create(config_class, extension):
    path = Path('tests', 'test_data', f'create_test.{extension}')
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
    config = config_class(path, CONFIG_ATTRS, create=True)
    assert isinstance(config.config, dict)
    assert isinstance(config.month, int)
    assert isinstance(config.payment, float)
    assert isinstance(config.transactions, list)
    assert len(config.config) == 3
