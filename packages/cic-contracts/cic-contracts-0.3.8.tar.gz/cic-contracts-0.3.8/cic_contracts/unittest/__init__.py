# standard imports
import os

# local imports
from cic_contracts.search import search
from cic_contracts import Name

cic_unittest_dir = os.path.dirname(os.path.realpath(__file__))
contracts_dir = os.path.join(cic_unittest_dir, 'solidity')


def bytecode(v):
    if isinstance(v, Name):
        v = v.value
    return search(v + 'Test', ext='bin', search_dir=contracts_dir)

    
