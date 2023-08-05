#!/usr/bin/env python3
import argparse


def get_opts(prog_name="dfeed"):
    parser = argparse.ArgumentParser(
        allow_abbrev=False,
        description="""dmenu + sfeed""",
        formatter_class=argparse.RawTextHelpFormatter,
        prog=prog_name,
    )
    # group = parser.add_mutually_exclusive_group()
    #     group.add_argument(
    #         "-l",
    #         "--list",
    #         action="store_true",
    #         help="""
    # List feeds. Will display feeds based on your configuration.
    #         """,
    #     )
    parser.add_argument(
        "-f",
        "--feed",
        metavar="FEED",
        action="store",
        help="""
The FEED to use for other flags such as --list.
A FEED may be a comma seperated list of feed files like so:
\tsome_rss_feed,feed2,etc.
If the given file is not an actual feed file, it may be a file
in:
\t$XDG_CONFIG_HOME/dfeed/feed_filters
The file may be a list of feed files seperated by new lines like so:
\tsome_rss_feed
\tfeed2
\tetc.
        """,
    )
    parser.add_argument(
        "-F",
        "--format",
        metavar="FORMAT_STRING",
        action="store",
        help="""
Use FORMAT_STRING to format output of commands like --list.
FORMAT_STRING has the following keys:
\tstatus,        # uses new_indicator when feed is more recent
\t               # than current time + new_time
\t               # uses old_indicator otherwise
\tfeed_file,     # name of feed_file in sfeed_dir/feeds
\t# the remaining keys should explain themselves
\t# if you have questions look at a feed file.
\t# The following keys follow the tab seperated values.
\ttime,
\ttitle,
\tlink,
\tcontent,
\tcontent_type,
\tid,
\tauthor,
\tenclosure,
\tcategory
Not all fields are present for every feed. Any field not found in a feed
file will be removed form the format string.
Default example:
\t"{status} - {time:%%Y-%%m-%%d %%H:%%M} - {feed_file:<12} - {title:.51}"
        """,
    )
    parser.add_argument(
        "-i",
        "--invert",
        action="store_true",
        help="Invert the behavior of the --apply-filter flag",
    )
    parser.add_argument(
        "-p",
        "--pick-feeds",
        action="store_true",
        help="Get a prompt to choose from the feeds in your sfeed_dir.",
    )
    parser.add_argument(
        "-P",
        "--pick-filters",
        action="store_true",
        help="Get a prompt to choose from the filters in your dfeed/feed_filters directory.",
    )
    parser.add_argument(
        "-o",
        "--filter-output",
        metavar="FILTER_FILES",
        action="store",
        help="""
Use the files listed in FILTER_FILES to filter the output of dfeed.
This is a comma seperated list of files like so:
\tfilter_file1,/some/absolute/path,filter_file2
If the file is relative it is assumed to exist in the key_filters
directory of your configuration directory. On Linux this would be
\t$XDG_CONFIG_HOME/dfeed/key_filters
The makeup of a FILTER_FILE looks like this:
\tKEY = REGEX
\ttitle = \\([tT]op ten\\)
Any KEY matching the REGEX will be filtered. Use the --invert flag to
change this behavior.
        """,
    )
    args = parser.parse_args()
    return args
