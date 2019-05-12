import math
import random
import warnings
import sys
import pyprimes
import hashlib
import setup

qbound = 2**160
pbound = 2**1024
k = 4

f_pk = open('pk.txt', 'w')  # file to public parameters
f_sk = open('sk.txt', 'w')  # file to private key

q, p, g = setup.Param_Generator(qbound, pbound)

print ("q is prime: ", q, pyprimes.isprime(q))
print ("p is prime: ", p, pyprimes.isprime(p))
print ("g is a generator: ", g, (pow(g, (p-1)//q, p) != 1))

f_pk.write(str(p)+"\n")
f_pk.write(str(q)+"\n")
f_pk.write(str(g)+"\n")

for i in range(0,k):
    G, rho = setup.Verifiably_Random_Generator(p, q)
    phi = int.from_bytes(hashlib.sha256(str(rho).encode('utf-8')).digest(), byteorder='big')%q
    if G == pow(phi, (p-1)//q, p):
        print ("G is generated verifiably randomly")
    else:
        print ("G is not generated verifiably randomly")
    f_pk.write(str(G)+"\n")

s, h = setup.KeyGen(p, q, g)
f_pk.write(str(h))
f_sk.write(str(s))
f_pk.close()
f_sk.close()



