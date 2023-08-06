import os
import configparser
from raga import RAGA_CONFIG_FILE
import sys

DEFAULT_CONFIG_VALUES = {
    "api_host": "https://example.com",
    "raga_access_key_id": "your-access-key",
    "raga_secret_access_key": "your-secret-key"
}

def read_raga_config():
    config_file_path = os.path.expanduser(os.path.join("~", RAGA_CONFIG_FILE))

    if not os.path.isfile(config_file_path):
        create_default_config(config_file_path)
        print("A default config file has been created. Please update the credentials in the config file.")
        sys.exit(0)

    config = configparser.ConfigParser()
    try:
        config.read(config_file_path)
    except configparser.Error as e:
        raise ValueError(f"Invalid config file format: {str(e)}")

    validate_default_section(config)

    config_data = {}
    for section_name in config.sections():
        config_data[section_name] = dict(config.items(section_name))

    return config_data

def create_default_config(config_file_path):
    config = configparser.ConfigParser()
    config.add_section("default")

    for option, value in DEFAULT_CONFIG_VALUES.items():
        config.set("default", option, value)

    os.makedirs(os.path.dirname(config_file_path), exist_ok=True)

    with open(config_file_path, "w") as config_file:
        config.write(config_file)

def validate_default_section(config):
    default_section = config["default"]

    for option, default_value in DEFAULT_CONFIG_VALUES.items():
        if option not in default_section or default_section[option] == default_value:
            raise ValueError(f"Please update the value of '{option}' in the [default] section of the config file.")

def get_config_value(config_data, section, option):
    if section in config_data:
        section_data = config_data[section]
        if option in section_data:
            return section_data[option]
        else:
            raise KeyError(f"Option '{option}' not found in section '{section}'.")
    else:
        raise KeyError(f"Section '{section}' not found in config data.")
