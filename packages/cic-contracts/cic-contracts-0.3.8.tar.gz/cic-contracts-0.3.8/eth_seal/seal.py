# external imports
from chainlib.eth.tx import TxFormat
from chainlib.eth.tx import TxFactory
from chainlib.jsonrpc import JSONRPCRequest
from chainlib.eth.constant import ZERO_ADDRESS
from chainlib.eth.contract import ABIContractEncoder
from chainlib.eth.contract import ABIContractType
from chainlib.eth.contract import abi_decode_single
from hexathon import add_0x


class EthSeal(TxFactory):

    def __noarg(self, method, contract_address, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method(method)
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        return o
   

    def max_seal_state(self, contract_address, sender_address=ZERO_ADDRESS, id_generator=None):
        return self.__noarg('maxSealState', contract_address, sender_address=sender_address, id_generator=id_generator)


    def seal_state(self, contract_address, sender_address=ZERO_ADDRESS, id_generator=None):
        return self.__noarg('sealState', contract_address, sender_address=sender_address, id_generator=id_generator)
