from cryptos import *
from pprint import pprint
import threading
from time import time
from random import randint, shuffle

def get_tx(n, txid, reg_list, currency):
    try:
        reg_list[n] = currency.fetchtx(txid)
    except Exception:
        reg_list[n] = {'error': 'direccion no valida.'}

with open('txid_list.txt','r') as tl:
    txid_list = tl.read().split('\n')

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
                        txid_list[randint(0,len(txid_list)-1)],
                        li,
                        c))
    th.start()
# pprint(li)
# print(inputs)

p_thread = threading.main_thread()
for th in threading.enumerate():
    if th is not p_thread:
        th.join()
t_end = (time()-t_ini)/N
for n, l in enumerate(li):
    print(n,':')
    pprint(l)
print(t_end)
