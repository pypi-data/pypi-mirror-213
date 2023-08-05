#!/usr/bin/env python3
from promptx import PromptX
from typing import List

from .user import User


class InvalidCmdPrompt(Exception):
    """Exception raised when user has invalid command prompt"""

    def __init__(self, error, message="ERROR: prompt_cmd not recognized"):
        self.error = error
        self.message = message

    def __str__(self):
        return f'{self.message} "{self.error}"'


class InputError(Exception):
    """Exception fzf or dmenu prompt fails"""

    def __init__(self, error, message="ERROR: Could not get user input", prefix=""):
        self.error = error
        self.prefix = prefix
        self.message = message

    def __str__(self):
        return f"{self.prefix}{self.message}{self.error}"


def user_choice(
    options: List[str],
    prompt: str,
):
    """
    Give user a prompt to choose from a list of options.  Uses dmenu, fzf, or
    rofi
    """
    p = PromptX(prompt_cmd=User.settings_str("prompt_cmd"))
    choice = p.ask(
        options=options,
        prompt=prompt,
        additional_args=User.settings_str("prompt_args"),
    )
    return choice
