#!/usr/bin/env python3
import shlex
import sys

from .args import Args
from .config import get_user_settings
from .options import get_opts
from .sfeed import get_feed_files
from .system import open_process
from .user import User
from .utils import cprint
from .list_feed import show_list


__license__ = "GPL-v3.0"
__program__ = "dfeed"


def process_opts():
    """
    Opts handler for main
    """
    return show_list()


def main():
    """
    Command line application to integrate dmenu into sfeed
    """
    # Set and get command line args
    args = get_opts(__program__)

    # Creates a UserSettings object. This will be used by various function
    # to access file paths, settings, filters, and command line args
    user, args = get_user_settings(program=__program__, args=args)

    User.define_user(user)
    Args.define_args(args)
    # Execute the appropriate function based on command line options
    return process_opts()


if __name__ == "__main__":
    sys.exit(main())
