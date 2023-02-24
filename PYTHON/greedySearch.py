import numpy as np
import funzioni as f

def greedySearch(NP, manhattan):
    # trovare percorso greedy per arrivare al goal più vicino

    # bool per goal raggiunto
    finito = False
    StartMago = f.trovaMago(NP)
    percorso = []
    while finito == False:
        spostamentoMigliore(NP, manhattan, StartMago)




        #posMago = f.trovaMago(NP)
        ######################################### da sistemare il percorso, utilizziamo le stampe per ora
        #dir = np.array(spostamentoMigliore(manhattan, posMago))
        #if len(percorso) == 0:
            #percorso = dir
        #else:
            #ercorso = np.concatenate(percorso, dir)
    # while bool == false
        # migliore tra celle adiacenti NSOE
        # controllo cella accessibile



# coordinate spostamento migliore
def spostamentoMigliore(NP, manhattan, cella):
    icella = cella[0]
    jcella = cella[1]

    heuristicN = 1000
    heuristicO = 1000
    heuristicS = 1000
    heuristicE = 1000

    minimo = 0

    listaPesi = []

    if controlloCella(manhattan, icella - 1, jcella):
        #NORD
        heuristicN = manhattan[icella-1, jcella]

    if controlloCella(manhattan, icella, jcella - 1):
        #OVEST
        heuristicO = manhattan[icella, jcella - 1]

    if controlloCella(manhattan, icella + 1, jcella):
        #SUD
        heuristicS = manhattan[icella + 1, jcella]

    if controlloCella(manhattan, icella, jcella + 1):
        #EST
        heuristicE = manhattan[icella, jcella + 1]

    listaPesi = [(heuristicN, (icella - 1, jcella)), (heuristicO, (icella, jcella - 1)),
                 (heuristicS, (icella + 1, jcella)), (heuristicE, (icella, jcella + 1))]

    sorted_list = sorted(listaPesi, key=lambda x: x[0])

    controlloOstacolo(NP, manhattan, sorted_list[0][1][0], sorted_list[0][1][1])


def controlloCella(manhattan, icella, jcella):
    n = len(manhattan)
    print(n)
    if icella >= 0 and icella < n:
        if jcella >= 0 and jcella < n:
            return True
    return False


def controlloOstacolo(NP, manhattan, i, j):
    ostacolo = NP[i,j]
    if ostacolo == 'L':
        return 1000
    if ostacolo == 'P':
        if controlloCella(manhattan, i, j):
            return


#def mossa: