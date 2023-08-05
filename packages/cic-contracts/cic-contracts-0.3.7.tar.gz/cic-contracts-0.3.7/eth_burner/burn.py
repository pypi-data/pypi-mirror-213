# external imports
from chainlib.eth.tx import TxFormat
from chainlib.eth.tx import TxFactory
from chainlib.jsonrpc import JSONRPCRequest
from chainlib.eth.constant import ZERO_ADDRESS
from chainlib.eth.contract import ABIContractEncoder
from chainlib.eth.contract import ABIContractType
from chainlib.eth.contract import abi_decode_single
from hexathon import add_0x


class EthBurner(TxFactory):

    def burn(self, contract_address, sender_address, value, tx_format=TxFormat.JSONRPC):
        enc = ABIContractEncoder()
        enc.method('burn')
        enc.typ(ABIContractType.UINT256)
        enc.uint256(value)
        data = enc.get()
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        tx = self.finalize(tx, tx_format)
        return tx


    def burn_all(self, contract_address, sender_address, tx_format=TxFormat.JSONRPC):
        enc = ABIContractEncoder()
        enc.method('burn')
        data = enc.get()
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        tx = self.finalize(tx, tx_format)
        return tx
