# external imports
from chainlib.eth.tx import receipt

# local imports
from eth_seal import EthSeal


class TestEthSealInterface:

    def __init__(self):
        self.set_method = None
        self.max_seal_state = 0


    def test_default_seal(self):
        if self.max_seal_state == 0:
            return
        c = EthSeal(self.chain_spec)
        o = c.max_seal_state(self.address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(self.max_seal_state, int(r, 16))


    def test_seal_set(self):
        if self.set_method == None:
            return
        if self.max_seal_state == 0:
            return

        (tx_hash, o) = self.set_method(self.contracts['seal'], self.accounts[0], self.max_seal_state)
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        c = EthSeal(self.chain_spec)
        o = c.max_seal_state(self.address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(self.max_seal_state, int(r, 16))
