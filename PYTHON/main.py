import numpy as np
import funzioni as f
import greedySearch as gs

# PREDISPOSIZIONE INIZIALE

# definizione dimensione labirinto
n = 5

# predisposizione del labirinto
matrix = f.creaLabirinto(n)
f.stampaMatrice(matrix)
print()
NP = np.array(matrix)

# creazione tabella Manhattan
manhattan = f.manhattan(NP)
print()
f.stampaMatrice(manhattan)

# INIZIO DEL GIOCO

posMago = f.trovaMago(NP)
posInv = f.trovaInvurgus(NP)
print(posMago)
print(posInv)


#############
#percorso = np.array([])
#d = np.array([(1, 2)])
#if len(percorso) == 0:
    #percorso = dir
#else:
    #percorso = np.concatenate(percorso, d)
#print(percorso)
##############

print(gs.controlloCella(manhattan, 4, 4))

print(gs.spostamentoMigliore(NP, manhattan, posMago))

gs.greedySearch(NP, manhattan)