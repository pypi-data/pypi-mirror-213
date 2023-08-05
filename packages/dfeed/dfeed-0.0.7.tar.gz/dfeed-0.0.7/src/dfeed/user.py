#!/usr/bin/env python3
import pathlib
from typing import Dict, List


class User:
    _config_dir = ""
    _settings_dict = {}
    _stored_dict = {}
    _files_dict = {}

    @classmethod
    def define_user(cls, user):
        cls._set_config_dir(user.config_dir)
        cls._set_settings(user.settings)
        cls._set_files(user.files)
        cls._set_stored(user.stored)

    @classmethod
    def get_config_dir(cls) -> str:
        return cls._config_dir

    @classmethod
    def get_dir(cls, dir: str) -> pathlib.Path:
        return pathlib.Path(f"{cls._config_dir}/{dir}")

    @classmethod
    def get_files(cls, key: str) -> str:
        return cls._files_dict[key]

    @classmethod
    def get_files_dict(cls) -> Dict[str, str]:
        return cls._files_dict

    @classmethod
    def settings_bool(cls, key: str) -> bool:
        return cls._settings_dict[key]

    @classmethod
    def settings_int(cls, key: str) -> int:
        return cls._settings_dict[key]

    @classmethod
    def settings_str(cls, key: str) -> str:
        return cls._settings_dict[key]

    @classmethod
    def get_settings_dict(cls) -> Dict[str, int | bool | str]:
        return cls._settings_dict

    @classmethod
    def get_stored(cls, key: str) -> List[str]:
        return cls._stored_dict[key]

    @classmethod
    def get_stored_dict(cls) -> Dict[str, List[str]]:
        return cls._stored_dict

    @classmethod
    def _set_config_dir(cls, config_dir):
        cls._config_dir = config_dir

    @classmethod
    def _set_files(cls, files_dict):
        for key, val in files_dict.items():
            cls._files_dict[key] = val

    @classmethod
    def _set_settings(cls, settings_dict):
        for key, val in settings_dict.items():
            cls._settings_dict[key] = val

    @classmethod
    def _set_stored(cls, stored_dict):
        for key, val in stored_dict.items():
            cls._stored_dict[key] = val
