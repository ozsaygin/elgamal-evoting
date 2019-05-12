import math
import random
import warnings
import sys
import pyprimes
import vote_gen

k = 4 # number of candidates
ell = 40 # number of voters

#random.seed(2) # for dubugging

verbose = False

f_pk = open('pk.txt', 'r')  # file to public parameters
f_sk = open('sk.txt', 'r')  # file to private key

p = int(f_pk.readline())
q = int(f_pk.readline())
g = int(f_pk.readline())
G = [0]*k
for i in range(0, k):
    G[i] = int(f_pk.readline())
h = int(f_pk.readline())    

s = int(f_sk.readline())

if verbose:
    print("p: ", p)
    print("q: ", q)
    print("g: ", g)
    print("G: ", G)
    print("h: ", h)
    print("s: ", s)

f_pk.close()
f_sk.close()

# vote generation step
x = [0]*ell
y = [0]*ell

votes = [0]*k
for i in range(0,ell):
    j = random.randint(0,k-1) # random vote
    votes[j] += 1
    x[i], y[i] = vote_gen.vote_cast(p, q, g, G[j], h)

print("votes: ", votes)

# combine votes
X, Y = vote_gen.combine(x, y, ell, p)

# decryption step
result = vote_gen.decrypt(X, Y, p, q, s)

# Vote counting
votes_ = vote_gen.vote_cnt(G, p, k, ell, result)
if votes_ == votes:
    print("Success:))") 
    print("Election result: ", votes_)
else:
    print("Failure:((")
