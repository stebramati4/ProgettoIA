import funzioni as f
import greedySearch as g

# Contiene il carattere della matrice prima che l'Invurgus saltasse sulla cella attuale
InvPrecedente = 'V'


# effettua la mossa dell'Invurgus in base alla distanza più piccola dal mago
# oppure in base alla cella in senso antiorario
def mossaInvurgus(NP):
    global InvPrecedente

    catturato = False
    daCella = f.trovaInvurgus(NP)
    spostamento = spostamentoMiglioreInv(NP, daCella)
    aCella = spostamento[0]
    Nota = spostamento[1]

    NP[aCella[0]][aCella[1]] = 'I'
    NP[daCella[0]][daCella[1]] = InvPrecedente

    if Nota == 'F':
        InvPrecedente = 'V'
        print("Oh no! L'Invurgus ha calpestato il fungo!")
        print()
    elif Nota == 'M':
        InvPrecedente = 'M'
        print("L'Invurgus ha catturato il mago!")
        print()
        catturato = True
    else:
        InvPrecedente = Nota
    return catturato


# coordinate spostamento migliore
# RESTITUISCE: (x, y), Nota
def spostamentoMiglioreInv(NP, daCella):
    icella = daCella[0]
    jcella = daCella[1]
    xMago = -1
    yMago = -1

    listaPesi = []
    posMago = f.trovaMago(NP)
    if posMago != False:
        xMago = posMago[0]
        yMago = posMago[1]

    if g.controlloCella(NP, icella - 1, jcella):
        # NORD
        valoreCellaN = f.distanza(icella-1, jcella, xMago, yMago)
        heuristicN = int(valoreCellaN)               # converto numpy.str_ in intero
        listaPesi.append((heuristicN, "N", (icella-1, jcella)))

    if g.controlloCella(NP, icella, jcella - 1):
        # OVEST
        valoreCellaO = f.distanza(icella, jcella - 1, xMago, yMago)
        heuristicO = int(valoreCellaO)
        listaPesi.append((heuristicO, "O", (icella, jcella - 1)))

    if g.controlloCella(NP, icella + 1, jcella):
        # SUD
        valoreCellaS = f.distanza(icella + 1, jcella, xMago, yMago)
        heuristicS = int(valoreCellaS)
        listaPesi.append((heuristicS, "S", (icella + 1, jcella)))

    if g.controlloCella(NP, icella, jcella + 1):
        # EST
        valoreCellaE = f.distanza(icella, jcella + 1, xMago, yMago)
        heuristicE = int(valoreCellaE)
        listaPesi.append((heuristicE, "E", (icella, jcella + 1)))

    lista = listaPesi
    sorted_list = sorted(listaPesi, key=lambda x: x[0])
    #print(sorted_list)

    return sceltaSpostamento(NP, sorted_list, lista, daCella)


# sceglie lo spostamento migliore tra i 4 elementi presenti in listaPesi
# listaPesi = array di liste, gli elementi sono della forma (euristica, (coordinateCella), Nota)
# RESTITUISCE: (x, y), Nota
# Note possibili: L, I, V, G, P, PrendiFungo, UsaFungo, UsaPrendiFungo
def sceltaSpostamento(NP, listaOrd, lista, daCella):

    valore = controlloOstacolo(NP, listaOrd[0][2], int(listaOrd[0][0]))
    nota = valore[1]
    cella = listaOrd[0][2]

    if nota == 'M' or nota == 'V' or nota == 'F' or nota == 'G1' or nota == 'G2':
        return cella, nota

    direzione = listaOrd.pop(0)[1]  # coordinate cella
    listaAO = roll(lista, direzione)

    elemLista = []
    listaAO.pop(0)
    trovato = False
    bloccato = False
    while not trovato and not bloccato:
        if not listaAO:
            print("Invurgus bloccato")
            print()
            bloccato = True
        else:
            elemLista = listaAO.pop(0)
            infoOstacolo = controlloOstacolo(NP, elemLista[2], elemLista[0])
            if infoOstacolo[0] != 1000:
                trovato = True
    if bloccato:
        cella = daCella
        nota = 'I'
    else:
        cella = elemLista[2]
        nota = NP[cella[0]][cella[1]]
    return cella, nota


def roll(listaAO, direzione):
    while direzione != listaAO[0][1]:
        primoEl = listaAO.pop(0)
        listaAO.append(primoEl)
    return listaAO


# restituisce un valore di cella (manhattan o 1000 se ostacolo)
# aCella contiene le coordinate di una delle quattro direzioni NSOE
# daCella contiene le coordinate della cella dalla quale salta il personaggio (verso NSOE)
# RESTITUISCE: (distanza, Nota)
# Note possibili: L, I, V, G, P, PrendiFungo, UsaFungo, UsaPrendiFungo
def controlloOstacolo(NP, aCella, distanza):

    #print(aCella)
    ostacolo = NP[aCella[0], aCella[1]]
    if ostacolo == 'L':
        return 1000, "L"

    if ostacolo == 'M':
        return distanza, "M"

    if ostacolo == 'V':
        return distanza, "V"

    if ostacolo == 'F':
        return distanza, "F"

    if ostacolo == 'G1':
        return distanza, 'G1'

    if ostacolo == 'G2':
        return distanza, 'G2'

    if ostacolo == 'P':
        return 1000, "P"
    return 1000, "Boh"
