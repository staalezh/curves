from sage.all import *

def embedding_degree(E):
    """ Compute the embedding degree of E in F_p """
    p = E.base_field().characteristic()
    q = E.cardinality()
    return Zmod(q)(p).multiplicative_order()

def cm_discriminant(E):
    """ Compute the CM-discriminant of the field K in which
    End(E) is an order """
    p = E.base_field().order()
    t = E.trace_of_frobenius()

    a = t**2 - 4*p

    s = 1
    for f, m in factor(a):
        if m % 2 == 0:
            s *= f**m

    D = a / s
    if D % 4 == 1: return abs(D)

    return 4*abs(D)

def has_prime_order_subgroup(E):
    q = E.cardinality()
    return q % 4 == 0 and is_prime(Integer(q / 4))
    
class SecurityTrait(object):
    PrimeOrderSubgroup = (
            lambda E: has_prime_order_subgroup(E),
            "The subgroup of rational points is of non-prime order")

    NonTraceOne = (
            lambda E: E.cardinality() != E.base_field().order(),
            "The curve is of trace one (anomalous)")

    EmbeddingResistance = (
            lambda E: embedding_degree(E) > 5,
            "The curve is of low embedding degree")

class TechnicalTrait(object):
    PointCompression = (
            lambda F: F.order() % 4 == 3,
            "Base field is not congrurent 3 mod 4")

    OverrunProtection = (
            lambda E: E.cardinality() < E.base_field().order(),
            "Number of rational points exceed field order")
