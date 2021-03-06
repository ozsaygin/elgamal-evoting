import random


def vote_cast(p, q, g, G, h):
    # print('vote_cast')
    r = random.randint(0, q)
    x = pow(g, r, p)
    y = (pow(h, r, p) * G) % p

    return x, y


def combine(x, y, ell, p):
    # print('combine')
    X = 1
    Y = 1
    for i in range(ell):
        X = (X * x[i]) % p
        Y = (Y * y[i]) % p

    # print('X: ', X)
    # print('Y: ', Y)
    return X, Y


def decrypt(X, Y, p, q, s):  # DONE IMO
    # print('decrypt')
    plain = (Y* pow(X, q-s, p)) %p
    # print('plain: ', plain )
    return plain


def nToSum(N, S):
    ''' Creates a nested list of all possible lists of length N that sum to S'''
    if N <= 1:  # base case
        return [S]
    else:
        L = []
        for x in range(S+1):  # create a sub-list for each possible entry of 0 to S
            # create a sub-list for this value recursively
            L += [[x, nToSum(N-1, S-x)]]
        return L


def compress(n, L):  # designed to take in a list generated by nToSum
    '''takes the input from nToSum as list L, and then flattens it so that each list is a
       top level list.  Leading set n is the "prefix" list, and grows as you climb down the 
       sublists'''
    if type(L[0]) == int:  # base case:  you have exposed a pure integer
        return [n+L]  # take that integer, and prepend the leading set n
    else:
        Q = []
        for x in L:  # look at every sublist
            # for each sublist, create top level lists recursively
            Q += compress(n+[x[0]], x[1])
        return Q                          # note:  append x[0] to leading set n


def vote_cnt(G, p, k, ell, result):
    # print('vote_cnt')
    comb = compress([], nToSum(k, ell))
    for c in comb:
        res = 1
        for i in range(len(G)):
            res *= pow(G[i], c[i], p)
        res = res % p
        # print('res1', res)
        # print('res2', result)
        if res == result:
            return c
