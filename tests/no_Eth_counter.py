from ERC_20tokens import infura_rpc

rpc = infura_rpc.Infura_RPC()
n_blk = 3
while True:
    fst, lst, n_blk = 100*n_blk, 100*n_blk+100, n_blk + 1
    blocks = rpc.get_last_blocks(range(fst,lst))
    txs = rpc.get_transactions_from_blocks(blocks)
    cnt_noEth, cnt_txs = 0, 0
    for tx in txs:
        # print('value:',tx['value'])
        cnt_txs += 1
        if tx['input'] not in ['0x', '0x0', ''] \
                and tx['value'] in ['', '0', '0x', '0x0']:
                cnt_noEth += 1
    print(f'blocks {fst}-{lst}: {cnt_noEth/cnt_txs*100:.5f} % no Ether txs ({cnt_noEth} out of {cnt_txs})')