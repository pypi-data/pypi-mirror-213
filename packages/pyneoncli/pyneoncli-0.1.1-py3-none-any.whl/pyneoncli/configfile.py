import os
from configparser import ConfigParser
from pathlib import Path


class ConfigFileDefaults:

    def __init__(self):
        self._home = str(Path.home())
        self._home_config_file = Path(f"{self._home}/neoncli.conf")
        self._cwd_config_file = Path(f"{os.getcwd()}/neoncli.conf")

    @property
    def config_file_list(self):
        return [str(self._home_config_file), str(self._cwd_config_file)]


class NeonConfigFile:

    def __init__(self):
        self._cfg_paths = ConfigFileDefaults()
        cfg = ConfigParser()
        cfg.read(self._cfg_paths.config_file_list)

        env_api_key = os.getenv("NEON_API_KEY")

        self._default_project_id = cfg['DEFAULT']['project_id'] \
            if 'DEFAULT' in cfg and 'project_id' in cfg['DEFAULT'] else None
        self._api_key = cfg['DEFAULT']['api_key'] \
            if 'DEFAULT' in cfg and 'api_key' in cfg['DEFAULT'] else env_api_key

    @property
    def api_key(self):
        return self._api_key

    @property
    def default_project_id(self):
        return self._default_project_id


