# external imports
from chainlib.eth.tx import TxFormat
from chainlib.eth.tx import TxFactory
from chainlib.jsonrpc import JSONRPCRequest
from chainlib.eth.constant import ZERO_ADDRESS
from chainlib.eth.contract import ABIContractEncoder
from chainlib.eth.contract import ABIContractType
from hexathon import add_0x

class EthCapped(TxFactory):

    def max_supply(self, contract_address, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('maxSupply')
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        return o
