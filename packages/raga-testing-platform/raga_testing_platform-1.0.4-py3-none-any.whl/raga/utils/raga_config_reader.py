import configparser
import os
from raga import RAGA_FILE

def read_raga_config():
    config_file_path = os.path.expanduser(os.path.join("~", RAGA_FILE))
    if not os.path.isfile(config_file_path):
        raise FileNotFoundError(f"Config file '{config_file_path}' not found.")

    config = configparser.ConfigParser()
    try:
        config.read(config_file_path)
    except configparser.Error as e:
        raise ValueError(f"Invalid config file format: {str(e)}")

    config_data = {}
    for section_name in config.sections():
        config_data[section_name] = dict(config.items(section_name))

    return config_data

def get_config_value(config_data, section, option):
    if section in config_data:
        section_data = config_data[section]
        if option in section_data:
            return section_data[option]
        else:
            raise KeyError(f"Option '{option}' not found in section '{section}'.")
    else:
        raise KeyError(f"Section '{section}' not found in config data.")
