import numpy as np
import funzioni as f
import greedySearch as gs
import aStar as a

# PREDISPOSIZIONE INIZIALE

# definizione dimensione labirinto
n = 8

inp = '0'

while inp != '1' and inp != '2':
    print("MENU' SCELTA")
    print("Digita il numero corrispondente all'algoritmo che vuoi usare:")
    print("1. Greedy Search")
    print("2. Algoritmo A*")
    print()
    inp = input("La tua scelta: ")
    print()
    print()

    # predisposizione del labirinto
    print("Labirinto iniziale:")
    print()
    matrix = f.creaLabirinto(n)
    f.stampaMatrice(matrix)
    print()
    NP = np.array(matrix)
    labirinto = NP.copy()

    # creazione tabella Manhattan
    print("Matrice di Manhattan:")
    print()
    manhattan = f.manhattan(NP)
    f.stampaMatrice(manhattan)
    print()

    if inp == '2':
        print("Matrice delle distanze:")
        print()
        matriceDistanze = a.matriceDistanza(NP)
        f.stampaMatrice(matriceDistanze)
        print()

    if inp == '1':

        # GIOCO GREEDY
        percorsoGreedy = gs.greedySearch(NP, manhattan)
        print("Labirinto iniziale:")
        print()
        f.stampaMatrice(labirinto)

    elif inp == '2':
        #GIOCO A STAR
        percorsoAstar = a.aStar(NP, manhattan, matriceDistanze)
        print(percorsoAstar, "percorso")
        print("Labirinto iniziale:")
        print()
        f.stampaMatrice(labirinto)

    else:
        print("Controlla meglio il tuo inserimento")
        print()


