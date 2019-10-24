from btc_family_signer import sign_message
from random import choice
import requests

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
print(encoding)

message = "最終的に唐滅亡時の混乱の中で貴族勢力は完全に瓦解した"

signed = sign_message(message, "btc", key="a", encoding=encoding)

print(signed)


keys = ["address", "signature"]
server = "https://eundbca335wap08.azurewebsites.net"
url = server+"/api/v1/btc/dsv"

for enc in encodings:
    data = { key: signed[key] for key in keys }
    try:
        utf8_message = message.encode(enc).decode('utf8')
        data["message"] = utf8_message

        r = requests.post(url=url, json=data)
        print(f"\nValidation with {enc}:")
        print(r.json()['validation'])
    except UnicodeDecodeError:
        print(f"\nValidation with {enc} failed.")