import numpy as np
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.data import *

def test_caching():

    file_cache = "tests/cached_data.npy"

    if os.path.isfile(file_cache):
        os.remove(file_cache)
    assert not os.path.isfile(file_cache)
    
    @CachedFunction(file_cache)
    def read_data(a, b):
        return dict(a=a, b=b)

    data = read_data('foo','bar')
    
    assert data == dict(a='foo', b='bar')
    assert os.path.isfile(file_cache)
    
    data = read_data('foo2','bar2')

    assert data == dict(a='foo', b='bar')

def test_normalizing():

    xlen = 10
    ylen = 20
    data = np.linspace(1,xlen*ylen,xlen*ylen).reshape(xlen,ylen) - 10

    # Test only data
    with NormalizeData() as n:
        for row in data:
            n.append(row)
        linnorm = n.linnorm()
        lognorm = n.lognorm()
        zranges = n.zranges()

    assert linnorm.vmin == -9.
    assert linnorm.vmax == 190.0
    assert lognorm.vmin == 0
    assert lognorm.vmax == 2.278753600952829
    assert zranges.minpos == 1
    assert zranges.min == -9
    assert zranges.max == 190.0
    
    # Test data and x-axis
    with NormalizeData(xaxis=True) as n:
        for r,row in enumerate(data):
            xdata = np.linspace(-r,r,xlen)
            n.append(row, xdata)
        xranges = n.xranges()

    assert xranges.minpos == 0.11111111111111116
    assert xranges.min == -9
    assert xranges.max == 9

    # Test data and both axes
    with NormalizeData(xaxis=True, yaxis=True) as n:
        for r,row in enumerate(data):
            xdata = np.linspace(-r,r,xlen)
            ydata = np.linspace(-r*2,r*2,ylen)
            n.append(row, xdata, ydata)
        xranges = n.xranges()
        yranges = n.yranges()

    assert xranges.minpos == 0.11111111111111116
    assert xranges.min == -9
    assert xranges.max == 9
    assert yranges.minpos == 0.10526315789473673
    assert yranges.min == -18
    assert yranges.max == 18
    
def test_list_to_grid():

    data = range(7)
    ncols = 2
    grid = []
    for row in ListToGrid(data,ncols):
        grid.append(row)
    assert grid == [
        (0, 0, 0, 0),
        (1, 0, 1, 1),
        (2, 1, 0, 2),
        (3, 1, 1, 3),
        (4, 2, 0, 4),
        (5, 2, 1, 5),
        (6, 3, 0, 6)
    ]
