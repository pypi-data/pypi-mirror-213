# external imports
from hexathon import strip_0x
from hexathon import same as same_hex
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.address import to_checksum_address
from eth_owned import Owned


class TestInterface:

    def __owned_check(self):
        self.owner == to_checksum_address(self.owner)


    def test_owner(self):
        self.__owned_check()
       
        c = Owned(self.chain_spec)
        o = c.owner(self.address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        owner_address = c.parse_owner(r)
        self.assertTrue(same_hex(self.owner, owner_address))
