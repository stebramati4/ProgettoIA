import numpy as np
import funzioni as f

n = 5

matrix = f.creaLabirinto(n)
f.stampaMatrice(matrix)
print()
NP = np.array(matrix)

manhattan = f.manhattan(NP)
print()
f.stampaMatrice(manhattan)