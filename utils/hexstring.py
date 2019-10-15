
def hex2int(hex_):
    if hex_[:2] != '0x':
        hex_ = '0x'+hex_
    return int(hex_, base=0)

def int2hex(int_):
    return hex(int_)