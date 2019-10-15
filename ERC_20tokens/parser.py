import json
from utils.hexstring import hex2int

class Parser():
    """
    Parser class will create an object containing information
    about the known ERC-20 tokens, their contract addresses, 
    names and decimals, and the supported token functions 
    (like 'transfer' and 'transferFrom').
    """
    token_functions = {
            '0x23b872dd': {'name': 'transferFrom(address _from, address _to, uint256 _value)',
                            'params': [{'name': 'address_from',
                                        'chars': (34, 74)},
                                        {'name': 'addres_to',
                                        'chars': (98,138)},
                                        {'name': 'token_value',
                                        'chars': (158, 202)}]},
            '0xa9059cbb': {'name': 'transfer(address _to, uint256 _value)',
                            'params': [{'name': 'address_to',
                                        'chars': (34, 74)},
                                        {'name': 'token_value',
                                        'chars': (74, 138)}]}
            }
    def __init__(self, **kwargs):
        contracts_file = kwargs.get('contracts_file', '')
        self.contracts = self.load_contracts(contracts_file)

    def load_contracts(self, file_):
        try:
            with open(file_, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def parse_transactions(self, transactions):
        """ Generator
        When getting an iterable with transactions, it
        checks the 'input' field to identify known token
        functions. Also checks the 'to' field against
        the list of known contract addresses. If token
        function is known it yields the data regarding
        the token's operation.
        """
        for tx in transactions:
            token_op = tx.copy()
            tx_function, input_ = tx['input'][:10], tx['input']
            if tx_function in self.token_functions:
                function = self.token_functions[tx_function]
                token_op['token_function'] = function['name']
                for param in function['params']:
                    sl = slice(*param['chars'])
                    token_op[param['name']] = input_[sl]
                
                if tx['to'] in self.contracts:
                    token_op['contract'] = self.contracts[tx['to']]['name']
                else:
                    token_op['contract'] = 'unknown'
                
                if 'token_value' in token_op:
                    decimals = 0
                    if tx['to'] in self.contracts:
                        decimals = self.contracts[tx['to']]['decimals']
                    token_op['token_value'] = hex2int(token_op['token_value'])/10**decimals
                
                yield token_op
