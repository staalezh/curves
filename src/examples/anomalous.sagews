# vim:syntax=python

from sage.all import *

p = 101
K = GF(p)
R = IntegerModRing(p**2)

EC = EllipticCurve(Qp(p), [12, 83])
log = EC.formal_group().log()

u = 1
v = R(32*u + 92)
s = 1
t = R(15*s + 4)

P = EC(1 + p*u, 46 + p*v)
Q = EC(10 + p*s, 71 + p*t)

f = lambda P: -P[0]/P[1]

print(log(f(p*P)))
print(log(f(p*Q)))

print(log(f(p*Q))/log(f(p*P)))
