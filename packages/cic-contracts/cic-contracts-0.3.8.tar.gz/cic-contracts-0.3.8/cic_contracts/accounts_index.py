# standard imports
import logging

# external imports
from chainlib.eth.tx import (
        TxFormat,
        )
from chainlib.eth.contract import (
        ABIContractEncoder,
        ABIContractDecoder,
        ABIContractType,
        abi_decode_single,
        )
from chainlib.eth.constant import ZERO_ADDRESS
from chainlib.jsonrpc import JSONRPCRequest
from chainlib.eth.error import RequestMismatchException
from hexathon import (
        add_0x,
        strip_0x,
        )

# local imports
from .base import CICTxHelper
from .writer import CICWriter

logg = logging.getLogger(__name__)


class CICAccountsIndex(CICWriter):

    def add(self, contract_address, sender_address, address, tx_format=TxFormat.JSONRPC):
        return self.single_address_method('add', contract_address, sender_address, address, tx_format)


    def have(self, contract_address, address, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('have')
        enc.typ(ABIContractType.ADDRESS)
        enc.address(address)
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        return o


    def entry_count(self, contract_address, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('entryCount')
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        return o


    def count(self, contract_address, sender_address=ZERO_ADDRESS, id_generator=None):
        return self.entry_count(contract_address, sender_address=sender_address, id_generator=id_generator)


    def entry(self, contract_address, idx, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('entry')
        enc.typ(ABIContractType.UINT256)
        enc.uint256(idx)
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        return o


    @classmethod
    def parse_account(self, v):
        return abi_decode_single(ABIContractType.ADDRESS, v)


    @classmethod
    def parse_entry(self, v):
        return abi_decode_single(ABIContractType.ADDRESS, v)


    @classmethod
    def parse_entry_count(self, v):
        return abi_decode_single(ABIContractType.UINT256, v)


    @classmethod
    def parse_have(self, v):
        return abi_decode_single(ABIContractType.BOOLEAN, v)


    @classmethod
    def parse_add_request(self, v):
        v = strip_0x(v)
        cursor = 0
        enc = ABIContractEncoder()
        enc.method('add')
        enc.typ(ABIContractType.ADDRESS)
        r = enc.get()
        l = len(r)
        m = v[:l]
        if m != r:
            logg.debug('method mismatch, expected {}, got {}'.format(r, m))
            raise RequestMismatchException(v)
        cursor += l

        dec = ABIContractDecoder()
        dec.typ(ABIContractType.ADDRESS)
        dec.val(v[cursor:cursor+64])
        r = dec.decode()
        return r 
