"""
account.py

This module provides a Python interface for interacting
with account part of the PulseChain explorer API.
"""
from typing import Dict, Any, List

import requests

from pulsechain import API_URL
from pulsechain.utils import check_result


# pylint: disable=too-many-arguments
def get_eth_balance(address: str) -> Dict[str, Any]:
    """
    Fetch the Ethereum balance for a given address.

    :param address: The address to fetch the Ethereum balance for.
    :type address: str
    :return: A dictionary containing the response from the API.
    :rtype: Dict[str, Any]
    """
    params = {"module": "account", "action": "eth_get_balance", "address": address}
    response = requests.get(API_URL, params=params, timeout=10)
    return check_result(response.json())


def get_balance(address: str) -> Dict[str, Any]:
    """
    Fetch the balance for a given address.

    :param address: The address to fetch the balance for.
    :type address: str
    :return: A dictionary containing the response from the API.
    :rtype: Dict[str, Any]
    """
    params = {"module": "account", "action": "balance", "address": address}
    response = requests.get(API_URL, params=params, timeout=10)
    return check_result(response.json())


def get_balances_multi(addresses: List[str]) -> Dict[str, Any]:
    """
    Fetch the balances for multiple addresses.

    :param addresses: The list of addresses to fetch the balances for. Maximum of 20 addresses.
    :type addresses: List[str]
    :return: A dictionary containing the response from the API.
    :rtype: Dict[str, Any]
    :raises ValueError: If more than 20 addresses are provided.
    """
    if len(addresses) > 20:
        raise ValueError("Maximum of 20 addresses can be queried at once.")

    params = {
        "module": "account",
        "action": "balancemulti",
        "address": ",".join(addresses),
    }
    response = requests.get(API_URL, params=params, timeout=10)
    return check_result(response.json())


def get_pending_transactions(
        address: str, page: int = None, offset: int = None
) -> Dict[str, Any]:
    """
    Fetch the pending transactions for a given address.

    :param address: The address to fetch the pending transactions for.
    :type address: str
    :param page: The page number to be used for pagination.
    :type page: int, optional
    :param offset: The maximum number of records to return when paginating.
    :type offset: int, optional
    :return: A dictionary containing the response from the API.
    :rtype: Dict[str, Any]
    :raises ValueError: If either 'page' or 'offset' is provided, but not both.
    """
    if (page is None and offset is not None) or (page is not None and offset is None):
        raise ValueError("Both 'page' and 'offset' must be provided for pagination.")

    params = {"module": "account", "action": "pendingtxlist", "address": address}

    if page is not None and offset is not None:
        params.update({"page": page, "offset": offset})

    response = requests.get(API_URL, params=params, timeout=10)
    return check_result(response.json())


def get_transactions(address, sort=None, start_block=None, end_block=None, page=None, offset=None, filter_by=None,
                     start_timestamp=None, end_timestamp=None):
    """
    Fetches a list of transactions for a given address from the PulseChain API.

    :param address: A 160-bit code used for identifying Accounts. (required)
    :type address: str
    :param sort: A string representing the order by block number direction. Defaults to descending order.
                 Available values: asc, desc
    :type sort: str, optional
    :param start_block: A nonnegative integer that represents the starting block number.
    :type start_block: int, optional
    :param end_block: A nonnegative integer that represents the ending block number.
    :type end_block: int, optional
    :param page: A nonnegative integer that represents the page number to be used for pagination. '
                 offset' must be provided in conjunction.
    :type page: int, optional
    :param offset: A nonnegative integer that represents the maximum number of records to return when paginating.
                   'page' must be provided in conjunction.
    :type offset: int, optional
    :param filter_by: A string representing the field to filter by. If none is given it returns transactions
                      that match to, from, or contract address. Available values: to, from
    :type filter_by: str, optional
    :param start_timestamp: Represents the starting block timestamp.
    :type start_timestamp: int, optional
    :param end_timestamp: Represents the ending block timestamp.
    :type end_timestamp: int, optional

    :return: JSON response from the API call.
    :rtype: dict
    """

    if not address:
        raise ValueError("The 'address' parameter is required")

    if sort and sort not in ['asc', 'desc']:
        raise ValueError("The 'sort' parameter must be either 'asc' or 'desc'")

    if start_block is not None and start_block < 0:
        raise ValueError("The 'start_block' parameter must be a nonnegative integer")

    if end_block is not None and end_block < 0:
        raise ValueError("The 'end_block' parameter must be a nonnegative integer")

    if page is not None and page < 0:
        raise ValueError("The 'page' parameter must be a nonnegative integer")

    if offset is not None and offset < 0:
        raise ValueError("The 'offset' parameter must be a nonnegative integer")

    if filter_by and filter_by not in ['to', 'from']:
        raise ValueError("The 'filter_by' parameter must be either 'to', 'from', or None")

    if start_timestamp is not None and start_timestamp < 0:
        raise ValueError("The 'start_timestamp' parameter must be a nonnegative integer")

    if end_timestamp is not None and end_timestamp < 0:
        raise ValueError("The 'end_timestamp' parameter must be a nonnegative integer")

    params = {
        'module': 'account',
        'action': 'txlist',
        'address': address,
        'sort': sort,
        'start_block': start_block,
        'end_block': end_block,
        'page': page,
        'offset': offset,
        'filter_by': filter_by,
        'start_timestamp': start_timestamp,
        'end_timestamp': end_timestamp
    }
    response = requests.get(API_URL, params=params, timeout=10)
    return check_result(response.json())


def get_token_list(address):
    """
    Fetch the list of tokens owned by a given address on PulseChain.

    :param address: The PulseChain address to fetch the tokens for.
    :type address: str
    :return: A dictionary representing the JSON response from the API,
             which includes a list of owned tokens.
    :rtype: Dict[str, Any]
    """
    params = {"module": "account", "action": "tokenlist", "address": address}

    # Make the API request and get the response
    response = requests.get(API_URL, params=params, timeout=10)
    return check_result(response.json())


def get_token_balance(contract_address: str, address: str) -> Dict[str, Any]:
    """
    Fetch the token balance for a given address and contract.

    :param contract_address: The contract address of the token.
    :type contract_address: str
    :param address: The address to fetch the token balance for.
    :type address: str
    :return: A dictionary containing the response from the API.
    :rtype: Dict[str, Any]
    """
    params = {
        "module": "account",
        "action": "tokenbalance",
        "contractaddress": contract_address,
        "address": address,
    }
    response = requests.get(API_URL, params=params, timeout=10)
    return check_result(response.json())
