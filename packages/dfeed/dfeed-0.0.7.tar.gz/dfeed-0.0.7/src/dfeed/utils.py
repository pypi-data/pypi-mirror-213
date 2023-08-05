#!/usr/bin/env python3
# import json
# import pathlib
# import re
import sys

# import time
# import datetime
# from typing import Tuple, AnyStr, List, Dict, Any
from os.path import join as os_join

# from .system import curl_url, get_files


def cprint(color: str, string, out_file=sys.stdout):
    """
    Red: \033[31m
    Green: \033[32m
    Yellow: \033[33m
    Blue: \033[34m
    Magenta: \033[35m
    Cyan: \033[36m
    """
    format = ""
    end = "\033[0m"
    if color.lower() == "red":
        format = "\033[31m"
    elif color.lower() == "green":
        format = "\033[32m"
    elif color.lower() == "yellow":
        format = "\033[33m"
    elif color.lower() == "blue":
        format = "\033[34m"
    elif color.lower() == "magenta":
        format = "\033[35m"
    elif color.lower() == "cyan":
        format = "\033[36m"
    else:
        print(string, file=out_file)
        return
    print(format + string + end, file=out_file)


# def old_format_row(
#     row: List[str],
#     format_string: str,
#     max_length: int,
#     format_time: str,
# ) -> str:
#     ret_str = format_string
#     rep_list = [
#         "feed_file",
#         "time",
#         "title",
#         "link",
#         "content",
#         "content_type",
#         "id",
#         "author",
#         "enclosure",
#         "category",
#     ]
#     time_index = rep_list.index("time")
#     format_items = re.findall("{([^}]+)}", ret_str)
#     extra_regex = []
#     # find extra regex items for content
#     for item in format_items:
#         if item not in rep_list:
#             extra_regex.append(item)
#     # Replace each field with coresponding feed info
#     for rep_item in rep_list:
#         if rep_item not in format_items:
#             continue
#         row_string = row[rep_list.index(rep_item)]
#         if len(row_string) > max_length and not max_length < 0:
#             row_string = row_string[:max_length] + "..."
#         if rep_item == rep_list[time_index] and format_time != "":
#             row_string = time.strftime(format_time, time.localtime(float(row_string)))
#         # current_time = time.time()
#         # formatted_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(current_time))
#         # print(formatted_time)  # Output: 2023-04-12 09:27
#         ret_str = re.sub(
#             f"{{{rep_item}}}",
#             row_string,
#             ret_str,
#         )
#     # If any regex were given, use them to pull from feed content
#     # and replace them with the matching info
#     if extra_regex != []:
#         content_str = row[rep_list.index("content")]
#         for regex in extra_regex:
#             replace_match = re.search(regex, content_str)
#             if replace_match is None:
#                 ret_str = re.sub(
#                     f"{{{re.escape(regex)}}}",
#                     "",
#                     ret_str,
#                 )
#                 continue
#             if len(replace_match.group()) > max_length and max_length < 0:
#                 replace_str = replace_match.group()[:max_length] + "..."
#             else:
#                 replace_str = replace_match.group()
#             ret_str = re.sub(
#                 f"{{{re.escape(regex)}}}",
#                 replace_str,
#                 ret_str,
#             )
#     return ret_str


def key_value_list(dic, search_key=None):
    """
    Take a dicionary and return two lists one for keys and one for values
    """
    # While it is easiest if dic is a true dict
    # it need not be. As long as the items in dic
    # _are_ true dicts then we can make do
    def psuedo_dic():
        for item in dic:
            if isinstance(item, dict):
                true_dic(item)

    def true_dic(d=dic):
        if search_key is None:
            keys.extend(d.keys())
            values.extend(d.values())
        else:
            for key, value in d.items():
                if key == search_key:
                    keys.append(key)
                    values.append(value)

    keys = []
    values = []
    if isinstance(dic, dict):
        true_dic()
    else:
        psuedo_dic()

    return keys, values


def join(a, b):
    return os_join(a, b)


def pad_string(string: str):
    # convert input string to float, then back to string with 1 decimal place
    converted_string = "{:.1f}".format(float(string))
    # pad the string with zeros on the left to make it 3 characters long
    padded_string = converted_string.zfill(5)
    return padded_string
