# src\config\config.py

import json

from pathlib import Path


class Configuration:

    __instance = None

    @staticmethod
    def get_instance():
        if not Configuration.__instance:
            Configuration.__instance = Configuration()
        return Configuration.__instance

    def __init__(self) -> None:
        super().__init__()

        self.__config_path = Path(f".config.json")
        # Define configuration dictionary
        self.__data = {
            "audio-bitrate": 192,    # Default audio bitrate in kbps
            "video-bitrate": 10000,  # Default video bitrate in kbps
        }

        self.load()

    def __repr__(self) -> str:
        return repr(self.__data)

    def __str__(self) -> str:
        return str(self.__data)

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __delitem__(self, key):
        del self.__data[key]

    def __contains__(self, key):
        return key in self.__data

    def __len__(self):
        return len(self.__data)

    def clear(self):
        self.__data.clear()
        self.load()

    def update(self, new: dict):
        self.__data.update(new)

    def load(self):
        """Load app configuration file"""
        if self.__config_path.exists():
            self.__data.update(json.loads(self.__config_path.read_text()))

    def save(self):
        """Save app configuration file"""
        self.__config_path.write_text(json.dumps(self.__data))
