import vote_cast_II
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


def change_vote(p, q, g, G, x, y, r, j, k):
    old_vote = G[j-1]
    new_vote = G[k-1]

    diff = (old_vote * modinv(new_vote, p)) % p
    y_ = (y * new_vote) % p
    y_ = (y_ * diff) % p

    y_ = y
    x_ = x
    return x_, y_