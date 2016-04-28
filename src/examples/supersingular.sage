# vim:syntax=python

from sage.all import *

p = 103
K.<x> = GF(p)
L.<x> = GF(p^2)

ec = EllipticCurve(K, [61, 65])
EC = ec.base_extend(L)

n = ec.order()
N = EC.order()

P = EC(48, 39, 1)
Q = EC(46, 20, 1)

R = EC(78*x + 37, 76*x + 16, 1)
w1 = R.weil_pairing(P, n)
w2 = R.weil_pairing(Q, n)

print w1, w2
print(log(w2, w1))
