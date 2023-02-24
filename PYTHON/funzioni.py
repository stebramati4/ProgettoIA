import numpy as np
import random

#crea il labirinto nella situazione iniziale
def creaLabirinto(n):
    matrix = []

    for i in range(n):
        row = []
        if i == 0:
            # scegli casualmente tra "G1", "G2" e "V" per ogni cella della prima riga
            scelteR1 = ["G1", "G2"] + ["V"] * (n - 2)
            random.shuffle(scelteR1)
            row = scelteR1
        if i == n - 1:
            scelteRUltimo = ["M"] + ["V"] * (n - 1)
            random.shuffle(scelteRUltimo)
            row = scelteRUltimo
        matrix.append(row)

    # fa array con n*n-2 celle, da usare nella popolazione del corpo
    scelteCorpo = (n - 1) * ["L"] + ["P"] * (n - 2) + (n - 3) * ["F"] + ["I"] + (n * (n - 2) - 3 * (n - 2) - 1) * ["V"]
    random.shuffle(scelteCorpo)

    # popola il corpo della matrice con Invurgus, Ostacoli e Funghi
    for i in range(1, n - 1):
        matrix[i] = scelteCorpo[:5]
        scelteCorpo = scelteCorpo[5:]

    return matrix


# crea la matrice manhattan con le distanze di ogni cella del labirinto al goal più vicino
def manhattan(NP):
    manhattan = np.array(NP)
    G1 = trovaGoal(NP, "G1")
    G2 = trovaGoal(NP, "G2")

    for i in range(NP.shape[0]):
        for j in range(NP.shape[1]):
            manhattan[i][j] = distanzaGoalPiùVicino(G1, G2, i, j)

    return manhattan


#restituisce l'indice y della prima riga, corrispondente alla posizione del goal
def trovaGoal (NP, goal):
    n = len(NP[0])

    firstRow = NP[0]

    for i in range(n):
        if firstRow[i] == goal:
            cella = i

    return cella



# trova Mago nel labirinto, restituisce coordinate
def trovaMago(NP):
    n = len(NP[0])

    for i in range(NP.shape[0]):
        for j in range(NP.shape[1]):
            if NP[i][j] == "M":
                cella = i, j

    return cella


# trova Invurgus nel labirinto, restituisce coordinate
def trovaInvurgus(NP):
    n = len(NP[0])

    for i in range(NP.shape[0]):
        for j in range(NP.shape[1]):
            if NP[i][j] == "I":
                cella = i, j

    return cella

#ritorna la distanza minima
def distanzaGoalPiùVicino(G1, G2, x, y):

    # calcola manhattan dalla cella ai due nodi
    distanzaG1 = distanza(0, G1, x, y)
    distanzaG2 = distanza(0, G2, x, y)

    if distanzaG1 < distanzaG2:
        return distanzaG1
    else:
        return distanzaG2


# calcola la distanza tra due elementi della matrice
def distanza(x1, y1, x2, y2):
    # distanza = | x(mago) - x(invurgus) | + | y(mago) - y(invurgus) |
    distanza = abs(x1 - x2) + abs(y1 - y2)

    return distanza



# stampa la matrice
def stampaMatrice(matrix):
    for row in matrix:
        print(' '.join(row))