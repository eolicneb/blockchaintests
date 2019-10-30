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
n = 18

p = (2**128-3)//76439
a = int('0xDB7C2ABF62E35E668076BEAD2088', 0)
b = int('0x659EF8BA043916EEDE8911702B22', 0)
G = (int('0x09487239995A5EE76B55F9C2F098', 0),
     int('0xA89CE5AF8724C0A23E0E0FF77500', 0))
n = int('0xDB7C2ABF62E35E7628DFAC6561C5', 0)

print('p ', p)
print('a ', a)
print('b ', b)
print('Gx ', G[0])
print('Gy ', G[1])
print('n ', n)

# n = 10

def modular_inv(n):
    n = n%p
    for m in range(1,p):
        if (m*n)%p == 1:
            return m
    return None

def mod_mult_inv_(n, p=p):
    a, b = p, n%p
    if a == b:
        return None
    rs, qs = [a, b], []
    while rs[-1] != 0:
        qs.append(rs[-2]//rs[-1])
        rs.append(rs[-2] - qs[-1]*rs[-1])    
    x, y = 1, -(-1)**len(qs)
    for ix in range(len(qs), 0, -1):
        x, y = x*qs[ix-1] + y, x
    return x%p

def mod_mult_inv(n, p=p):
    a, b = p, n%p
    if 0 == b:
        return None
    qs = []
    while b != 0:
        qs[:0] = [a//b]
        a, b = b, a-qs[0]*b
    x, y = 1, 1
    for q in qs:
        x, y = -x*q + y, x
    return x%p

def add(P: tuple, Q: tuple) -> tuple:
    Px, Py = P
    Px, Py = Px%p, Py%p # (mod p)
    Qx, Qy = Q
    Qx, Qy = Qx%p, Qy%p # (mod p)
    try:
        s = (((Py-Qy)%p)*mod_mult_inv(Px-Qx))%p
    except:
        return None
    # print("s:", s)
    Rx = int(((s*s)%p-(Px+Qx)%p)%p)
    Ry = int((s*(Px-Rx)-Py)%p)
    return Rx, Ry

# for i in range(1,p+5):
#     print(f"modular inversor of {i} (mod {p}): ", modular_inv(i), mod_mult_inv(i), mod_mult_inv_(i))

def times2(P):
    Px, Py = P
    Px, Py = Px%p, Py%p
    s = (((3*Px*Px+a)%p)*mod_mult_inv(2*Py))%p
    # print("s:", s, "(2Py)⁻¹(mod p):", mod_mult_inv(2*Py))
    Rx = int(((s*s)%p-2*Px)%p)
    Ry = int((s*(Px-Rx)-Py)%p)
    return Rx, Ry

from math import log2
limit_pow = int(log2(n))+1
G2s = [G]
for i in range(1, limit_pow):
    G2s.append(times2(G2s[-1]))
    # print(i, 2**i, G2s[-1])

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

def fast_times(number):
    if number < 1 or number >= n:
        return None
    m, i, adding = number, 0, []
    while m:
        if m & 1:
            adding.append(G2s[i])
        m >>= 1
        i += 1
    Q = adding.pop()
    while adding:
        Q = add(Q, adding.pop())
    return Q

from time import time

REPEAT = 3
OFFSET = n-10000000
RANGO = (OFFSET, OFFSET+REPEAT)

s = time()
for number in range(*RANGO):
    Q = fast_times(number)
    print(number, Q)

print((time()-s)/REPEAT)

# s = time()
# for _ in range(REPEAT):
#     for i in range(*RANGO):
#         Q = times_k(i)
#         print(i, Q)
# print(time()-s)