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
from eth_burner import EthBurner
from eth_burner.unittest import TestEthBurnerInterface
from eth_burner.unittest.base import TestEthBurner


logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestBurnerBase(TestEthBurner, TestEthBurnerInterface, TestERC165):

    def setUp(self):
        super(TestBurnerBase, self).setUp()
        self.add_interface_check('bc4babdd')


if __name__ == '__main__':
    unittest.main()
