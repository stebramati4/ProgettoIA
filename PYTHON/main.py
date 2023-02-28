import numpy as np
import funzioni as f
import greedySearch as gs
import invurgus as i

# PREDISPOSIZIONE INIZIALE

# definizione dimensione labirinto
n = 5

# predisposizione del labirinto
matrix = f.creaLabirinto(n)
f.stampaMatrice(matrix)
print()
NP = np.array(matrix)
labirinto = NP.copy()

# creazione tabella Manhattan
manhattan = f.manhattan(NP)
print()
f.stampaMatrice(manhattan)

# GIOCO GREEDY
percorsoGreedy = gs.greedySearch(NP, manhattan)
f.stampaMatrice(labirinto)
