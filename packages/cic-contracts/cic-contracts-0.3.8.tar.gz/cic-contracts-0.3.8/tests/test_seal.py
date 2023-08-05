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
from eth_seal import EthSeal
from eth_seal.unittest import TestEthSealInterface
from eth_seal.unittest.base import TestEthSeal


logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestSealBase(TestEthSeal, TestEthSealInterface, TestERC165):

    def setUp(self):
        super(TestSealBase, self).setUp()
        self.add_interface_check('0d7491f8')
        self.set_method = self.seal


if __name__ == '__main__':
    unittest.main()
