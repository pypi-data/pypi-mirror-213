# external imports
from chainlib.eth.tx import (
        TxFactory,
        TxFormat,
        )

# local imports
from .base import CICTxHelper

class CICWriter(CICTxHelper):

    def add_writer(self, contract_address, sender_address, address, tx_format=TxFormat.JSONRPC):
        return self.single_address_method('addWriter', contract_address, sender_address, address, tx_format)


    def delete_writer(self, contract_address, sender_address, address, tx_format=TxFormat.JSONRPC):
        return self.single_address_method('deleteWriter', contract_address, sender_address, address, tx_format)
