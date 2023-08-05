#!/usr/bin/env python3
import sys

from .args import Args
from .opener import open_links
from .prompts import user_choice, InvalidCmdPrompt, InputError
from .system import curl_links
from .sfeed import (
    format_feed_info,
    # filter_feed_info,
    get_feed_files,
    get_feed_info,
    get_feed_links,
    get_format_string,
    get_max_length,
    pick_feed_files,
)
from .user import User
from .utils import cprint


def show_list() -> int:
    """
    Show user their feed info. If they passed --with-opener open
    their file in the opener they passed. If user set always_open to
    True this will use their [video|browser|etc]_regex settings to
    open the chosen link in the program matching their regex
    """
    feed_files = get_feed_files()
    if Args.getBool("pick_feeds"):
        feed_files = pick_feed_files(feed_files)
    if feed_files == []:
        cprint("yellow", "WARN: No feeds found")
        return 1
    sort_time = User.settings_bool("sort_time")
    if not isinstance(sort_time, bool):
        cprint(
            "yellow",
            f"WARN: Setting 'sort_time' must be True or False: {sort_time}",
            sys.stderr,
        )
        sort_time = True
    feed_info = get_feed_info(feed_files, sort_time)
    format_string = get_format_string()
    max_length = get_max_length()
    formated_info = format_feed_info(
        feed_info,
        format_string,
        max_length,
    )
    try:
        choices = user_choice(formated_info, "Feed:")
    except (InvalidCmdPrompt, InputError) as err:
        cprint("red", f"ERROR: {err.message}", sys.stderr)
        return 1
    chosen_rows = [formated_info.index(choice) for choice in choices]
    raw_links = get_feed_links(feed_info, chosen_rows)
    links = curl_links(
        raw_links,
        User.get_stored("curl_file"),
        User.settings_str("temp_dir"),
    )
    open_links(links)
    return 0
