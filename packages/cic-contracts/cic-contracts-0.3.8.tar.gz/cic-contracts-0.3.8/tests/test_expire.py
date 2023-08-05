# standard imports
import unittest
import logging
import os
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.tx import receipt
from eth_erc20 import ERC20
from giftable_erc20_token import GiftableToken
from eth_interface.unittest import TestERC165

# local imports
from eth_expire import EthExpire
from eth_expire.unittest import TestEthExpireInterface
from eth_expire.unittest.base import TestEthExpire


logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestExpireBase(TestEthExpire, TestEthExpireInterface, TestERC165):

    def setUp(self):
        super(TestExpireBase, self).setUp()
        self.add_interface_check('841a0e94')
        self.set_method = self.set_expire


if __name__ == '__main__':
    unittest.main()
