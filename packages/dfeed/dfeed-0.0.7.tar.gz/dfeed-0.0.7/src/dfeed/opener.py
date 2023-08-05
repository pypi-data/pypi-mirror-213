#!/usr/bin/env python3
import re
import shlex

# import subprocess
from typing import List
from .system import open_process
from .user import User
from .utils import cprint


def open_links(links: List[str]) -> None:
    """
    Loop over openers,
       for each opener get links matching regex
       open those links with the opener
    """
    opener_delim = User.settings_str("opener_delim")
    for opener_line in User.get_stored("openers"):
        line_parts = opener_line.split(opener_delim, 1)
        if len(line_parts) != 2:
            cprint(
                "yellow",
                f"WARNING: malformed openrc on line {User.get_stored('openers').index(opener_line) + 1}",
            )
            continue
        opener_regex = line_parts[0].rstrip()
        cmd_line = line_parts[1].strip()
        opener_list = shlex.split(cmd_line)
        starting_len = len(opener_list)
        pop_links = set()
        for link in links:
            link_match = re.search(opener_regex, link)
            if link_match is None:
                continue
            opener_list.append(link)
            pop_links.add(link)
        if len(opener_list) == starting_len:
            continue
        links = [x for x in links if x not in pop_links]
        open_process(opener_list)
