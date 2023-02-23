def manhattan(NP):

    manhattan = []
    G1 = trovaGoal(NP, "G1")
    G2 = trovaGoal(NP, "G2")

    for i in range(NP.shape[0]):
        for j in range(NP.shape[1]):
            print(NP[i, j])
            manhattan[i][j] = distanzaGoalPiùVicino(G1, G2, i, j)

    stampaMatrice(manhattan)


    # for ogni cella
        # calcola il goal più vicino
        # trova cella goal
        # calcola distanza dal goal
        # assegnazione

    #return G1 #matrice manhattan


def trovaGoal (matrix, goal):
    n = len(matrix[0])

    firstRow = matrix[0]

    for i in range(n):
        if firstRow[i] == goal:
            cella = i
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

def distanza(x1, y1, x2, y2):
    # distanza = | x(mago) - x(invurgus) | + | y(mago) - y(invurgus) |
    distanza = abs(x1 - x2) + abs(y1 - y2)
    print(distanza)
    return distanza

# stampa la matrice
def stampaMatrice(matrix):
    for row in matrix:
        print(' '.join(row))
