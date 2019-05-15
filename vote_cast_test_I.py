import math
import random
import warnings
import sys
import pyprimes
import vote_cast_I # this is the file that contains your codes for Section 5.1

def run_protocol(p, q, g, G, vote, j, h):
    # vote casting
    # step 1 by voter: (x, y) is the vote
    # x, y, a, and b are sent to HV
    # c, z, r, and w are not shared with HV      
    x, y, a, b, c, z, r, w = vote_cast_I.voter_I(p, q, g, G, vote, j, h)

    if verbose:
        print("a: ", a)
        print("b: ", b)
        print("c: ", c)
        print("z: ", z)

    # step 2 by HV: random challenge C     
    C = random.randint(0, q-1)

    # Step 3 by voter:  response
    # c and z are now sent to HV
    c, z = vote_cast_I.voter_III(p, q, g, j, C, c, z, r, w)

    if verbose:
        print("c: ", c)
        print("z: ", z)
    
    # Step 4 by HV: verification of the response
    print("Vote is good: ", vote_cast_I.HV_IV(p, q, g, h, G, C, x, y, a, b, c, z))    


k = 3 # number of candidates

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

j = 1 # voting for the first candidate; 
          # i.e., G(j-1) as the index starts at 0
# run_protocol should return True
print("Vote generation for G_"+str(j))
vote = G[j-1]
run_protocol(p, q, g, G, vote, j, h)

j = 2 # voting for the second candidate; 
# run_protocol should return True
print("\nVote generation for G_"+str(j))
vote = G[j-1]
run_protocol(p, q, g, G, vote, j, h)

j = 3 # voting for the third candidate;
# run_protocol should return True
print("\nVote generation for G_"+str(j))
vote = G[j-1]
run_protocol(p, q, g, G, vote, j, h)

# Another random generator G_fake
# run_protocol should return False
# "vote" here is a generator that corresponds to none of the candidates
print("\nVote generation using a different G")
vote = vote_cast_I.fake_vote_gen(p, q)
run_protocol(p, q, g, G, vote, 1, h)

# Multiple voting for one candidate
# run_protocol should return False
print("\nGenerating 100 votes for G_"+str(j))
j = 3
vote = pow(G[j-1], 100, p)
run_protocol(p, q, g, G, vote, j, h)
