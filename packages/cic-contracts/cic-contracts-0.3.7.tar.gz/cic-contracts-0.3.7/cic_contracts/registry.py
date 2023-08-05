# standard imports
import logging
import hashlib

# external imports
from chainlib.jsonrpc import JSONRPCRequest
from chainlib.eth.contract import (
        ABIContractEncoder,
        ABIContractType,
        abi_decode_single,
        )
from chainlib.eth.tx import TxFactory
from hexathon import (
        add_0x,
        strip_0x,
        )
from chainlib.eth.constant import (
        ZERO_ADDRESS,
        )

logg = logging.getLogger(__name__)


def to_text(b):
        b = b[:b.find(0)]
        # TODO: why was this part of this method previously?
        # if len(b) % 2 > 0:
        #     b = b'\x00' + b
        return b.decode('utf-8')


def from_text(txt):
    return '0x{:0<64s}'.format(txt.encode('utf-8').hex())


def from_identifier(b):
    return to_text(b)


def from_identifier_hex(hx):
    b = bytes.fromhex(strip_0x(hx))
    return from_identifier(b)


def to_identifier(txt):
    return from_text(txt)


class CICRegistry(TxFactory):

    def address_of(self, contract_address, identifier_string, sender_address=ZERO_ADDRESS, id_generator=None):
        identifier = to_identifier(identifier_string)
        logg.debug('using identifier for addressOf {} -> {}'.format(identifier, identifier_string))
        return self.address_of_literatl(contract_address, identifier, sender_address=sender_address, id_generator=id_generator)


    def address_of_literal(self, contract_address, identifier, sender_address=ZERO_ADDRESS, id_generator=None): 
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('addressOf')
        enc.typ(ABIContractType.BYTES32)
        enc.bytes32(identifier)
        data = add_0x(enc.encode())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        o = j.finalize(o)
        return o


    @classmethod
    def parse_address_of(self, v):
        return abi_decode_single(ABIContractType.ADDRESS, v)


    def set(self, contract_address, sender_address, identifier_string, address):
        enc = ABIContractEncoder()
        enc.method('set')
        enc.typ(ABIContractType.BYTES32)
        enc.typ(ABIContractType.ADDRESS)
        identifier = to_identifier(identifier_string)
        enc.bytes32(identifier)
        enc.address(address)
        data = enc.encode()
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        return self.build(tx)


    def bind(self, contract_address, sender_address, identifier_string, reference):
        enc = ABIContractEncoder()
        enc.method('bind')
        enc.typ(ABIContractType.BYTES32)
        enc.typ(ABIContractType.BYTES32)
        identifier = to_identifier(identifier_string)
        enc.bytes32(identifier)
        enc.bytes32(reference)
        data = enc.encode()
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        return self.build(tx)


    def identifier(self, contract_address, idx, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('identifiers')
        enc.typ(ABIContractType.UINT256)
        enc.uint256(idx)
        data = add_0x(enc.encode())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        o = j.finalize(o)
        return o


    @classmethod
    def parse_identifier(self, v):
        return from_identifier_hex(v)
