import numpy as np
import funzioni as f

# variabile globale per definire quanti il numero di salti sui pozzi senza fondo
conteggioFunghi = 0

def greedySearch(NP, manhattan):
    # trovare percorso greedy per arrivare al goal più vicino

    # bool per goal raggiunto
    finito = False
    StartMago = f.trovaMago(NP)
    percorso = []
    while finito == False:
        ############################################
        # ripete spostamentoMigliore, mossa e inserimento delle coordinate
        # in array "percorso" finchè non arriva al goal
        spostamentoMigliore(NP, manhattan, StartMago)
        ############################################



        #posMago = f.trovaMago(NP)
        ######################################### da sistemare il percorso, utilizziamo le stampe per ora
        #dir = np.array(spostamentoMigliore(manhattan, posMago))
        #if len(percorso) == 0:
            #percorso = dir
        #else:
            #ercorso = np.concatenate(percorso, dir)




# coordinate spostamento migliore

def spostamentoMigliore(NP, manhattan, daCella):
    icella = daCella[0]
    jcella = daCella[1]

    heuristicN = 1000
    heuristicO = 1000
    heuristicS = 1000
    heuristicE = 1000

    minimo = 0
    listaPesi = []

    if controlloCella(manhattan, icella - 1, jcella):
        #NORD
        valoreCellaN = manhattan[icella-1, jcella]
        heuristicN = int(valoreCellaN.item())               #converto numpy.str_ in intero

    if controlloCella(manhattan, icella, jcella - 1):
        #OVEST
        valoreCellaO = manhattan[icella, jcella - 1]
        heuristicO = int(valoreCellaO.item())

    if controlloCella(manhattan, icella + 1, jcella):
        #SUD
        valoreCellaS = manhattan[icella + 1, jcella]
        heuristicS = int(valoreCellaS.item())

    if controlloCella(manhattan, icella, jcella + 1):
        #EST
        valoreCellaE = manhattan[icella, jcella + 1]
        heuristicE = int(valoreCellaE.item())

    NotaIniziale = ""
    # listaPesi ha elementi del tipo (euristica, (coordinate))
    listaPesi = [(heuristicN, (icella - 1, jcella), NotaIniziale),
                 (heuristicO, (icella, jcella - 1), NotaIniziale),
                 (heuristicS, (icella + 1, jcella), NotaIniziale),
                 (heuristicE, (icella, jcella + 1), NotaIniziale)]

    sorted_list = sorted(listaPesi, key=lambda x: x[0])

    print(sorted_list)

    ##################################
    coordinateSpostamento = sceltaSpostamento(NP, manhattan, listaPesi)
    ##################################

# sceglie lo spostamento migliore tra i 4 elementi presenti in listaPesi
# listaPesi = array di liste, gli elementi sono della forma (euristica, (coordinateCella), Nota)
# RESTITUISCE: (x, y), Nota
# Note possibili: L, I, V, G, P, PrendiFungo, UsaFungo, UsaPrendiFungo
def sceltaSpostamento(NP, manhattan, listaPesi):
    ####################################
    # In un ciclo successivo, se il primo elemento della lista ha una nota significa che è il migliore
    # per cui posso terminare il ciclo
    ####################################



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
            conteggioFunghi = conteggioFunghi +2
        elif Nota == "UsaFungo":
            conteggioFunghi = conteggioFunghi -1
        elif Nota == "UsaPrendiFungo":
            conteggioFunghi = conteggioFunghi -1 +2
        NP[aCella[0]][aCella[1]] = 'M'
        return NP
    else:
        print("Non trovo il mago")

# controlla se le coordinate sono all'interno del labirinto
# icella e jcella = coordinate cella
# RESTITUISCE: True/False
def controlloCella(manhattan, icella, jcella):
    n = len(manhattan)
    print(n)
    if icella >= 0 and icella < n:
        if jcella >= 0 and jcella < n:
            return True
    return False

# restituisce un valore di cella (manhattan o 1000 se ostacolo)
# aCella contiene le coordinate di una delle quattro direzioni NSOE
# daCella contiene le coordinate della cella dalla quale salta il personaggio (verso NSOE)
# RESTITUISCE: (valoreManhattam, Nota)
# Note possibili: L, I, V, G, P, PrendiFungo, UsaFungo, UsaPrendiFungo
def controlloOstacolo(NP, manhattan, aCella, daCella):
    global conteggioFunghi
    ostacolo = NP[aCella[0], aCella[1]]
    if ostacolo == 'L':
        return (1000, "L")

    if ostacolo == 'I':
        return (999, "I")

    if ostacolo == 'V':
        heurCella = manhattan[aCella[0]][aCella[1]]
        return (heurCella, "V")

    if ostacolo == 'F':
        heurCella = manhattan[aCella[0]][aCella[1]]
        return (heurCella, "PrendiFungo")

    if ostacolo == 'G1' or ostacolo == 'G2':
        return (0, 'G')

    if ostacolo == 'P':
        cellaAtterraggio = saltoPozzo(daCella, aCella)
        # controllo
        if controlloCella(manhattan, cellaAtterraggio[0], cellaAtterraggio[1]):
            ostacoloAtterraggio = NP[cellaAtterraggio[0]][cellaAtterraggio[1]]
            if ostacoloAtterraggio == 'V' or ostacoloAtterraggio == 'F' or ostacoloAtterraggio == 'G1' or ostacoloAtterraggio == 'G2':
                if conteggioFunghi > 0:
                    heurCellaAtterraggio = manhattan[cellaAtterraggio[0]][cellaAtterraggio[1]]
                    if ostacoloAtterraggio == 'F':
                        return (heurCellaAtterraggio, "UsaPrendiFungo")
                    return (heurCellaAtterraggio, "UsaFungo")
        return (1000, "P")


# calcola le coordinate di atterraggio dopo aver saltato il pozzo
# saltoDa = nel salto del pozzo, cella in cui il Mago è attualmente
# pozzo = coordinate pozzo da saltare
# RESTITUISCE: (x, y)
def saltoPozzo(saltoDa, pozzo):
    diff = saltoDa - pozzo
    if diff[0] == 1:
        # direzione = 'N'
        return (pozzo[0]-1, pozzo[1])
    else:
        if diff[0] == -1:
            # direzione = 'S'
            return (pozzo[0]+1, pozzo[1])
        else:
            if diff[1] == 1:
                #direzione = 'O'
                return (pozzo[0], pozzo[1]-1)
            else:
                if diff[1] == -1:
                    # direzione = 'E'
                    return (pozzo[0],pozzo[1]+1)
                else:
                    # caso in cui salto due pozzi di fila (IMPOSSIBILE)
                    # forzo il valore di manhattan a 1000
                    return (-1, -1)