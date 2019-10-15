from ERC_20tokens import infura_rpc, parser
from pprint import pprint

rpc = infura_rpc.Infura_RPC()

print('Testing infura_api module:')

def test_get_last_block_number():
    print('\ntest "get_last_block_number":')
    lastblock = rpc.get_last_block_number()
    print(lastblock)

def test_get_nth_block():
    print('\ntest "get_nth_block":')
    block = rpc.get_nth_block(lastblock)
    print(block)
    print(f'block number: {lastblock}')

def test_get_nth_from_last_block():
    print('\ntest "get_nth_from_last_block":')
    midblocknum = rpc.hex2int(lastblock)//2
    block = rpc.get_nth_from_last_block(midblocknum)
    print(block)
    print(f'block number: {midblocknum}')

    print('\ntest if "get_nth_from_last_block(0) == get_nth_block(get_last_block_number)"')
    lastblock = rpc.get_last_block_number()
    block1 = rpc.get_nth_block(lastblock)
    block2 = rpc.get_nth_from_last_block(0)
    print(block1==block2)

def test_get_blocks():
    print('\ntest "get_blocks":')
    lastblock = rpc.hex2int(rpc.get_last_block_number())
    someblock = lastblock - 10
    numbers = range(someblock, lastblock)
    blocks = rpc.get_blocks(numbers)
    for block in blocks:
        print(block['number'], block['hash'])

def test_get_last_blocks():
    print('\ntest "get_last_blocks":')
    numbers = range(30, 40)
    blocks = rpc.get_blocks(numbers)
    for block in blocks:
        print(block['number'], block['hash'])

def test_get_transactions_from_blocks():
    print('\ntest "get_transactions_from_blocks":')
    blocks = rpc.get_last_blocks(range(30, 40))
    txs = rpc.get_transactions_from_blocks(blocks)
    for tx in txs:
        print(tx['blockNumber'], tx['transactionIndex'], tx['hash'])

def test_get_transaction_by_hash():
    print('\ntest "get_transaction_by_hash":')
    block = rpc.get_nth_from_last_block(0)
    tx_hash = block['transactions'][0]['hash']
    print('asking hash ', tx_hash)
    tx = rpc.get_transaction_by_hash(tx_hash)
    print(tx['blockNumber'], tx['transactionIndex'], tx['hash'])

def test_Parser_contructor_and_loader():
    print('\ntest "Parser.Contructor":')
    psr = parser.Parser(contracts_file="ERC-20_tokens.dat")
    print("token function in the parser:")
    pprint(psr.token_functions)
    print("contracts in the parser:")
    pprint(psr.contracts)

def test_parse_transactions():
    print('\ntest "Parser.parse_transactions()":')
    psr = parser.Parser(contracts_file="ERC-20_tokens.dat")
    blocks = rpc.get_last_blocks(range(1))
    txs = rpc.get_transactions_from_blocks(blocks)
    for tx in psr.parse_transactions(txs):
        pprint(tx)

def test_parse_transferFrom():
    print('\ntest "Parse.parse_transactions() with block 8358107,')
    print('which contains an ERC-20 contract transferFrom operation')
    psr = parser.Parser(contracts_file="ERC-20_tokens.dat")
    blocks = (rpc.get_nth_block(8358107),)
    txs = rpc.get_transactions_from_blocks(blocks)
    for tx in psr.parse_transactions(txs):
        pprint(tx)
