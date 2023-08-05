"""
token.py

This module provides a Python interface for interacting
with transaction part of the PulseChain explorer API.
"""
from typing import Dict, Any

import requests

from pulsechain import API_URL
from pulsechain.utils import check_result


def get_token(contract_address: str) -> Dict[str, Any]:
    """
    Fetch the ERC-20 or ERC-721 token by contract address.

    :param contract_address: The contract address to fetch the token for.
    :type contract_address: str
    :return: A dictionary containing the response from the API.
    :rtype: Dict[str, Any]
    """
    params = {
        "module": "token",
        "action": "getToken",
        "contractaddress": contract_address,
    }

    response = requests.get(API_URL, params=params, timeout=10)
    return check_result(response.json())


def get_token_holders(
    contract_address: str, page: int = 1, offset: int = 10
) -> Dict[str, Any]:
    """
    Fetch the token holders by contract address.

    :param contract_address: The contract address to fetch the token holders for.
    :type contract_address: str
    :param page: The page number for pagination.
    :type page: int, optional
    :param offset: The maximum number of records to return for pagination.
    :type offset: int, optional
    :return: A dictionary containing the response from the API.
    :rtype: Dict[str, Any]
    """
    params = {
        "module": "token",
        "action": "getTokenHolders",
        "contractaddress": contract_address,
        "page": page,
        "offset": offset,
    }

    response = requests.get(API_URL, params=params, timeout=10)
    return check_result(response.json())
