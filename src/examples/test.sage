from sage.all import *

K.<x> = GF(8111)
L.<x> = GF(8111^3)
ec  = EllipticCurve(K, [1,300])
EC = EllipticCurve(L, [1,300])
 
n = ec.order()
P = EC(ec.random_element())
Q = ZZ.random_element(n) * P
 
R = EC.random_element() * (EC.order() // n^2)
 
W1 = P.weil_pairing(R, n)
W2 = Q.weil_pairing(R, n)
u = log(W2, W1)
print(factor(ec.order()))
print(W1, W2, u)
 
assert(P*u == Q)
