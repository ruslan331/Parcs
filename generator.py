from random import seed
from random import randint
import string


output_file_name = "in.txt"
f = open(output_file_name, 'w')
N = 50
X = 1e3
seed(1)
f.write(str(N))
f.write('\n')
for i in range(N):
    for j in range(N):
        x = randint(-X, X)
        f.write(str(x))
        f.write(' ')
    f.write('\n')
f.close()