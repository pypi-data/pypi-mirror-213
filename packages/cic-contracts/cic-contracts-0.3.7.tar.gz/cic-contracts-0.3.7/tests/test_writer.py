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
from eth_writer import EthWriter
from eth_writer.unittest import TestEthWriterInterface
from eth_writer.unittest.base import TestEthWriter


logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestWriterBase(TestEthWriter, TestEthWriterInterface, TestERC165):

    def setUp(self):
        super(TestWriterBase, self).setUp()
        self.add_interface_check('abe1f1f5')


if __name__ == '__main__':
    unittest.main()
