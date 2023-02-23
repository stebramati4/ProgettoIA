import random

n = 5
matrix = []

for i in range(n):
    row = []
    if i == 0:
        # scegli casualmente tra "G1", "G2" e "V" per ogni cella della prima riga
        scelteR1 = ["G1", "G2"] + ["V"] * (n - 2)
        random.shuffle(scelteR1)
        row = scelteR1
    if i == n - 1:
        scelteRUltimo = ["M"] + ["V"] * (n - 1)
        random.shuffle(scelteRUltimo)
        row = scelteRUltimo
    matrix.append(row)

# fa array con n*n-2 celle, da usare nella popolazione del corpo
scelteCorpo = (n-1)*["L"] + ["P"] * (n - 2) + (n-3)*["F"] + ["I"] + (n*(n-2) - 3*(n-2)-1)*["V"]
random.shuffle(scelteCorpo)

# popola il corpo della matrice con Invurgus, Ostacoli e Funghi
for i in range(1, n-1):
    matrix[i] = scelteCorpo[:5]
    scelteCorpo = scelteCorpo[5:]

# stampa la matrice
for row in matrix:
    print(row)