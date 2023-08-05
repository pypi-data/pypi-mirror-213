# standard imports
import os

# local imports
from cic_contracts.data import data_dir
from cic_contracts.names import Name


def search(v, ext='interface', search_dir=data_dir):
    if isinstance(v, Name):
        v = v.value
    fp = os.path.join(search_dir, v + '.' + ext)
    f = open(fp, 'r')
    r = f.read()
    f.close()
    return r.rstrip()
