import math
import random
import warnings
import sys
import pyprimes
import hashlib


def Param_Generator():
    n_p = 3072
    n_q = 256

    while True:
        q = random.randint(0, 2**n_q)
        q = q | 1
        if pyprimes.isprime(q) == True:
            break
    print('q: ', q)
    while True:
        k = random.randint(0, 2**(n_p-n_q))
        p = q * k + 1
        if pyprimes.isprime(p):
            break
    print('p: ', p)
    return (p, q)


def find_generator(p, q):
    alpha = random.randint(0, p)
    while True:
        g = pow(alpha, (p-1)//q, p)
        if g != 1:
            break
    print('g: ', g)
    return p, q, g


def Param_Generator(qbound, pbound):

    while True:
        q = random.randint(0, qbound)
        q = q | 1
        if pyprimes.isprime(q) == True:
            break
    while True:
        k = random.randint(0, pbound-qbound)
        p = q * k + 1
        if pyprimes.isprime(p):
            break

    alpha = random.randint(0, p)
    while True:
        g = pow(alpha, (p-1)//q, p)
        if g != 1:
            break
    print('g: ', g)
    return q, p, g


def Verifiably_Random_Generator(p,q):
    while True:
        rho = random.randint(0, q)
        digest = hashlib.sha256(str(rho).encode('utf-8')).digest()
        phi = int.from_bytes(digest, byteorder='big') % q
        G = pow(phi, (p-1)//q, p)
        if G != 1:
            break
    return G, rho

def KeyGen(p,q,g):
    s = random.randint(1,q-1)
    h = pow(g,s,p)
    return s, h