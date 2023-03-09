import funzioni as f
import numpy as np
import greedySearch as gs
import invurgus as i
import heapq

# variabile globale per definire quanti il numero di salti sui pozzi senza fondo
conteggioFunghi = 0


def aStar(NP, manhattan, matriceDistanze):
    start = f.trovaMago(NP)
    ostacolo = NP[start]
    G1 = (0, f.trovayGoal(NP, "G1"))
    G2 = (0, f.trovayGoal(NP, "G2"))

    finito = False
    catturato = False

    open_list = []

    heapq.heappush(open_list, (0, start, ostacolo))

    g_score = {start: 0}
    f_score = {start: euristica_fn(manhattan, start)}
    came_from = {start: None}

    passo = 1

    while open_list and not finito and not catturato:
        current_cost, current_node, ostacolo = heapq.heappop(open_list)

        if current_node == G1 or current_node == G2:
            percorso = []
            while current_node != start:
                percorso.append(current_node)
                current_node = came_from[current_node]
            percorso.append(start)
            percorso.reverse()
            print("Il mago ha trovato l'uscita")
            print()
            return percorso

        for vicino in vicini_fn(NP, current_node):
            if gs.controlloCella(NP, vicino[0], vicino[1]):
                tentative_g_score = g_score[current_node] + dist_between(matriceDistanze, current_node, vicino)

            if vicino not in g_score or tentative_g_score < g_score[vicino]:
                g_score[vicino] = int(tentative_g_score)
                f_score[vicino] = int(tentative_g_score) + int(euristica_fn(manhattan, vicino))

                ostacolo = controlloOstacolo(NP, vicino)

                if ostacolo == 'V' or ostacolo == 'F' or ostacolo == 'G1' or ostacolo == 'G2':
                    came_from[vicino] = current_node
                    heapq.heappush(open_list, (f_score[vicino], vicino, ostacolo))
                elif ostacolo == 'P':
                    if conteggioFunghi > 0:
                        cellaAtterraggio = controlloDopoPozzo(NP, current_node, vicino)
                        if cellaAtterraggio is not None:

                            g_scoreCellaAtt, f_scoreCellaAtt = calcoloCosti(matriceDistanze, manhattan, g_score[current_node], current_node, cellaAtterraggio)

                            g_score[cellaAtterraggio] = g_scoreCellaAtt
                            f_score[cellaAtterraggio] = f_scoreCellaAtt

                            came_from[cellaAtterraggio] = current_node
                            heapq.heappush(open_list, (f_score[cellaAtterraggio], cellaAtterraggio, ostacolo))

        if heapq:
            elementoMigliore = heapq.heappop(open_list)

            while open_list:
                heapq.heappop(open_list)
            heapq.heappush(open_list, elementoMigliore)

            cellaMigliore = elementoMigliore[1]

            mossaMago(NP, current_node, cellaMigliore)

        catturato = i.mossaInvurgus(NP)

        print("------- Passo ", passo, " ----------")
        print()
        f.stampaMatrice(NP)
        print()
        passo = passo + 1

    return None


#Funzione che aggiorna la posizione del Mago
def mossaMago(NP, daCella, aCella):
    if NP[daCella[0]][daCella[1]] == 'M':
        NP[daCella[0]][daCella[1]] = 'V'
        NP[aCella[0]][aCella[1]] = 'M'
    else:
        return False

#Funzione che calcola la distanza tra 2 celle
#Restituisce il valore della distanza calcolata
def dist_between(MD, cella, vicino):
    distanzaCella = int(MD[cella[0]][cella[1]])
    distanzaVicino = int(MD[vicino[0]][vicino[1]])

    distanza = abs(distanzaVicino - distanzaCella)

    return distanza

#Funzione calcola il g_score e l'f_score
#Restituisce i valori calcolati di g_scoreACella e f_scoreACella
def calcoloCosti(MD, MN, g_scoreDaCella, daCella, aCella):
    tentative_g_score = g_scoreDaCella + dist_between(MD, daCella, aCella)
    g_scoreACella = int(tentative_g_score)
    f_scoreACella = int(tentative_g_score) + int(euristica_fn(MN, aCella))

    return g_scoreACella, f_scoreACella


#Data la cella la funzione andrà a verificate cosa è contenuto in quella cella
#Restituisce la nota che rappresenta l'ostacolo
def controlloOstacolo(NP, aCella):
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


#Controllo la cella dopo il pozzo
#Restituisce la cella dove deve atterrare il mago dopo il salto del pozzo
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


#crea una lista contenente le celle vicine alla cella le gli passo
def vicini_fn(NP, cella):
    icella = cella[0]
    jcella = cella[1]

    vicini = []

    if gs.controlloCella(NP, icella - 1, jcella):
        # NORD
        cella = (icella - 1, jcella)
        vicini.append(cella)

    if gs.controlloCella(NP, icella, jcella - 1):
        # OVEST
        cella = (icella, jcella - 1)
        vicini.append(cella)

    if gs.controlloCella(NP, icella + 1, jcella):
        # SUD
        cella = (icella + 1, jcella)
        vicini.append(cella)

    if gs.controlloCella(NP, icella, jcella + 1):
        # EST
        cella = (icella, jcella + 1)
        vicini.append(cella)

    return vicini


#Restituisce l'euristica della cella
def euristica_fn(manhattan, cella):
    heuristic = manhattan[cella[0]][cella[1]]
    return heuristic


#Crea la matrice contenente le distanze
def matriceDistanza(NP):
    MD = np.array(NP)
    start = f.trovaMago(NP)

    for i in range(NP.shape[0]):
        for j in range(NP.shape[1]):
            MD[i][j] = f.distanza(start[0], start[1], i, j)

    return MD
