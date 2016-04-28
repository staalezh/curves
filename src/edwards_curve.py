import collections

from sage.schemes.generic.scheme import Scheme, is_Scheme
from sage.schemes.plane_curves.projective_curve \
    import ProjectiveCurve_generic
from sage.schemes.elliptic_curves.weierstrass_transform \
    import WeierstrassTransformation
from sage.schemes.projective.projective_point \
    import SchemeMorphism_point_abelian_variety_field
from sage.schemes.projective.projective_homset \
    import SchemeHomset_points_abelian_variety_field

from sage.all import ProjectiveSpace, EllipticCurve

class TwistedEdwardsCurvePoint(SchemeMorphism_point_abelian_variety_field):
    def __init__(self, curve, v, check = True): 
        self.curve = curve

        if v == 0:
            v = (0, 1, 1)
        elif not isinstance(v, collections.Iterable):
            raise TypeError("Invalid point type")

        if check:
            a, d = self.curve.a, self.curve.d
            x, y, z = v
            if a*x**2*z**2 + y**2*z**2 != z**4 + d*x**2 * y**2:
                raise TypeError("Coordinates %s do not define a point on %s" %
                        (v, curve))

        point_homset = curve.point_homset()
        SchemeMorphism_point_abelian_variety_field.__init__(
                self, point_homset, v, check = False)


    def __add__(self, rhs):
        x1, y1, z1 = self
        x2, y2, z2 = rhs

        a, d = self.curve.ainvs()

        A = z1*z2
        B = A**2
        D = d*x1*x2*y1*y2

        x3 = A*(x1*y2 + x2*y1)*(B - D)
        y3 = A*(y1*y2 - a*x1*x2)*(B + D)
        z3 = (B - D)*(B + D)

        return self.curve.point((x3, y3, z3), check = True)

    def __mul__(self, n):
        if n == 0: return self.curve.point(0)
        if n == 1: return self

        # Dumb point multiplication
        if n < 80:
            P = 0
            for i in xrange(n):
                P = P + self

            return P

        r = floor(log(n, 2))
        d = n - 2**r

        P = self.double(r)

        return P + self * d

    def double(self, n):
        x1, y1, z1 = self
        x2, y2, z2 = self

        a, d = self.curve.ainvs()

        for i in range(n):
            A = z1*z2
            B = A**2
            D = d*x1*x2*y1*y2

            x3 = A*(x1*y2 + x2*y1)*(B - D)
            y3 = A*(y1*y2 - a*x1*x2)*(B + D)
            z3 = (B - D)*(B + D) 

            x1, y1, z1 = x3, y3, z3
            x2, y2, z2 = x3, y3, z3

        return self.curve.point((x3, y3, z3), check = False)

class TwistedEdwardsCurve(ProjectiveCurve_generic):
    _point = TwistedEdwardsCurvePoint

    def __init__(self, K, ainvs):
        self.__base_ring = K
        self.__ainvs = tuple(map(K, ainvs))
        self.a, self.d = self.__ainvs

        P2 = ProjectiveSpace(2, K, names='xyz')
        x, y, z = P2.coordinate_ring().gens()

        a, d = self.ainvs()
        f = a*x**2*z**2 + y**2*z**2 - z**4 - d*x**2*y**2
        ProjectiveCurve_generic.__init__(self, P2, f)

    def __str__(self):
        a, d = self.ainvs()
        return "Twisted Edwards Curve defined by %dx^2 + y^2 = 1 - %dx^2y^2 " \
               "over %s" % (a, d, self.base_ring())

    def to_weierstrass_map(self):
        """ 
        Returns a morphism from this Edwards curve to the associated
        elliptic curve on Weierstrass form.
        """

        P2 = ProjectiveSpace(2, self.__base_ring, names='xyz')
        x, y, z = P2.coordinate_ring().gens()

        a, d = self.ainvs()

        E = self.associated_ec()
        C = P2.subscheme(a*x**2*z**2 + y**2*z**2 - z**4 - d*x**2*y**2)
        f = WeierstrassTransformation(C, E, [
            (a - d)*(z + y)*x,       # <-- x
            (a - d)*2*(z**2 + y*z),  # <-- y
            z*x*(z - y)              # <-- z
            ], 1)

        return f

    def from_weierstrass_map(self):
        """
        Returns a morphism from the associated elliptic curve on
        Weierstrass form to this Edwards curve.
        """

        P2 = ProjectiveSpace(2, self.__base_ring, names='xyz')
        x, y, z = P2.coordinate_ring().gens()

        a, d = self.ainvs()

        E = self.associated_ec()
        C = P2.subscheme(a*x**2*z**2 + y**2*z**2 - z**4 - d*x**2*y**2)
        f = WeierstrassTransformation(E, C, [
            2*x*(x + (a - d)*z),  # <-- x
            (x - (a - d)*z)*y,    # <-- y
            y * (x + (a - d)*z)    # <-- z
            ], 1)

        return f

    def associated_ec(self):
        """
        Returns the elliptic curve that is birationally equivalent to
        this Edwards curve. That is, the elliptic curve given by
        E: y^2 = x^3 + 2(a + d)x^2 + (a - d)^2x
        """
        
        a, d = self.ainvs()
        K = self.__base_ring
        return EllipticCurve(K, [0, 2*(a + d), 0, (a - d)**2, 0])

    def ainvs(self):
        return self.__ainvs

    def __call__(self, *args):
        if len(args) == 1 and args[0] == 0:
            R = self.base_ring()
            return self.point([R(0), R(1), R(1)], check=False)

        return self.point(*args, check=True)

    def _point_homset(self, *args, **kwds):
        return SchemeHomset_points_abelian_variety_field(*args, **kwds)
