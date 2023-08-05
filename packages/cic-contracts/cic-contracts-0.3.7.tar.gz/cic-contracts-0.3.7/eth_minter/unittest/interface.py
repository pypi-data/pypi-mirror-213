# external imports
from chainlib.eth.tx import receipt
from chainlib.eth.nonce import RPCNonceOracle

# local imports
from eth_minter import EthMinter


class TestEthMinterInterface:

    def test_supply(self):
        self.alice = self.accounts[1]
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)
        c = EthMinter(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.mint_to(self.address, self.accounts[0], self.alice, self.initial_supply)
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'],1)
