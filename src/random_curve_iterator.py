from sage.all import EllipticCurve
from edwards_curve import TwistedEdwardsCurve

class RandomCurveIterator:
    def __init__(self, F):
        self.F = F

    def __iter__(self):
        return self

    def next(self):
        if self.F.characteristic() < 3:
            raise ArithmeticError("Only fields of characteristic > 3 is supported")

        while True:
            try:
                a = self.F.random_element()
                d = self._random_nonsquare()

                tec = TwistedEdwardsCurve(self.F, [a, d])
                aec = tec.associated_ec()
                return tec
            except ArithmeticError:
                # The associated elliptic curve is singular. No biggie.
                pass

    def _random_nonsquare(self):
        """ We want the addition law to be complete """
        d = 1
        while self.F(d).is_square():
            d = self.F.random_element()

        return d
