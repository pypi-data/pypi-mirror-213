# standard imports
import os
import logging
import datetime

# external imports
from chainlib.eth.unittest.ethtester import EthTesterCase
from chainlib.connection import RPCConnection
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.tx import receipt
from chainlib.eth.tx import TxFactory
from chainlib.eth.tx import TxFormat
from chainlib.eth.contract import ABIContractEncoder
from chainlib.eth.contract import ABIContractType
from cic_contracts.unittest import bytecode
from cic_contracts import Name

# local imports
from eth_burner import EthBurner

logg = logging.getLogger(__name__)


class TestEthBurner(EthTesterCase):

    def setUp(self):
        super(TestEthBurner, self).setUp()

        self.conn = RPCConnection.connect(self.chain_spec, 'default')
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.conn)

        code = bytecode(Name.BURNER)

        txf = TxFactory(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        tx = txf.template(self.accounts[0], None, use_nonce=True)

        self.initial_supply = 1024
        enc = ABIContractEncoder()
        enc = ABIContractEncoder()
        enc.uint256(self.initial_supply)
        args = enc.get()

        tx = txf.set_code(tx, code + args)
        (tx_hash_hex, o) = txf.build(tx)
        self.conn.do(o)
        o = receipt(tx_hash_hex)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)
        self.address = r['contract_address']
        logg.debug('published burner test contract with hash {}'.format(r))
