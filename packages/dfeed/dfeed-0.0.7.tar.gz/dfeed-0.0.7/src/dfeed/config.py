#!/usr/bin/env python3
# import os
from loadconf import Config


def get_user_settings(program, args):
    # Create user object to read files and get settings
    user = Config(program=program)
    # Define some basic settings, files, etc.
    user_settings = {
        "debug": False,
        "sfeed_dir": "~/.sfeed/feeds",
        "field_length": 50,
        "format_list": "",
        "format_all": "{status} - {time:%Y-%m-%d %H:%M} - {feed_file} - {title:.51}",
        "new_indicator": "N",
        "new_time": 86400,
        "old_indicator": " ",
        "opener_delim": "\\=\\=",
        "prompt_cmd": "fzf",
        "prompt_args": "",
        "sort_time": True,
        "temp_dir": "/tmp/dfeed",
        "feed_length": 999,
    }
    config_files = {
        "conf_file": "dfeedrc",
        "curl_file": "curlrc",
        "openers": "openrc",
    }
    files = [
        "conf_file",
        "curl_file",
        "openers",
    ]
    settings = list(user_settings.keys())
    # Fill out user object
    user.define_settings(settings=user_settings)
    user.define_files(user_files=config_files)
    user.associate_settings(settings, "conf_file")
    user.create_files(create_files=files)
    user.create_template(["conf_file"])
    user.read_conf(user_settings=settings, read_files=["conf_file"])
    user.store_files(files=["openers", "curl_file"])

    return user, args
