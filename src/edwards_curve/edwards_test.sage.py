# This file was *autogenerated* from the file edwards_test.sage
from sage.all_cmdline import *   # import sage library
_sage_const_13 = Integer(13); _sage_const_2 = Integer(2); _sage_const_1 = Integer(1); _sage_const_10000 = Integer(10000); _sage_const_12 = Integer(12)
load('edwards_curve.py')

from sage.all import *
import random

K = GF(_sage_const_13 )
ed = TwistedEdwardsCurve(K, [_sage_const_1 , _sage_const_2 ])
ec = ed.associated_ec()

Q = ec(_sage_const_12 , _sage_const_2 , _sage_const_1 )
f = ed.from_weierstrass_map()
P = TwistedEdwardsCurvePoint(ed, f(Q))

timeit("P + P", number = _sage_const_10000 )
timeit("Q + Q", number = _sage_const_10000 )