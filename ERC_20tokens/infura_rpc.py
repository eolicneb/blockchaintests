import requests
from utils.hexstring import hex2int, int2hex

class Infura_RPC():
    nets = ('mainnet',
            'ropsten',
            'kovan',
            'rinkeby',
            'goerly')
    proj_id = '3ef7da9a92144381b0f426914b60b02c'
    proj_secret = 'd31f765890914197a0c228b4b7d1b7e3'
    def __init__(self, **kwargs):
        net = kwargs.get('net', self.nets[0])
        p_id = kwargs.get('project_id', self.proj_id)
        p_secret = kwargs.get('project_secret', self.proj_secret)
        self.conn_str = f'https://:{p_secret}@{net}.infura.io/v3/{p_id}'

    def ask(self, instruction, params=[]):
        """
        By means of this method every query can be bypassed to the API
        """
        headers = {"Content-Type": "application/json"}
        data = {"jsonrpc": "2.0",
                "id": 1,
                "method": instruction,
                "params": params}
        r = requests.post(self.conn_str, json=data, headers=headers).json()
        if 'error' in r and r['error']:
            print(r['error'])
            return None
        return r['result']

    def get_last_block_number(self):
        return self.ask('eth_blockNumber')

    def get_nth_block(self, n=0, complete=True):
        """
        Asks for that nth block and returns it inmediatly.
        If complete is False, only the hashes of the transactions
        are returned within the block.
        """
        if type(n) == int:
            n = int2hex(n)
        result = self.ask('eth_getBlockByNumber', params=[n, complete])
        return result

    def get_nth_from_last_block(self, n=0, complete=True):
        """
        Consults the ledger twice. First to get the number
        of the last block. Then, after computing the number
        of the nth-from-last block, it asks for that block
        and returns it inmediatly.
        If complete is False, only the hashes of the transactions
        are returned within the block.
        """
        lastblock = hex2int(self.get_last_block_number())
        blocknum = int2hex(lastblock - n)
        result = self.ask('eth_getBlockByNumber', params=[blocknum, complete])
        return result

    def get_blocks(self, numbers, complete=True):
        """
        Receives an iterable containing the needed 
        block numbers and yields the block one by one.
        """
        for n in numbers:
            yield self.get_nth_block(n, complete)

    def get_last_blocks(self, numbers, complete=True):
        """
        Receives an iterable containing the needed 
        block numbers and yields the block one by one.
        """
        for n in numbers:
            yield self.get_nth_from_last_block(n, complete)

    def get_transactions_from_blocks(self, blocks):
        """
        Generator to yield transactions out of
        the blocks iterator.
        """
        for block in blocks:
            for txs in block['transactions']:
                yield txs

    def get_transaction_by_hash(self, hash_):
        """
        Only needs the transaction's hash as parameter.
        """
        tx = self.ask('eth_getTransactionByHash', params=[hash_])
        return tx