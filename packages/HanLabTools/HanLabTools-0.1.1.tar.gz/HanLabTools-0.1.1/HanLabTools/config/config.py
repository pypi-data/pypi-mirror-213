"""
Read Configuration File

The configuration file can reside in three different locations:

1) The package directory
2) The current working directory
3) The user's home directory

"""

from configparser import ConfigParser
from pathlib import Path
import warnings


def _get_config(configname="HanLab.cfg"):
    config = ConfigParser()

    # config = configparser.ConfigParser(
    #     converters={
    #         "list": lambda x: list(
    #             x.strip("(").strip("[").strip("]").strip(")").split(",")
    #         )
    #     }
    # )

    # Define three possible locations:
    HanLab_current_config = Path.cwd() / configname
    HanLab_home_config = Path.home() / configname

    cfg_folder = str(Path(__file__).parent)

    config_file_path = Path(cfg_folder) / configname
    config_read_list = [config_file_path, HanLab_home_config, HanLab_current_config]

    # User defined takes precedence
    config.read(config_read_list)

    configDict = config._sections

    return configDict


HanLab_CONFIG = _get_config()
