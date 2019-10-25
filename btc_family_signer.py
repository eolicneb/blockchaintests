import cryptos as cr
from cashaddress import convert
import argparse
import random
import json

# TODO Not working for Litecoin!!!

KEY_UPPER_LIMIT = int('0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140', 0)

def sign_message(message, coin, key=None, encoding='utf8'):

    # message = message.encode('utf8')

    coin_dispatcher = {'btc': cr.Bitcoin(),
                        'bch': cr.BitcoinCash(),
                        'ltc': cr.Litecoin()}

    client = coin_dispatcher[coin]

    # if no key provided, create one randomly
    if key is None:
        priv = random.randint(1, KEY_UPPER_LIMIT)
        pub = client.privtopub(priv)
        addr = client.privtoaddr(priv)
    else:
        try:
            priv = int(key)
            pub = client.privtopub(priv)
            addr = client.privtoaddr(priv)
        except:
            priv = cr.sha256(key)
            pub = client.privtopub(priv)
            addr = client.privtoaddr(priv)

    # sign message
    # if coin == 'ltc':
    #     signature = cr.litecoin_ecdsa_sign(message, priv)
    # else:
    #     signature = cr.ecdsa_sign(message, priv)
    signature = cr.bytes_ecdsa_sign(message, priv, coin, encoding)

    if coin == 'bch':
        addr = convert.to_cash_address(addr)

    # output
    output = {"address": addr,
            "signature": signature,
            "message": message,
            "private_key": priv,
            "public_key": pub,
            "coin": coin}

    return output


if __name__ == "__main__":
    import requests

    parser = argparse.ArgumentParser()
    parser.add_argument('--key', help='When provided, used to sign the given message and corresponded address is returned.')
    parser.add_argument('--message', help='Message to be signed.')
    parser.add_argument('--coin', default='btc', help='btc: bitcoin, bch: bitcoin cash, ltc: litecoin.')
    parser.add_argument('--encoding', default='utf8', help='Encoding with which the message is passed to bytes.')
    
    options = parser.parse_args()

    signed_dict = sign_message(options.message, options.coin, options.key, options.encoding)

    print(json.dumps(signed_dict))

    keys = ["message", "address", "signature"]

    server = "https://eundbca335wap08.azurewebsites.net"
    url = server+"/api/v1/"+options.coin+"/dsv"
    data = { key: signed_dict[key] for key in keys }
    r = requests.post(url=url, json=data)
    print("RPC-client validation:")
    print(r.json())
