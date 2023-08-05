"""
utils.py

This module provides helper functions.
"""
import requests


def add_decimal_sign(string: str, decimal_places: int = 18) -> str:
    """
    Insert a dot into a string at a specific position from the right.

    :param string: The string to insert the dot into.
    :type string: str
    :param decimal_places: The number of decimal places to separate from the right.
    :type decimal_places: int
    :return: The string with the dot inserted.
    :rtype: str
    """
    return string[:-decimal_places] + "." + string[-decimal_places:]


def check_result(response):
    """

    :param response: Response from the API to be checked.
    :return: Unwrapped result if the call was successful.
    """
    if response["message"] == "OK":
        return response["result"]
    raise requests.exceptions.RequestException(response["message"])
