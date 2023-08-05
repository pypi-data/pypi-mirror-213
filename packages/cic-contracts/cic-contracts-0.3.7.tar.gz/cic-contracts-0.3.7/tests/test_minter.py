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
from eth_minter import EthMinter
from eth_minter.unittest import TestEthMinterInterface
from eth_minter.unittest.base import TestEthMinter


logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestMinterBase(TestEthMinter, TestEthMinterInterface, TestERC165):

    def setUp(self):
        super(TestMinterBase, self).setUp()
        self.add_interface_check('5878bcf4')


if __name__ == '__main__':
    unittest.main()
