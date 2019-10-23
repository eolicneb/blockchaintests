# Elliptic curve y² = x³ + ax + b
#
# P + Q = R
# s = (Py - Qy)/(Px - Qx)
# Rx = s² -(Px + Qx)
# Ry = s(Px - Rx) - Py
#
# 2P = R
# s = (3Px² + a)/2Py
# Rx = s² - 2Px
# Ry = s(Px - Rx) - Py
#
# CURVE PARAMETERS
a = 2
b = 2
p = 17
G = (5, 1)

def modular_inv(n):
    n = n%p
    for m in range(1,p):
        if (m*n)%p == 1:
            return m
    return None

def add(P: tuple, Q: tuple) -> tuple:
    Px, Py = P
    Px, Py = Px%p, Py%p # (mod p)
    Qx, Qy = Q
    Qx, Qy = Qx%p, Qy%p # (mod p)
    s = (((Py-Qy)%p)*modular_inv(Px-Qx))%p
    # print("s:", s)
    Rx = int(((s*s)%p-(Px+Qx)%p)%p)
    Ry = int((s*(Px-Rx)-Py)%p)
    return Rx, Ry

for i in range(1,4*p):
    print(f"modular inversor of {i} (mod {p}): ", modular_inv(i))

def times2(P):
    Px, Py = P
    Px, Py = Px%p, Py%p
    s = (((3*Px*Px+a)%p)*modular_inv(2*Py))%p
    # print("s:", s, "(2Py)⁻¹(mod p):", modular_inv(2*Py))
    Rx = int(((s*s)%p-2*Px)%p)
    Ry = int((s*(Px-Rx)-Py)%p)
    return Rx, Ry

def times_k(k):
    if k == 1:
        return G
    Pub = times2(G)
    if k == 2:
        return Pub
    for i in range(2,k):
        Pub = add(Pub, G)
        # print("pub:", Pub)
    return Pub


for i in range(1,2*p):
    try:
        print(i, times_k(i))
    except:
        print(i, "O")
        break
