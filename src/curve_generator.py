from sage.all import EllipticCurve, parallel

from random_curve_iterator import RandomCurveIterator

class CurveGenerator:
    """
    Generate a curve over a field F of characteristic different from 2 and
    3, that passes a set of tests on the curve and base field.
    """

    def __init__(self, F, curve_traits):
        self.F = F
        self.curve_traits = curve_traits

    def run(self):
        print("Starting curve generation...")
        for tec in RandomCurveIterator(self.F):
            ec = tec.associated_ec()
            if self.check_curve(ec):
                return tec

    def check_curve(self, curve):
        return self.curve_traits.check(curve, nothrow = True)

