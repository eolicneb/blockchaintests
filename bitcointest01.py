from cryptos import *
from pprint import pprint
import threading
from time import time

def get_tx(n, txid, reg_list, currency):
    reg_list[n] = currency.fetchtx(txid)

c = Bitcoin()
# priv = sha256('a big long brainwallet password')
# pub = c.privtopub(priv)
# addr = c.pubtoaddr(pub)
t_ini = time()
N = 1000
li = [ '' for _ in range(N) ]
for n in range(N):
    th = threading.Thread(target=get_tx,
                        args=(n,
                        "4e77a5b181d3027bed2924dc06d63d204405533ff41f3b33e834e12ac4856fd8",
                        li,
                        c))
    th.start()
# pprint(li)
# print(inputs)

p_thread = threading.main_thread()
for th in threading.enumerate():
    if th is not p_thread:
        th.join()
print(li)
print((time()-t_ini)/N)
