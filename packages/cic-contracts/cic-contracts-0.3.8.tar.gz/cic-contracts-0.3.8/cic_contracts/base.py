# external imports
from chainlib.eth.tx import (
        TxFactory,
        TxFormat,
        )
from chainlib.eth.contract import (
    ABIContractEncoder,
    ABIContractType,
    )


class CICTxHelper(TxFactory):

    def single_address_method(self, method, contract_address, sender_address, address, tx_format=TxFormat.JSONRPC):
        enc = ABIContractEncoder()
        enc.method(method)
        enc.typ(ABIContractType.ADDRESS)
        enc.address(address)
        data = enc.get()
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        tx = self.finalize(tx, tx_format)        
        return tx
