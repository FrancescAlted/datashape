"""
A symbol table object to hold types for the parser.
"""

from __future__ import absolute_import, division, print_function

__all__ = ['TypeSymbolTable']

import ctypes

from . import coretypes as T

_is_64bit = (ctypes.sizeof(ctypes.c_void_p) == 8)

def _complex(tp):
    """Simple temporary type constructor for complex"""
    if tp == T.DataShape(T.float32):
        return T.complex_float32
    elif tp == T.DataShape(T.float64):
        return T.complex_float64
    else:
        raise TypeError('Cannot contruct a complex type with real component %s' % tp)

class TypeSymbolTable(object):
    """
    This is a class which holds symbols for types and type constructors,
    and is used by the datashape parser to build types during its parsing.
    A TypeSymbolTable sym has four tables, as follows:

    sym.dtype
        Data type symbols with no type constructor.
    sym.dtype_constr
        Data type symbols with a type constructor. This may contain
        symbols also in sym.dtype, e.g. for 'complex' and 'complex[float64]'.
    sym.dim
        Dimension symbols with no type constructor.
    sym.dim_constr
        Dimension symbols with a type constructor.
    """
    def __init__(self, bare=False):
        # Initialize all the symbol tables to empty dicts1
        self.dtype = {}
        self.dtype_constr = {}
        self.dim = {}
        self.dim_constr = {}
        if not bare:
            self.add_default_types()

    def add_default_types(self):
        """
        Adds all the default datashape types to the symbol table.
        """
        # data types with no type constructor
        self.dtype.update([('bool', T.bool_),
                           ('int8', T.int8),
                           ('int16', T.int16),
                           ('int32', T.int32),
                           ('int64', T.int64),
                           ('intptr', T.int64 if _is_64bit else T.int32),
                           ('int', T.int32),
                           ('uint8', T.uint8),
                           ('uint16', T.uint16),
                           ('uint32', T.uint32),
                           ('uint64', T.uint64),
                           ('uintptr', T.uint64 if _is_64bit else T.uint32),
                           ('float32', T.float32),
                           ('float64', T.float64),
                           ('real', T.float64),
                           ('complex', T.complex_float64)])
        # data types with a type constructor
        self.dtype_constr.update([('complex', _complex)])