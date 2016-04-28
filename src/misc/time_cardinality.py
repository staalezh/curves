# vim:syntax=python

from sage.all import *

def random_curve(K):
    a = K.random_element()
    b = K.random_element()

    try:
        ec = EllipticCurve(K, [a, b])
        return ec
    except ArithmeticError:
        return random_curve(K)

p = next_prime(2**256)
K = GF(p)

t = cputime()
for i in range(10):
    ec = random_curve(K)
    ec.cardinality()

print(cputime(t))
