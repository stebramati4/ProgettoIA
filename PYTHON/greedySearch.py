import numpy as np
import funzioni as f

def greedySearch(NP, manhattan, SMago):
    # trovare percorso greedy per arrivare al goal più vicino

    # bool per goal raggiunto
    finito = False
    StartMago = f.trovaMago(NP)
    percorso = []
    while finito == False:
        posMago = f.trovaMago(NP)
        ######################################### da sistemare il percorso, utilizziamo le stampe per ora
        dir = np.array(spostamentoMigliore(manhattan, posMago))
        if len(percorso) == 0:
            percorso = dir
        else:
            percorso = np.concatenate(percorso, dir)
    # while bool == false
        # migliore tra celle adiacenti NSOE
        # controllo cella accessibile



# coordinate spostamento migliore
def spostamentoMigliore

def controlloCella

def mossa