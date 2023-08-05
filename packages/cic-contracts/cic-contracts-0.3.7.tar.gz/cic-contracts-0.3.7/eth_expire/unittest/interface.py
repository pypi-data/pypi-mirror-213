# external imports
from chainlib.eth.tx import receipt

# local imports
from eth_expire import EthExpire


class TestEthExpireInterface:

    def __init__(self):
        self.set_method = None


    def test_expire(self):
        if self.expire_value == 0:
            return
        c = EthExpire(self.chain_spec)
        o = c.expires(self.address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(self.expire_value, int(r, 16))


    def test_expire_change(self):
        if self.set_method == None:
            return

        self.expire_value += 43200
        (tx_hash_hex, o) = self.set_method(self.address, self.accounts[0], self.expire_value)
        self.rpc.do(o)
        o = receipt(tx_hash_hex)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)

        c = EthExpire(self.chain_spec)
        o = c.expires(self.address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(self.expire_value, int(r, 16))
