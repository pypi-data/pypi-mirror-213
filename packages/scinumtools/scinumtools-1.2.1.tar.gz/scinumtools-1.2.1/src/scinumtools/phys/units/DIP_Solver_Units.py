import numpy as np
import re
from math import isclose

from .QuantityClass import Quantity
from .UnitList import *

class UnitSolver:

    prefixes: dict 
    units: dict
    
    def __init__(self, **kwargs): 
        # Load unit lists into dictionaries
        kwargs['units'] = {}
        for unit in UnitStandard:
            kwargs['units'][unit[2]] = Quantity(
                unit[0], unit[1], symbol=unit[2], dfn=unit[3], name=unit[4]
            )
        kwargs['prefixes'] = {}
        for unit in UnitPrefixes:
            kwargs['prefixes'][unit[2]] = Quantity(
                unit[0], unit[1], symbol=unit[2], dfn=unit[3], name=unit[4]
            )
        super().__init__(**kwargs)
            
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
    
