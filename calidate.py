import random

k = 2
j = 1
q = 1213739201406691053111461418952562906605807973221
C = random.randint(0,q-1)

arr = []

c1 = random.randint(0, q-1)
c2 = random.randint(0, q-1)

arr = [C-c2, C-c1]

print(arr)
print(C == (sum(arr) % p))
print('C: ', C)
print('s:', sum(arr) % q)
