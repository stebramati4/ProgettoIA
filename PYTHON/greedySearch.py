import funzioni as f
import invurgus as i

# variabile globale per definire quanti il numero di salti sui pozzi senza fondo
conteggioFunghi = 0

# RESTITUISCE: lista (percorso)
def greedySearch(NP, manhattan):
    # trovare percorso greedy per arrivare al goal più vicino

    # bool per goal raggiunto
    finito = False
    catturato = False
    daCella = f.trovaMago(NP)
    percorso = [daCella]
    NotaFinale = ""
    while not finito and not catturato:
        infoMago = spostoMago(NP, manhattan, daCella, percorso)
        daCella = infoMago[0]
        percorso = infoMago[1]
        finito = infoMago[2]

        catturato = i.mossaInvurgus(NP)
        ############################################
        f.stampaMatrice(NP)
        print()
        f.stampaMatrice(manhattan)
        ############################################

    if finito:
        print("Il Mago ha raggiunto l'uscita!")
    elif catturato:
        print("L'Invurgus ha catturato il Mago!")
    print(NotaFinale)
    print(percorso)
    return percorso

# spostamento integrale del mago
#RESTITUISCE: (x, y) (daCella), array (percorso), bool(finito)
def spostoMago(NP, manhattan, daCella, percorso):
    # ripete spostamentoMigliore, mossa e inserimento delle coordinate
    # in array "percorso" finchè non arriva al goal

    aCella, Nota = spostamentoMigliore(NP, manhattan, daCella)
    percorso.append(aCella)
    heur = manhattan[daCella[0]][daCella[1]]
    manhattan[daCella[0]][daCella[1]] = int(heur) + 1

    ret = mossa(NP, daCella, aCella, Nota)

    NP = ret[0]
    if NP[aCella[0]][aCella[1]] == "G1" or NP[aCella[0]][aCella[1]] == "G2":
        finito = True
    else:
        finito = ret[1]
    NotaFinale = ret[2]
    daCella = f.trovaMago(NP)
    return daCella, percorso, finito

# effettua la mossa e aggiorna il labirinto secondo la Nota riportata
# daCella e aCella sono le coordinate di due celle, da dove a dove salta il Mago
# (già controllate negli altri costrutti)
# RESTITUISCE: matrice NP aggiornata
# Note possibili: L, I, V, G, P, PrendiFungo, UsaFungo, UsaPrendiFungo
def mossa(NP, daCella, aCella, Nota):
    global conteggioFunghi
    if NP[daCella[0]][daCella[1]] == 'M':
        NP[daCella[0]][daCella[1]] = 'V'
        if Nota == "PrendiFungo":
            conteggioFunghi = conteggioFunghi + 2
        elif Nota == "UsaFungo":
            conteggioFunghi = conteggioFunghi - 1
        elif Nota == "UsaPrendiFungo":
            conteggioFunghi = conteggioFunghi - 1 + 2
        NP[aCella[0]][aCella[1]] = 'M'

        if Nota == 'G':
            return NP, True, "Hai Vinto! Hai raggiunto l'uscita più vicina"
        elif Nota == 'I':
            return NP, True, "Hai Perso! L'Invurgus ti ha catturato"
        else:
            return NP, False, ""
    else:
        print("Non trovo il mago")


# coordinate spostamento migliore
# RESTITUISCE: (x, y), Nota
def spostamentoMigliore(NP, manhattan, daCella):
    icella = daCella[0]
    jcella = daCella[1]

    listaPesi = []
    NotaIniziale = ""

    if controlloCella(manhattan, icella - 1, jcella):
        # NORD
        valoreCellaN = manhattan[icella-1, jcella]
        heuristicN = int(valoreCellaN.item())               # converto numpy.str_ in intero
        listaPesi.append((heuristicN, (icella-1, jcella), NotaIniziale))

    if controlloCella(manhattan, icella, jcella - 1):
        # OVEST
        valoreCellaO = manhattan[icella, jcella - 1]
        heuristicO = int(valoreCellaO.item())
        listaPesi.append((heuristicO, (icella, jcella - 1), NotaIniziale))

    if controlloCella(manhattan, icella + 1, jcella):
        # SUD
        valoreCellaS = manhattan[icella + 1, jcella]
        heuristicS = int(valoreCellaS.item())
        listaPesi.append((heuristicS, (icella + 1, jcella), NotaIniziale))

    if controlloCella(manhattan, icella, jcella + 1):
        # EST
        valoreCellaE = manhattan[icella, jcella + 1]
        heuristicE = int(valoreCellaE.item())
        listaPesi.append((heuristicE, (icella, jcella + 1), NotaIniziale))

    sorted_list = sorted(listaPesi, key=lambda x: x[0])
    print(sorted_list)

    return sceltaSpostamento(NP, manhattan, daCella, sorted_list)


# sceglie lo spostamento migliore tra i 4 elementi presenti in listaPesi
# listaPesi = array di liste, gli elementi sono della forma (euristica, (coordinateCella), Nota)
# RESTITUISCE: (x, y), Nota
# Note possibili: L, I, V, G, P, PrendiFungo, UsaFungo, UsaPrendiFungo
def sceltaSpostamento(NP, manhattan, daCella, listaOrd):

    if listaOrd[0][2] == "":
        valore = controlloOstacolo(NP, manhattan, listaOrd[0][1], daCella)
        heur = valore[0]
        nota = valore[1]
        if nota == "UsaFungo" or nota == "UsaPrendiFungo":
            cellaPrimoElemento = valore[2]
        else:
            cellaPrimoElemento = listaOrd.pop(0)[1]  # coordinate cella

        nuovoElemento = (int(heur), cellaPrimoElemento, valore[1])
        listaOrd.append(nuovoElemento)
        lista = sorted(listaOrd, key=lambda x: x[0])
        return sceltaSpostamento(NP, manhattan, daCella, lista)
    else:
        return listaOrd[0][1], listaOrd[0][2]


# restituisce un valore di cella (manhattan o 1000 se ostacolo)
# aCella contiene le coordinate di una delle quattro direzioni NSOE
# daCella contiene le coordinate della cella dalla quale salta il personaggio (verso NSOE)
# RESTITUISCE: (valoreManhattan, Nota)
# Note possibili: L, I, V, G, P, PrendiFungo, UsaFungo, UsaPrendiFungo
def controlloOstacolo(NP, manhattan, aCella, daCella):
    global conteggioFunghi
    print(aCella)
    ostacolo = NP[aCella[0], aCella[1]]
    if ostacolo == 'L':
        return 1000, "L", ()

    if ostacolo == 'I':
        return 999, "I", ()

    if ostacolo == 'V':
        heurCella = manhattan[aCella[0]][aCella[1]]
        return int(heurCella), "V", ()

    if ostacolo == 'F':
        heurCella = manhattan[aCella[0]][aCella[1]]
        return int(heurCella), "PrendiFungo", ()

    if ostacolo == 'G1' or ostacolo == 'G2':
        return 0, 'G', ()

    if ostacolo == 'P':
        cellaAtterraggio = saltoPozzo(daCella, aCella)
        # controllo
        if controlloCella(manhattan, cellaAtterraggio[0], cellaAtterraggio[1]):
            ostacoloAtterraggio = NP[cellaAtterraggio[0]][cellaAtterraggio[1]]
            if ostacoloAtterraggio == 'V' or ostacoloAtterraggio == 'F' or ostacoloAtterraggio == 'G1' or ostacoloAtterraggio == 'G2':
                if conteggioFunghi > 0:
                    heurCellaAtterraggio = manhattan[cellaAtterraggio[0]][cellaAtterraggio[1]]
                    if ostacoloAtterraggio == 'F':
                        return int(heurCellaAtterraggio), "UsaPrendiFungo", cellaAtterraggio
                    return int(heurCellaAtterraggio), "UsaFungo", cellaAtterraggio
        return 1000, "P", ()
    return 1000, "Boh", ()


# controlla se le coordinate sono all'interno del labirinto
# icella e jcella = coordinate cella
# RESTITUISCE: True/False
def controlloCella(NP, icella, jcella):
    n = len(NP[0])
    if 0 <= icella < n:
        if 0 <= jcella < n:
            return True
    return False


# calcola le coordinate di atterraggio dopo aver saltato il pozzo
# saltoDa = nel salto del pozzo, cella in cui il Mago è attualmente
# pozzo = coordinate pozzo da saltare
# RESTITUISCE: (x, y)
def saltoPozzo(saltoDa, pozzo):
    xsaltoDa = saltoDa[0]
    xpozzo = pozzo[0]
    ysaltoDa = saltoDa[1]
    ypozzo = pozzo[1]

    diffx = xsaltoDa - xpozzo
    diffy = ysaltoDa - ypozzo

    if diffx == 1:
        # direzione = 'N'
        return pozzo[0]-1, pozzo[1]
    else:
        if diffx == -1:
            # direzione = 'S'
            return pozzo[0]+1, pozzo[1]
        else:
            if diffy == 1:
                # direzione = 'O'
                return pozzo[0], pozzo[1]-1
            else:
                if diffy == -1:
                    # direzione = 'E'
                    return pozzo[0], pozzo[1] + 1
                else:
                    # caso in cui salto due pozzi di fila (IMPOSSIBILE)
                    # forzo il valore di manhattan a 1000
                    return -1, -1
