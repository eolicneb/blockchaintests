""" INFURA testing

INFURA is an Ethereum API that allows making consults to the
Ethereum blockchain without need to download any ledger.

It can query to five different nets:
MAINNET mainnet.infura.io/v3/PROJECT_ID
ROPSTEN ropsten.infura.io/v3/PROJECT_ID
KOVAN kovan.infura.io/v3/PROJECT_ID
RINKEBY rinkeby.infura.io/v3/PROJECT_ID
GÖRLY goerli.infura.io/v3/PROJECT_ID

I've made my own account with theese parameters:
PROJECT_ID 3ef7da9a92144381b0f426914b60b02c
PROJECT_SECRET d31f765890914197a0c228b4b7d1b7e3

"""
import requests
from pprint import pprint
import json


class InfuraAPI():

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

class Analisys():
    """
    Perform different analytics upon the blockchain's data
    """
    def __init__(self, **kwargs):
         # This is the client instance to consult the ledger
        self.net = InfuraAPI(**kwargs)

        self.token_functions = {}
        self.contracts = self.load_contracts(kwargs.get('contracts_file',''))

    def last_block_number(self):
        result = self.net.ask('eth_blockNumber')
        return result

    def nth_from_last_block(self, n=0, complete=True):
        """
        Consults the ledger twice. First to get the number
        of the last block. Then, after computing the number
        of the nth-from-last block, it asks for that block
        and returns it inmediatly.
        If complete is False, only the hashes of the transactions
        are returned within the block.
        """
        blocknum = f'0x{int(self.last_block_number(), base=0)-n:02x}'
        result = self.net.ask('eth_getBlockByNumber', params=[blocknum, complete])
        return result

    def last_n_blocks(self, n=1, complete=True):
        return (self.nth_from_last_block(n=i, complete=complete) for i in range(n))

    def get_transactions_from_blocks(self, blocks):
        """
        Generator to yield transactions out of
        the blocks iterator.
        """
        for block in blocks:
            for txs in block['transactions']:
                yield txs

    def get_inputs_from_blocks(self, blocks):
        """
        This generator returns only those transactions that
        have not null 'input' field.
        """
        for tx in self.get_transactions_from_blocks(blocks):
            if tx['input'] not in ['','0x', '0x0']:    # Consider only non empty 'inputs'
                if tx['input'][:10] not in self.token_functions:
                    self.token_functions[tx['input'][:10]] = {tx['to']: 1}
                else:
                    if tx['to'] in self.token_functions[tx['input'][:10]]:
                        self.token_functions[tx['input'][:10]][tx['to']] += 1
                    else:
                        self.token_functions[tx['input'][:10]][tx['to']] = 1
                yield tx

    def save_transfers(self, file_):
        keep = [(count, addr) for addr, count in self.token_functions['0xa9059cbb'].items()]
        keep.sort(reverse=True)
        with open(file_, 'w') as f:
            f.write('{\n')
            for contract in keep:
                f.write(f"\"{contract[1]}\": {json.dumps({'count': contract[0], 'name': '', 'symbol': '', 'decimals': 0})}, \n")
            f.write('}')

    def load_contracts(self, file_):
        if file_:
            with open(file_, 'r') as f:
                return json.load(f)

    def check_transfers(self, transactions):
        """
        Returns a generator out of the iterable transactions.
        Each yield is a transfer operation identified by the
        first 8 bytes in the 'input' field.
        """
        for tx in transactions:
            if tx['input'][2:10] == 'a9059cbb':
                if tx['to'] in self.contracts:
                    contract = self.contracts[tx['to']]
                else:
                    contract = {'name': 'unnkown', 'decimals': 0}
                i = tx['input']
                value, name = int('0x'+i[74:], base=0) / 10**contract['decimals'], contract['name']
                transfer = {'tx': tx['hash'], 
                            'token': name, 
                            'to': '0x'+i[34:74], 
                            'value': value, 
                            'from': tx['from']}
                yield transfer

    def look_for(self, transactions, ouput_file):
        """
        Given an iterable of transactions, when the length of
        the 'input' field is exactly 202 = 2+8+3*64 and the
        'to' field is a registered contract address, features
        from the transaction are recorded in the output_file.
        """
        for tx in transactions:
            if len(tx['input']) == 202 and tx['to'] in self.contracts:
                name = self.contracts[tx['to']]['name'] or tx['to']
                finding = (tx['input'][2:10], name, tx['hash'], tx['blockNumber'], tx['input'])
                with open(ouput_file, 'a') as f:
                    f.write(', '.join(finding)+'\n')
    
    def search(self, transactions):
        """
        Given an iterable of transactions, this method stacks
        them according to the length of the 'input' field.
        """
        instructions = {}
        for tx in transactions:
            l, hash_, inst = len(tx['input']), f'"{tx["hash"]}"in"{tx["blockNumber"]}"to"{tx["to"]}"', tx['input'][2:10]
            if l not in instructions:
                instructions[l] = [(inst, hash_)]
            else:
                instructions[l].append((inst, hash_))
            for val in instructions.values():
                val.sort()
        return instructions





if __name__ == "__main__":
    # net = InfuraAPI()
    # addr = "0x839137072d1e0120860edcf1ec7d90562a0610eed70c123e4c47a00b9c763587"
    # res = net.ask('eth_blockNumber')
    # res = net.ask('eth_getBlockByHash', params=[addr, True])
    # inp = [ ((tx['input'], tx['to']), tx['hash'], tx['blockNumber']) for tx in res['transactions'] if not tx['input'] == '0x' ]
    # opers = [(i[0][1], '0x'+i[0][0][34:74], int('0x'+i[0][0][74:], base=0)) for i in inp if i[0][0][:10] == '0xa9059cbb']
    # opers.sort()
    # for oper in opers:
    #     print(oper)
    print('Analisys')
    ana = Analisys(contracts_file='ERC-20_tokens.dat')
    # blocks = ana.last_n_blocks(n=3)
    blocks = (ana.nth_from_last_block(n+1, True) for n in range(1000))
    txs = ana.get_inputs_from_blocks(blocks)
    # cont = ana.check_transfers(txs)
    # pprint(ana.search(txs))
    # for c in search:
    #     pprint(c)
    # pprint(ana.contracts)
    # ana.save_transfers('ERC-20_tokens.dat')
    ana.look_for(txs, '3_params_functions.txt')