import random


def voter_I(p, q, g, G, vote, j, h):
    # vote_gen
    r = random.randint(0, q-1)
    x = pow(g, r, p)
    y = (pow(h, r, p) * G) % p
    
    # ZK proof
    w = random.randint(0, q-1)
    a = pow(g, w,p )
    b = pow(h, w,p)

    # k = 2−j+1
    a_k = 

    return x, y, a, b, c, z, r, w

# def voter_III(p, q, g, j, C, c, z, r, w):
#     pass

# def HV_IV(p, q, g, h, G, C, x, y, a, b, c, z):
#     pass

# def fake_vote_gen(p, q):
#     pass
