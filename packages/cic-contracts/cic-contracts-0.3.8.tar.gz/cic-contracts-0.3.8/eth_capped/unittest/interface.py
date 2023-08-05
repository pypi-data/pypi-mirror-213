# external imports
from chainlib.eth.tx import receipt

# local imports
from eth_capped import EthCapped


class TestEthCappedInterface:

    def __init__(self):
        self.set_method = None
        self.max_supply_value = 0


    def test_default_supply(self):
        if self.max_supply_value == 0:
            return
        c = EthCapped(self.chain_spec)
        o = c.max_supply(self.address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(self.max_supply_value, int(r, 16))


    def test_supply_change(self):
        if self.set_method == None:
            return

        self.max_supply_value *= 2
        (tx_hash_hex, o) = self.set_method(self.address, self.accounts[0], self.max_supply_value)
        self.rpc.do(o)
        o = receipt(tx_hash_hex)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)

        c = EthCapped(self.chain_spec)
        o = c.max_supply(self.address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(self.max_supply_value, int(r, 16))
