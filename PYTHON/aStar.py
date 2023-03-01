import funzioni as f
import numpy as np
import greedySearch as gs
import heapq

# variabile globale per definire quanti il numero di salti sui pozzi senza fondo
conteggioFunghi = 0

def aStar(NP, manhattan, matriceDistanze):
    start = f.trovaMago(NP)
    ostacolo = NP[start]
    G1 = (0, f.trovayGoal(NP, "G1"))
    G2 = (0, f.trovayGoal(NP, "G2"))

    open_list = []

    heapq.heappush(open_list, (0, start, ostacolo))

    g_score = {start: 0}
    f_score = {start: euristica_fn(manhattan, start)}
    came_from = {start: None}

    while open_list:
        print(open_list, 'open_list')
        current_cost, current_node, ostacolo = heapq.heappop(open_list)

        if current_node == G1 or current_node == G2:
            print('start = a uno dei goal')
            percorso = []
            while current_node != start:
                print('while del if dove start = a uno dei goal')
                percorso.append(current_node)
                current_node = came_from[current_node]
            percorso.append(start)
            percorso.reverse()
            return percorso

        for vicino in vicini_fn(manhattan, current_node):
            print('ciclo i vicini')
            print(vicino)
            tentative_g_score = g_score[current_node] + dist_between(matriceDistanze, current_node, vicino)

            print(g_score[current_node], 'g_score')
            print(dist_between(matriceDistanze, current_node, vicino), 'distanza tra celle')
            print(tentative_g_score, 'tentative_g_score')

            if vicino not in g_score or tentative_g_score < g_score[vicino]:
                print('if dei vicini')
                g_score[vicino] = int(tentative_g_score)
                print(g_score , "g_score")
                f_score[vicino] = int(tentative_g_score) + int(euristica_fn(manhattan, vicino))
                print(f_score , "f_score")

                ostacolo = controlloOstacolo(NP, current_node, vicino)
                print(ostacolo)

                if ostacolo == 'V' or ostacolo == 'F' or ostacolo == 'G1' or ostacolo == 'G2':
                    print('if controllo ostacolo')
                    came_from[vicino] = current_node
                    heapq.heappush(open_list, (f_score[vicino], vicino, ostacolo))
                elif ostacolo == 'P':
                    print('elif controllo ostacolo pozzo')
                    if conteggioFunghi > 0:
                        print('if conteggio funghi')
                        cellaAtterraggio = controlloDopoPozzo(NP, current_node, vicino)
                        if cellaAtterraggio is not None:
                            print('if cella atterraggio none')
                            came_from[cellaAtterraggio] = current_node
                            heapq.heappush(open_list, (f_score[cellaAtterraggio], cellaAtterraggio, ostacolo))
                        else:
                            print("Non c'è una cella dopo il pozzo")

    return None


def dist_between(MD, cella, vicino):
    distanzaCella = int(MD[cella[0]][cella[1]])
    distanzaVicino = int(MD[vicino[0]][vicino[1]])

    distanza = abs(distanzaVicino - distanzaCella)

    return distanza


def controlloOstacolo(NP, daCella, aCella):
    global conteggioFunghi

    ostacolo = NP[aCella[0], aCella[1]]
    if ostacolo == 'L':
        return "L"

    if ostacolo == 'I':
        return "I"

    if ostacolo == 'V':
        return "V"

    if ostacolo == 'F':
        conteggioFunghi = conteggioFunghi + 2
        return "F"

    if ostacolo == 'G1':
        return 'G1'

    if ostacolo == 'G2':
        return 'G2'

    if ostacolo == 'P':
        return "P"


def controlloDopoPozzo(NP, daCella, aCella):
    global conteggioFunghi
    cellaAtterraggio = gs.saltoPozzo(daCella, aCella)
    # controllo
    if gs.controlloCella(NP, cellaAtterraggio[0], cellaAtterraggio[1]):
        ostacoloAtterraggio = NP[cellaAtterraggio[0]][cellaAtterraggio[1]]
        if ostacoloAtterraggio == 'V' or ostacoloAtterraggio == 'F' or ostacoloAtterraggio == 'G1' or ostacoloAtterraggio == 'G2':
            if ostacoloAtterraggio == 'F':
                conteggioFunghi = conteggioFunghi - 1 + 2
                return cellaAtterraggio
            elif ostacoloAtterraggio == "G1" or ostacoloAtterraggio == "G2":
                conteggioFunghi = conteggioFunghi - 1
                return cellaAtterraggio
            else:
                conteggioFunghi = conteggioFunghi - 1
                return cellaAtterraggio
    return None

def spostamentoMigliore(open_list):
    current_cost, current_node, ostacolo = heapq.heappop(open_list)

    if ostacolo == 'L':
        # Creare una copia dell'heap
        new_heap = list(open_list)
        # Rimuovere l'elemento dalla copia dell'heap
        new_heap.remove(5)
        # Ricostruire l'heap
        heapq.heapify(new_heap)
        return spostamentoMigliore(new_heap)


def vicini_fn(manhattan, cella):
    icella = cella[0]
    jcella = cella[1]

    vicini = []

    if gs.controlloCella(manhattan, icella - 1, jcella):
        # NORD
        cella = (icella - 1, jcella)
        vicini.append(cella)

    if gs.controlloCella(manhattan, icella, jcella - 1):
        # OVEST
        cella = (icella, jcella - 1)
        vicini.append(cella)

    if gs.controlloCella(manhattan, icella + 1, jcella):
        # SUD
        cella = (icella + 1, jcella)
        vicini.append(cella)

    if gs.controlloCella(manhattan, icella, jcella + 1):
        # EST
        cella = (icella, jcella + 1)
        vicini.append(cella)

    return vicini


def euristica_fn(manhattan, cella):
    heuristic = manhattan[cella[0]][cella[1]]
    return heuristic


def matriceDistanza(NP):
    MD = np.array(NP)
    start = f.trovaMago(NP)

    for i in range(NP.shape[0]):
        for j in range(NP.shape[1]):
            MD[i][j] = f.distanza(start[0], start[1], i, j)

    return MD