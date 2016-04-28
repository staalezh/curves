# vim:syntax=python

from sage.all import *

p = 107
K = GF(p)

E = EllipticCurve(K, [46, 72])
n = E.order()
N = 106

P = E(66, 45)
Q = E(90, 72)

# # for i in range(100):
#     S = E.random_point()
#     if S == 0 or S.order() % N**2 != 0:
#         continue
# 
#     T = S * Integer(n / N**2)
#     if T*N == 0:
#         break
# 
