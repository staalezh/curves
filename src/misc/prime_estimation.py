
# vim:syntax=python

from sage.all import *

class primes_from:
    def __init__(self, p, n):
        self.p = p if is_prime(p) else next_prime(p)
        self.c = 0
        self.n = n

    def __iter__(self):
        return self

    def next(self):
        if self.n != None and self.c >= self.n:
            raise StopIteration()

        r = self.p
        self.p = next_prime(self.p)
        self.c += 1
        return r

def random_curve(K):
    a = K.random_element()
    b = K.random_element()

    try:
        ec = EllipticCurve(K, [a, b])
        return ec
    except ArithmeticError:
        return random_curve(K)

def asymptotic_estimate(K):
    p = K.order()
    R = RealField(ceil(log(p, 2)))

    # The Hasse bound (a, b)
    a = R(p + 1 - 2*sqrt(p))
    b = R(p + 1 + 2*sqrt(p))

    return ((b/log(b) - a/log(a)) / (b - a))

def experimental_estimate(K, n):
    # Experimental estimate of curves with #E(F_p) prime
    c = 0.0
    for i in range(n):
        ec = random_curve(K)

        if is_prime(ec.cardinality()):
            c += 1

    return float(c/n)

# prime_fields = [GF(p) for p in primes_from(2**20, 1)]
# 
# analytical_ratios   = [asymptotic_estimate(K)         for K in prime_fields]
# experimental_ratios = [experimental_estimate(K, 1000) for K in prime_fields]
# 
# print(prime_fields)
# print(analytical_ratios)
# print(experimental_ratios)

p = next_prime(2**256)
F = GF(p)

ae = asymptotic_estimate(F)
print(ae)
print(0.5*ae)
