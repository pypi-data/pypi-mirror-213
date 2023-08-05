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
from eth_capped import EthCapped
from eth_capped.unittest import TestEthCappedInterface
from eth_capped.unittest.base import TestEthCapped


logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestCappedBase(TestEthCapped, TestEthCappedInterface, TestERC165):

    def setUp(self):
        super(TestCappedBase, self).setUp()
        self.add_interface_check('869f7594')
        self.set_method = self.set_max_supply


if __name__ == '__main__':
    unittest.main()
