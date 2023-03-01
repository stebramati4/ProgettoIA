import funzioni as f
import numpy as np
import greedySearch as gs
import heapq

def aStar(NP, manhattan, matriceDistanze):
    start = f.trovaMago(NP)
    ostacolo = NP[start]
    G1 = (0, f.trovayGoal(NP, "G1"))
    G2 = (0, f.trovayGoal(NP, "G2"))

    open_list = []

    heapq.heappush(open_list, (0, start, ostacolo))

    g_score = {start: 0}
    f_score = {start: euristica_fn(manhattan, start)}

    while open_list:
        current_cost, current_node, ostacolo = heapq.heappop(open_list)

        if current_node == G1 or current_node == G2:
            percorso = []
            while current_node != start:
                percorso.append(current_node)
                current_node = came_from[current_node]  #FUNZIONE CHE RITORNA LA CELLA DA CUI SIAMO PASSATI APPENA PRIMA
            percorso.append(start)
            percorso.reverse()
            return percorso

        for item in vicini_fn(manhattan, current_node):
            tentative_g_score = g_score[current_node] + dist_between(matriceDistanze, current_node, item)

            if item not in g_score or tentative_g_score < g_score[item]:
                g_score[item] = tentative_g_score
                f_score[item] = tentative_g_score + euristica_fn(item)
                if controlloOstacolo(NP, item):
                    heapq.heappush(open_list, (f_score[item], item))

    return None


def dist_between(MD, cella, vicino):
    distanzaCella = MD[cella[0]][cella[1]]
    distanzaVicino = MD[vicino[0]][vicino[1]]

    distanza = abs(distanzaVicino - cella)

    return distanza


def controlloOstacolo(NP, item):
    ostacolo = NP[item]

    if ostacolo == 'L':
        return False

    return True


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
