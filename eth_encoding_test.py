from eth_keys import KeyAPI, keys
from eth_utils import keccak

enc = 'utf8'
message = "2017年の骨学的分析とDNA検査によって女性であることが判明している"

pk = keys.PrivateKey(b'\01'*32)
addr = str(pk.public_key.to_checksum_address())

msg_bytes = message.encode(enc)
msg_length = str(len(msg_bytes)).encode(enc)
msg = b'\x19Ethereum Signed Message:\n'+msg_length+msg_bytes

signature = pk.sign_msg(msg).to_hex()
print(message)
print(addr)
print(signature)

print('\nChecking Stage:')
key_obj = KeyAPI()

if '0x' in signature:
    signature = signature[2:]
sign = KeyAPI.Signature(bytearray.fromhex(signature))

pub = key_obj.ecdsa_recover(message_hash=keccak(msg), signature=sign)
print(addr == str(pub.to_checksum_address()))