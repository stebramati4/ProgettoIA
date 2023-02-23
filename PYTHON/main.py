import numpy as np
import funzioni as f


# PREDISPOSIZIONE INIZIALE

#definizione dimensione labirinto
n = 5

#predisposizione del labirinto
matrix = f.creaLabirinto(n)
f.stampaMatrice(matrix)
print()
NP = np.array(matrix)

#creazione tabella Manhattan
manhattan = f.manhattan(NP)
print()
f.stampaMatrice(manhattan)

#INIZIO DEL GIOCO