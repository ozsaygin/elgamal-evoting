import math
import random
import warnings
import sys
import pyprimes
import vote_gen
import tally

k = 4 # number of candidates
ell = 40 # number of voters
n = 5 # number of tallying authorities
t = 3 #  the threshold for Shamir's secret sharing

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

# secret sharing of the secret key
s_a = tally.ShamirSecretSharing(n, t, s, q)
h_a = [0]*n
for i in range(0, n):
    h_a[i] = pow(g, s_a[i], p)

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

# Pick a random quorum
a = random.sample(range(n), t)
print('a: ', a)
Lambda = [0]*t
for i in range(0, t):
    Lambda[i] = s_a[a[i]]

print("Random Quorum: ", a, Lambda)

# The authorities in the quorum multicasts Omega_a = X^s mod p
Omega = tally.PartialDecryption(X, a, Lambda, t, p)
print("Omega: ", Omega)

# Perform Full Decryption
votes_ = tally.FullDecryption(Y, a, Omega, G, t, p, q)
if votes_ == votes:
    print("Success:))") 
    print("Election result: ", votes_)
else:
    print("Failure:((")

# Check if it is a good quorum
# This time, it is good
h_a_lambda = [0]*t
for i in range(0, t):
    h_a_lambda[i] = h_a[a[i]]

h_ = tally.CheckQuorum(a, h_a_lambda, p, q)
if h_ == h:
    print("Success: Good quorum:))") 
else:
    print("Failure:Bad quorum:((")
    
# Zero-Knowledge proof of common exponent
i = random.randint(0,t-1) # pick a random tallying authority in the quorum
if (tally.ZK_commonexp(Lambda[i], h_a_lambda[i], Omega[i], p, q) == True):
    print("Success: Zero-Knowledge proof of common exponent:)")
else:
    print("Failure: Zero-Knowledge proof of common exponent:(")

# Check if it is a good quorum
# This time, it is bad
h_a_lambda = [0]*t
for i in range(0, t):
    h_a_lambda[i] = h_a[a[i]]
h_a_lambda[1] = random.randint(0,q)   # bad one

h_ = tally.CheckQuorum(a, h_a_lambda, p, q)
if h_ == h:
    print("Success: Good quorum:))") 
else:
    print("Failure:Bad quorum:((")
    
# Zero-Knowledge proof of common exponent
# This is bad
i = random.randint(0,t-1) # pick a random tallying authority in the quorum
Omega[i] = random.randint(0,q) # bad one
if (tally.ZK_commonexp(Lambda[i], h_a_lambda[i], Omega[i], p, q) == True):
    print("Success: Zero-Knowledge proof of common exponent:)")
else:
    print("Failure: Zero-Knowledge proof of common exponent:(")    
