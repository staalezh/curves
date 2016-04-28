# vim:syntax=python

from sage.all import *

p = 107
K = GF(p)

ec = EllipticCurve(K, [46, 72])
n = ec.order()

P = ec(66, 45, 1)
Q = 43*P
R = ec(63, 47, 1)

w1 = R.tate_pairing(P, n, 1)
w2 = R.tate_pairing(Q, n, 1)
print(log(w2, w1))
