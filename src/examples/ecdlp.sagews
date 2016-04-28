# vim:syntax=python

from sage.all import *

def pollard_rho(P, Q, p):
    if Q == 0: return 0

    for n in range(1, p):
        if n*P == Q:
            return n
        

def discrete_log(E, P, Q):
    residues = []
    moduli   = []
    prev     = None

    for p in Primes():
        if not E.has_good_reduction(p): continue

        P_red = P.reduction(p)
        Q_red = Q.reduction(p)
        n     = P_red.order()

        residues.append(pollard_rho(P_red, Q_red, n))
        moduli.append(n)

        m = crt(residues, moduli)
        if prev == m and m*P == Q:
            return m

        prev = m


E = EllipticCurve(QQ, [-3, -1])
P = E(2, 1, 1)
Q = (2*3*5*7)*P

m = discrete_log(E, P, Q)

def reduce_problem(p):
    P_red, Q_red = P.reduction(p), Q.reduction(p)
    m_red = P_red.discrete_log(Q_red)

    return P_red, Q_red, m_red
