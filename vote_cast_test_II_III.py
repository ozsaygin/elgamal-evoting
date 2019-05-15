import math
import random
import warnings
import sys
import pyprimes
import vote_cast_II
import vote_cast_III

HV_CHEAT = False

def run_protocol(p, q, g, G, vote, j, h):
    # vote casting
    # step 1 by voter: (x, y) is the vote
    # x, y, a, and b are sent to HV
    # c, z, r, and w are not shared with HV
    # same as vote_cast_I.voter_I
    x, y, a, b, c, z, r, w1 = vote_cast_II.voter_I(p, q, g, G, vote, j, h)

    if verbose:
        print("a: ", a)
        print("b: ", b)
        print("c: ", c)
        print("z: ", z)

    # step 2 by HV: random challenge C
    # u, v, d, e, and C are sent to voter
    # t and w2 are not shared with voter
    C, u, v, d, e, t, w2 = vote_cast_II.HV_II(p, q, g, h)
    if HV_CHEAT == True:
        k = random.randint(0,len(G)-1)
        v = v*pow(G[k], 100, p)

    # Step 3 by voter:  response
    # c and z are now sent to HV
    c, z, f = vote_cast_II.voter_III(p, q, g, j, C, c, z, r, w1)

    if verbose:
        print("c: ", c)
        print("z: ", z)
    
    # Step 4 by HV: verification of the response
    ver, sigma = vote_cast_II.HV_IV(p, q, g, h, G, C, x, y, a, b, c, z, t, w2, f)
    print("Vote is good: ", ver)

    # Step 5 by voter: accepts u, v and generates the final vote
    accept, xf, yf = vote_cast_II.voter_V(p, q, g, h, x, y, f, u, v, e, d, sigma)
    print("voter accepts u and v: ", accept)
    if(x==xf or y==yf):
        print("This is not a final vote!!!")

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
vote = vote_cast_II.fake_vote_gen(p, q)
run_protocol(p, q, g, G, vote, 1, h)

# Multiple voting for one candidate
# run_protocol should return False
print("\nGenerating 100 votes for G_"+str(j))
j = 3
vote = pow(G[j-1], 100, p)
run_protocol(p, q, g, G, vote, j, h)

j = 1 # voting for the first candidate; 
          # i.e., G(j-1) as the index starts at 0
# run_protocol should return True
# However, voter refuse to generate final vote
# as u and v are not properly selected
print("\nHV is cheating and getting caught")
HV_CHEAT = True
vote = G[j-1]
run_protocol(p, q, g, G, vote, j, h)

# Test for 5.3
# j = 2 original vote for G_2
print("\nVoter is trying to sell his vote")
j = 2
vote = G[j-1]
x, y, a, b, c, z, r, w1 = vote_cast_II.voter_I(p, q, g, G, vote, j, h)
if (x == pow(g, r, p) and y == (pow(h,r,p)*G[j-1])%p):
    print("(x, y) is indeed a vote for G_"+str(j))
else:
    print("(x, y) is not a vote for G_"+str(j))
    
# Transform the original vote (x,y) to a vote for G_3 (k=3)
k = 3
x_, y_ = vote_cast_III.change_vote(p, q, g, G, x, y, r, j, k)
if (x_ == pow(g, r, p) and y_ == (pow(h,r,p)*G[k-1])%p):
    print("(x_, y_) is indeed a vote for G_"+str(k))
else:
    print("(x_, y_) is not a vote for G_"+str(k))
