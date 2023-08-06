from typing import List
import numpy as np
import re
from math import isclose
from typing import Union
from dataclasses import dataclass

from ...structs import ParameterDict
from .UnitList import *

class Quantity:
    prefixes: dict            # list of prefixes 
    unitlist: dict               # list of units
    
    magnitude: float          # quantity magnitude
    dimensions: List[int]     # quantity dimensions
    baseunits: dict            # base units

    precision: float = 1e-7

    def __init__(
            self, magnitude:float,
            dimensions = None,
            baseunits = {},
            precision:float=1e-7
    ):
        # Initialize settings
        self.unitlist = ParameterDict(['magnitude','dimensions','definition','name'], UnitStandard)
        self.prefixes = ParameterDict(['magnitude','dimensions','definition','name'], UnitPrefixes)
        self.precision = precision
        self.magnitude = magnitude
        # Set quantity
        if isinstance(dimensions, str):
            unit = self._solve(dimensions)
            self.magnitude *= float(unit.magnitude)
            self.dimensions = list(unit.dimensions)
            self.baseunits = dict(unit.baseunits)
        elif dimensions is None and baseunits:
            dimensions = "*".join({f"{k}{w:d}" for k,w in baseunits.items()})
            unit = self._solve(dimensions)
            self.magnitude *= float(unit.magnitude)
            self.dimensions = list(unit.dimensions)
            self.baseunits = dict(baseunits)            
        elif isinstance(dimensions, (list, np.ndarray)):
            self.dimensions = list(dimensions)
            if baseunits:
                self.baseunits = baseunits
            else:
                self.baseunits = {UnitBase[d]:dim for d,dim in enumerate(self.dimensions) if dim!=0 and d>0}
        elif isinstance(dimensions, Quantity):
            self.magnitude *= float(dimensions.magnitude)
            self.dimensions = list(dimensions.dimensions)
            self.baseunits = dict(dimensions.baseunits)
        else:
            self.dimensions = [0]*len(UnitBase)
        # Rebase quantity exponents
        if self.magnitude<0:
            exp = int(np.floor(np.log10(-self.magnitude)))
            magnitude = self.magnitude/10**exp
        elif self.magnitude==0:
            exp = 0
            magnitude = 0
        else:
            exp = int(np.floor(np.log10(self.magnitude)))
            magnitude = self.magnitude/10**exp
        self.magnitude = magnitude
        self.dimensions[0] += exp
        
    def __add__(self, other):
        if not self.dimensions[1:]==other.dimensions[1:]:
            raise Exception('Addition of two units with different dimensions:', self, other)
        magnitude =  self.magnitude * 10**self.dimensions[0]
        magnitude += other.magnitude * 10**other.dimensions[0]
        dimensions = [0] + self.dimensions[1:]
        print('+',self.baseunits, other.baseunits)
        return Quantity(magnitude, dimensions)

    def __sub__(self, other):
        if not self.dimensions[1:]==other.dimensions[1:]:
            raise Exception('Substraction of two units with different dimensions:', self, other)
        magnitude =  self.magnitude * 10**self.dimensions[0]
        magnitude -= other.magnitude * 10**other.dimensions[0]
        dimensions = [0] + self.dimensions[1:]
        print('-',self.baseunits, other.baseunits)
        return Quantity(magnitude, dimensions)
    
    def __mul__(self, other):
        magnitude = self.magnitude*other.magnitude
        dimensions = [self.dimensions[i]+other.dimensions[i] for i in range(len(self.dimensions))]
        print('*',self.baseunits, other.baseunits)
        baseunits = dict(self.baseunits)
        for unit,exp in other.baseunits.items():
            baseunits[unit] = baseunits[unit]+exp if unit in baseunits else exp
        return Quantity(magnitude, dimensions, baseunits)

    def __truediv__(self, other):
        magnitude = self.magnitude/other.magnitude
        dimensions = [self.dimensions[i]-other.dimensions[i] for i in range(len(self.dimensions))]
        print('/',self.baseunits, other.baseunits)
        return Quantity(magnitude, dimensions)

    def __pow__(self, power):
        magnitude = self.magnitude**power
        dimensions = [self.dimensions[i]*power for i in range(len(self.dimensions))]
        print('**',self.baseunits)
        return Quantity(magnitude, dimensions)

    def __eq__(self, other):
        if not isclose(self.magnitude, other.magnitude, rel_tol=self.precision):
            return False
        if self.dimensions!=other.dimensions:
            return False
        return True

    def _str_units(self,symbol,exponent):
        if exponent==1:
            return f"{symbol}"
        else:
            return f"{symbol}{exponent}"
    
    def __str__(self):
        if self.baseunits:
            unit = self/Quantity(1,baseunits=self.baseunits)
            magnitude = unit.magnitude * 10**unit.dimensions[0]
            units = "*".join([self._str_units(s,e) for s,e in self.baseunits.items()])
        else:
            units = []
            for s,symbol in enumerate(UnitBase):
                exponent = self.dimensions[s]            
                if s==0:
                    magnitude = self.magnitude * 10**exponent
                elif exponent!=0:
                    unit, exp = self._str_units(symbol,exponent)
                    magnitude *= 10**exp
                    units.append(unit)
            units = "*".join(units)
        return f"Quantity({magnitude:.03e} {units})"
            
    def _solve_atom(self, string=None):
        # parse number
        m = re.match(r'^[-]?([0-9.]+)(e([0-9+-]+)|)$', str(string))
        if m:
            num = float(string)
            return Quantity(num)
        # parse unit
        string_bak = string
        exp, base, prefix = '', '', ''
        symbol, string = string[-1], ' '+string[:-1]
        # parse exponent
        while len(string):
            if not re.match('^[0-9+-]{1}$', symbol):
                break
            exp = symbol+exp
            symbol, string = string[-1], string[:-1]
        baseunit = string[1:]+symbol
        # parse unit symbol
        unitkeys = self.unitlist.keys()
        while len(string):
            nbase = len(base)+1
            ukeys = [key[-nbase:] for key in unitkeys]
            if symbol+base not in ukeys:
                break
            base = symbol+base
            symbol, string = string[-1], string[:-1]
        # parse unit prefix
        while len(string):
            prefix = symbol+prefix
            symbol, string = string[-1], string[:-1]
            if symbol==' ':
                break
        # apply prefix
        prefixes = self.prefixes.keys()
        unit = Quantity(self.unitlist[base].magnitude, self.unitlist[base].dimensions)
        if prefix:
            if prefix not in prefixes:
                raise Exception(f"Unknown unit prefix:", string_bak)
            unit *=  Quantity(self.prefixes[prefix].magnitude, self.prefixes[prefix].dimensions)
        # apply exponent
        if exp:
            unit = unit**int(exp)
            unit.baseunits = {baseunit: int(exp)}
        else:
            unit.baseunits = {baseunit: 1}
        return unit

    def _solve(self, right):
        if right.count('(')!=right.count(')'):
            raise Exception(f"Unmatched parentheses in: {right}")
        left = ''
        symbol, right = right[0], right[1:]
        parentheses = 0
        while right:
            if symbol=='*':
                unit1 = self._solve(left)
                unit2 = self._solve(right)
                unit3 = unit1 * unit2
                return unit3
            elif symbol=='/':
                if '/' in right:
                    # If there are multiple divisions
                    # we need to start from the last
                    parts = right.split('/')
                    right = parts.pop()
                    parts.insert(0,left)
                    left = '/'.join(parts)
                return self._solve(left) / self._solve(right)
            elif symbol=='(':
                parentheses = 1
                symbol, right = right[0], right[1:]
                while parentheses>0:
                    if symbol=='(':
                        parentheses+=1
                    elif symbol==')':
                        parentheses-=1
                    else:
                        left = left + symbol
                    if not right:
                        return self._solve(left)
                    symbol, right = right[0], right[1:]
            else:
                left = left + symbol
                symbol, right = right[0], right[1:]
        unit = self._solve_atom(left+symbol)
        return unit
                
    def to(self, other):
        if isinstance(other,str):
            other = self._solve(other)
        elif isinstance(dimensions, (list, np.ndarray)):
            other = Quantity(1.0, other)
        if not self.dimensions[1:]==other.dimensions[1:]:
            raise Exception(f"Units cannot be converted:", self, other)
        else:
            return self / other
