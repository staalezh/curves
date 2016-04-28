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

    # Analytic estimation of weak curves
    alpha = arccos(2/(2*sqrt(p)))
    beta  = arccos(1/(2*sqrt(p)))
    f = lambda theta: 2/pi * sin(theta)**2

    return numerical_integral(f, alpha, beta)

def experimental_estimate(K, n):
    # Experimental estimate of weak curves
    c = 0.0
    for i in range(n):
        ec = random_curve(K)

        t = ec.trace_of_frobenius()
        if t in (0, 1, 2):
            c += 1

    return c/n

prime_fields = [GF(p) for p in primes_from(2**20, 3)]

analytical_ratios = [asymptotic_estimate(K)[0] for K in prime_fields]
experimental_ratios = [experimental_estimate(K, 10000) for K in prime_fields]

print(prime_fields)
print(analytical_ratios)
print(experimental_ratios)
