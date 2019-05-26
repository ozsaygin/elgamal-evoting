import random
import setup

# This block generates multiplicative inverse
###################################################
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m
####################################################


def voter_I(p, q, g, G, vote, j, h):
    k = len(G)

    # vote_gen
    r = random.randint(0, q-1)
    x = pow(g, r, p)
    y = (pow(h, r, p) * vote) % p

    # ZK proof
    a = [0]*k
    b = [0]*k
    c = [0]*k
    z = [0]*k

    for jj in range(1, k+1):
        if jj != j:
            f = k-jj+1
            # f-1 for correct index
            c[jj-1] = random.randint(0, q-1)
            z[jj-1] = random.randint(0, q-1)

            a[jj-1] = (pow(g, z[jj-1], p) * pow(x, c[jj-1], p)) % p
            b[jj-1] = (pow(h, z[jj-1], p) *
                      pow((y * modinv(G[jj-1], p)), c[jj-1], p)) % p

    w = random.randint(0, q-1)
    a[j-1] = pow(g, w, p)
    b[j-1] = pow(h, w, p)


    return x, y, a, b, c, z, r, w


def voter_III(p, q, g, j, C, c, z, r, w):
    k = len(c)

    f = k-j+1

    c[j-1] = (C - (sum(c)-c[j-1])) % q
    z[j-1] = (w - r * c[j-1]) % q

    return c, z


def HV_IV(p, q, g, h, G, C, x, y, a, b, c, z):
    k = len(G)
    C_ = sum(c) % q
    a_ = [0]*k
    b_ = [0]*k

    for i in range(k):
        a_[i] = (pow(g, z[i], p) * pow(x, c[i], p)) % p
        b_[i] = (pow(h, z[i], p) * pow((y * modinv(G[i], p)), c[i], p)) % p


    # print('C == C_ : ', C == C_)
    # print('a == a_ : ', a == a_)
    # print('b == b_ : ', b == b_)

    return C == C_ and a == a_ and b == b_


def fake_vote_gen(p, q):
    G, rho = setup.Verifiably_Random_Generator(p, q)
    return G