import numpy as np
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.phys.units import *

def test_units():
    """
    q = Quantity(123, [2,3,3,0,0,1,0,0,0])
    assert str(q) == "Quantity(1.230e+04 m3*g3*C)"

    q = q / Quantity(123, 'C')
    assert str(q) == "Quantity(1.000e+02 m3*g3)"

    q = q * Quantity(2, 's2')
    assert str(q) == "Quantity(2.000e+02 m3*g3*s2)"

    q = Quantity(123, "kg3*cm-2*s")
    assert str(q) == "Quantity(1.230e+02 kg3*cm-2*s)"

    q = Quantity(123e34, "J")
    assert str(q) == "Quantity(1.230e+36 J)"
    
    q = q / Quantity(123, 's')
    assert str(q) == "Quantity(1.000e+36 J*s-1)"

    assert 1==0
    """
    pass
