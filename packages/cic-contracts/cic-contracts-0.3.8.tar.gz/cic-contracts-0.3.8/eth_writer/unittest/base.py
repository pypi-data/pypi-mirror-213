# standard imports
import os
import logging

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
from eth_writer import EthWriter

script_dir = os.path.dirname(os.path.realpath(__file__))
contract_dir = os.path.join(script_dir, '..', '..', 'solidity')

logg = logging.getLogger(__name__)


class TestEthWriter(EthTesterCase):

    def setUp(self):
        super(TestEthWriter, self).setUp()

        self.set_method = None

        self.conn = RPCConnection.connect(self.chain_spec, 'default')
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.conn)

        code = bytecode(Name.WRITER)

        txf = TxFactory(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        tx = txf.template(self.accounts[0], None, use_nonce=True)
        tx = txf.set_code(tx, code)
        (tx_hash_hex, o) = txf.build(tx)
        self.conn.do(o)
        o = receipt(tx_hash_hex)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)
        self.address = r['contract_address']
        self.contracts['writer'] = self.address
        self.roles['publisher'] = self.accounts[0]
        self.roles['writer'] = self.accounts[1]
        logg.debug('published writer test contract with hash {}'.format(r))

        c = EthWriter(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.add_writer(self.address, self.accounts[0], self.accounts[0])
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

