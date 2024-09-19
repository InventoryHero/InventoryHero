# utils/validation.py

import re
from typing import Union

import validators


def validate_email(email: str) -> bool:
    """
    Validate the email address using the validators package.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: Returns True if the email is valid, otherwise returns False.
    """
    return validators.email(email)



def validate_username(username: str) -> bool:
    """
    Validate the username according to specified rules.

    Args:
        username (str): The username to validate.

    Returns:
        bool or str: Returns True if the username is valid, otherwise returns an error message.
    """
    username_regex = r'^[a-zA-Z0-9._-]{3,25}$'
    if not re.match(username_regex, username):
        return False

    return True
