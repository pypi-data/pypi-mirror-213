# external imports
from chainlib.eth.tx import receipt
from chainlib.eth.nonce import RPCNonceOracle

# local imports
from eth_burner import EthBurner


class TestEthBurnerInterface:

    def test_supply(self):
        self.alice = self.accounts[1]
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)
        c = EthBurner(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.burn(self.address, self.accounts[0], int(self.initial_supply / 2))
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)
