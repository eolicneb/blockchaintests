from btc_family_signer import sign_message
from random import choice
import requests
import cryptos as cr

encodings = ('utf8',
            'utf16',
            'utf32',
            'euc_jp',
            'euc_jis_2004',
            'euc_jisx0213',
            'iso2022_jp',
            'iso2022_jp_1',
            'iso2022_jp_2',
            'iso2022_jp_2004',
            'iso2022_jp_3',
            'iso2022_jp_ext',
            'shift_jis',
            'shift_jis_2004',
            'shift_jisx0213')

encoding = choice(encodings)
for encoding in encodings:
    print(encoding)

    message = "富田川のオオウナギ生息地とは、和歌山県南西部を流れる富田川の河口から、上流方向へ約18キロメートルまでの水域にわたる、国の天然記念物に指定されたオオウナギの生息地である"

    signed = sign_message(message, "btc", key="a", encoding=encoding)

    # print(signed)


    keys = ["address", "signature"]
    server = "https://eundbca335wap08.azurewebsites.net"
    url = server+"/api/v1/btc/dsv"

    results = []
    for enc in encodings:
        # Validation on RPC-client
        # data = { key: signed[key] for key in keys }
        # try:
        #     utf8_message = message.encode(enc).decode('utf8')
        #     data["message"] = utf8_message

        #     r = requests.post(url=url, json=data)
        #     print(f"\nValidation with {enc}:")
        #     print(r.json()['validation'])
        # except UnicodeDecodeError:
        #     print(f"\nValidation with {enc} failed.")

        # Validation on our own library
        result = cr.new_ecdsa_verify(message,
                                    signed['signature'],
                                    signed['address'],
                                    "btc",
                                    enc)
        results.append(result)
        # if result:
        #     print(f"\nValidation with {enc} at home.")
        #     print(result)

    print("final validation!")
    print(any(results))