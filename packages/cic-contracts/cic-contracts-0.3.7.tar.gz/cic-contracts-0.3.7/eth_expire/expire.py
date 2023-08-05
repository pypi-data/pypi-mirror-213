# external imports
from chainlib.eth.tx import TxFormat
from chainlib.eth.tx import TxFactory
from chainlib.jsonrpc import JSONRPCRequest
from chainlib.eth.constant import ZERO_ADDRESS
from chainlib.eth.contract import ABIContractEncoder
from chainlib.eth.contract import ABIContractType
from chainlib.eth.contract import abi_decode_single
from hexathon import add_0x

class EthExpire(TxFactory):

    def apply_expiry(self, method, contract_address, sender_address, tx_format=TxFormat.JSONRPC):
        enc = ABIContractEncoder()
        enc.method('applyExpiry')
        data = enc.get()
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        tx = self.finalize(tx, tx_format)
        return tx


    def expires(self, contract_address, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('expires')
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        return o


    def parse_expires(self, v):
        return abi_decode_single(ABIContractType.UINT256, v)
