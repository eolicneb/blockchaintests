#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
"""eth_signer.py

Generate signature as in EIP-191 "version ``E``
from Ethereum specs when private key and a message
are provided by -key and -message parameters.

usage: $> python eth_signer.py -key <private-key> 
                          -message <message-to-be-signed>

return: {
            'address' : '<address-derived-from-private-key>',
            'signature' : '<signature-for-given-message>',
            'message' : '<message-to-be-signed>'
         }

When imported as a module, the file provides the method
get_singature(message: str, key: str) -> dict

"""


from eth_account.messages import encode_defunct
from eth_account.account import Account

def get_signature(message: str, key: str) -> dict:
    """ 
    Returns the signature of the given
    message when signed using the reveived
    key as the private key.

    :param message: string
    :param key: string
    :return: dict

        The key param will be interpreted as
        a hex string if possible. In that way,
        if an existing private key is received
        in hex form, the returned signature would
        be the same as if signed from the original
        wallet possesing that key.
        Otherwise a 32 bytes private key will be
        formed by adding leading null-bytes to
        the bytes of the received string.

    """
    try:
        key = bytes.fromhex(key)
    except ValueError:
        key = bytes(key, 'utf-8')
    key = (b'\00'*32+key)[-32:]
    acc = Account.from_key(key)

    # the received message is encoded as in EIP-191 "version ``E``"
    encoded = encode_defunct(text=message)

    signed = acc.sign_message(encoded)['signature'].hex()
    return {"address":acc.address,"signature":signed,"message":message}

def __main__():
    """ 

    """
    import argparse
    from pprint import pprint
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument('--key', type=str, help='Private key. Should have 32 bytes, but if smaller will be zero left-padded.')
    parser.add_argument('--message', type=str, help='String to be signed.')
    parser.add_argument('--coin', type=str, help='Cryptocurrency.')

    args = parser.parse_args()

    key, message = args.key, args.message
    print(json.dumps(get_signature(message, key)))

if __name__ == "__main__":
    __main__()