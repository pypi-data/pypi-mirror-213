"""
transaction.py

This module provides a Python interface for interacting
with transaction part of the PulseChain explorer API.
"""
from typing import Dict, Any

import requests

from pulsechain import API_URL
from pulsechain.utils import check_result


def get_transaction_info(txhash: str, index: int = None) -> Dict[str, Any]:
    """
    Fetch the transaction info.

    :param txhash: The hash of the transaction.
    :type txhash: str
    :param index: The log index for pagination.
    :type index: int, optional
    :return: A dictionary containing the response from the API.
    :rtype: Dict[str, Any]
    """
    params = {
        "module": "transaction",
        "action": "gettxinfo",
        "txhash": txhash,
    }

    if index is not None:
        params["index"] = index

    response = requests.get(API_URL, params=params, timeout=10)
    return check_result(response.json())


def get_transaction_receipt_status(txhash):
    """
    Fetch the receipt status of a given transaction on PulseChain.

    :param txhash: The transaction hash to fetch the receipt status for.
    :type txhash: str
    :return: A dictionary representing the JSON response from the API,
             which includes the transaction receipt status.
    :rtype: dict
    """
    base_url = 'https://scan.pulsechain.com/api'

    params = {
        'module': 'transaction',
        'action': 'gettxreceiptstatus',
        'txhash': txhash
    }

    response = requests.get(base_url, params=params, timeout=10)
    return check_result(response.json())
