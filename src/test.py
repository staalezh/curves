import sys

from random_curve_iterator import RandomCurveIterator
from sage.all import GF, next_prime

if __name__ == "__main__":
    p = next_prime(100)

    F = GF(p)

    count = 0
    for ec in RandomCurveIterator(F):
        if ec.cardinality() == p - 1:
            print(ec)
            sys.exit()
