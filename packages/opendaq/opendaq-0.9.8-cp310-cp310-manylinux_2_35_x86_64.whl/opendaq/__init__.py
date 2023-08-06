from ._opendaq import *
import os

OPENDAQ_MODULES_DIR = os.path.dirname(os.path.abspath(__file__))

def Instance(*args) -> IInstance:
    if len(args) == 0:
        return _opendaq.Instance(OPENDAQ_MODULES_DIR)
    else:
        return _opendaq.Instance(*args)
