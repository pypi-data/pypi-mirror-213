# python-pulsechain
Python implementation for PulseChain API



# PulseChain API Python Wrapper
This Python package provides a convenient wrapper for interacting with the PulseChain API. It is currently in the alpha stage, and the interface may change significantly as I continue to develop and improve the package.

**API Docs:** https://scan.pulsechain.com/api-docs

## Structure
The package contains three modules:

* transaction.py: Functions for interacting with transactions on the PulseChain network.
* token.py: Functions for interacting with tokens on the PulseChain network.
* account.py: Functions for interacting with accounts on the PulseChain network.

## Installation
You can install this package using pip:
    
    pip install python-pulsechain

## Usage
First, import the functions from the package:

    from pulsechain.account import get_balance, get_token_list

Then, you can use the functions to interact with the PulseChain API. For example, to get the balance of a particular address:

    balance = get_balance('your-address-here')
    print(balance)

To get the list of tokens owned by a particular address:


    token_list = get_token_list('your-address-here')
    print(token_list)

Functions return data from API without any modifications.

## Documentation
You can find more detailed documentation in the docstrings of each function in the package.

## Contributing
If you'd like to contribute to this package, please feel free to submit a pull request. Any improvements or bug fixes are welcome.

## Disclaimer
Please note that this package is currently in the alpha stage. This means that the code may change significantly as I continue to improve and develop the package. I appreciate your understanding and patience during this time.

# License
This project is licensed under the MIT License.