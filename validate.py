from random import randint

from numpy.polynomial.polynomial import Polynomial as Poly
import numpy.polynomial.polynomial as polynomial


class SSS(object):
    """
    This class serves as an implementation of Shamir's Secret Sharing scheme,
    which provides methods for managing shared secrets
    """

    @staticmethod
    def l(j, x, k):
        """
        Create a Lagrange basis polynomial
        Reference: https://wikimedia.org/api/rest_v1/media/math/render/svg/6e2c3a2ab16a8723c0446de6a30da839198fb04b
        """

        polys = [
            Poly([-1 * x[m], 1]) / Poly([x[j] - x[m]])
            for m in range(k) if m != j
        ]

        return reduce(lambda acc, p: acc * p, polys, 1)

    @staticmethod
    def L(x, y, k):
        """
        Create a linear combination of Lagrange basis polynomials
        Reference: https://wikimedia.org/api/rest_v1/media/math/render/svg/d07f3378ff7718c345e5d3d4a57d3053190226a0
        """

        return sum([y[j] * SSS.l(j, x, k) for j in range(k)])

    def __init__(self, S, n, k, p):
        """
        S: secret
        n: total number of shares
        k: recovery threshold
        p: prime, where p > S and p > n
        """

        self.S = S
        self.n = n
        self.k = k
        self.p = p

        # Used to generate random coefficients in a production environment
        # production_coefs = [self.S] + [randint(1, self.S) for i in range(1, k)]
        # self.D = self.construct_shares()

        # Making use of the coefficients from Wikipedia's example
        production_coefs = [1234, 166, 94]
        self.production_poly = Poly(production_coefs)

    def construct_shares(self):
        """
        Used to generate shares in a production environment, based on a
        known number of total shares
        """

        return [
            # We use % self.p below to take advantage of finite field arithmetic
            (x, polynomial.polyval(x, self.production_poly.coef) % self.p)
            for x in range(1, self.n + 1)
        ]

    def reconstruct_secret(self, shares):
        """
        Reconstructs a shared secret, given at least self.k of the proper shares
        """

        if len(shares) < self.k:
            raise Exception("Need more participants")

        x = [a for a, b in shares]
        y = [b for a, b in shares]

        # We use % self.p below to take advantage of finite field arithmetic
        return SSS.L(x, y, self.k).coef[0] % self.p
        
def ShamirSecretSharing(n, t, s, q):
    # select t-1 random integers at random
    S = list()
    for _ in range(t-1):
        S_i = random.randint(0, q-1)
        S.append(S_i)

    # Construct a secret polynomial by inserting secret to S[0]
    S = [s] + S

    # Evaluate the polynomial by at n different values of x [1 .. n]
    s_a = list()
    for i in range(1, n+1):  # i is x
        y_i = 0
        for index, S_i in enumerate(S):
            y_i = (y_i + S_i * pow(i, index)) % q
        s_a.append(y_i)

    return s_a

s = ShamirSecretSharing(5,3,9,107)

# quarom = [0,1,2] 
X = 0
a = [0,1,2]
for i in range(3):
    for index, a_i in enumerate([1,2,3]): # get a and index of a
        # calculate lambda for each a
        l = 1 
        for m in a:
            if m != a_i:
                l = l * (m / (m - a_i)) 
        print('lambda: ', l) # debug
        # Omega_a ^ lambda
        X += s[0] * l
print(X == s)