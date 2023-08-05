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
from eth_minter import EthMinter

script_dir = os.path.dirname(os.path.realpath(__file__))
contract_dir = os.path.join(script_dir, '..', '..', 'solidity')

logg = logging.getLogger(__name__)


class TestEthMinter(EthTesterCase):

    def setUp(self):
        super(TestEthMinter, self).setUp()

        self.conn = RPCConnection.connect(self.chain_spec, 'default')
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.conn)

        code = bytecode(Name.MINTER)

        txf = TxFactory(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        tx = txf.template(self.accounts[0], None, use_nonce=True)

        self.initial_supply = 1024
        enc = ABIContractEncoder()
        args = enc.get()

        tx = txf.set_code(tx, code + args)
        (tx_hash_hex, o) = txf.build(tx)
        self.conn.do(o)
        o = receipt(tx_hash_hex)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)
        self.address = r['contract_address']
        logg.debug('published minter test contract with hash {}'.format(r))
