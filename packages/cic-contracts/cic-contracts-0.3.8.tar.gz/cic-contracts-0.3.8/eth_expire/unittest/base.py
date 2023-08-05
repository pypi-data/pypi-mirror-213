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

script_dir = os.path.dirname(os.path.realpath(__file__))
contract_dir = os.path.join(script_dir, '..', '..', 'solidity')

logg = logging.getLogger(__name__)


class TestEthExpire(EthTesterCase):

    def setUp(self):
        super(TestEthExpire, self).setUp()

        self.conn = RPCConnection.connect(self.chain_spec, 'default')
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.conn)

        code = bytecode(Name.EXPIRE)

        txf = TxFactory(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        tx = txf.template(self.accounts[0], None, use_nonce=True)

        date_expire = datetime.datetime.utcnow() + datetime.timedelta(seconds=10000)
        self.expire_value = int(date_expire.timestamp())
        enc = ABIContractEncoder()
        enc.uint256(self.expire_value)
        args = enc.get()

        tx = txf.set_code(tx, code + args)
        (tx_hash_hex, o) = txf.build(tx)
        self.conn.do(o)
        o = receipt(tx_hash_hex)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)
        self.address = r['contract_address']
        logg.debug('published expire test contract with hash {}'.format(r))


    def set_expire(self, contract_address, sender_address, v, tx_format=TxFormat.JSONRPC):
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.conn)
        txf = TxFactory(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        enc = ABIContractEncoder()
        enc.method('setExpire')
        enc.typ(ABIContractType.UINT256)
        enc.uint256(v)
        data = enc.get()
        tx = txf.template(sender_address, contract_address, use_nonce=True)
        tx = txf.set_code(tx, data)
        tx = txf.finalize(tx, tx_format)
        return tx
