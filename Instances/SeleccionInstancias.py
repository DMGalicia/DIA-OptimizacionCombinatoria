import random
import os

# Script para seleccionar un porcentaje aleatoriamente de cada grupo de instancias
c = 0.10

# Subclases de instancias
subclases = ['N1c1w1','N1c1w2','N1c1w4','N1c2w1','N1c2w2','N1c2w4','N1c3w1','N1c3w2','N1c3w4','N2c1w1','N2c1w2','N2c1w4','N2c2w1','N2c2w2','N2c2w4','N2c3w1','N2c3w2','N2c3w4','N3c1w1','N3c1w2','N3c1w4','N3c2w1','N3c2w2','N3c2w4','N3c3w1','N3c3w2','N3c3w4','N4c1w1','N4c1w2','N4c1w4','N4c2w2','N4c2w2','N4c2w4','N4c3w1','N4c3w2','N4c3w4','N1w1b1','N1w1b2','N1w1b3','N1w2b1','N2w2b2','N1w2b3','N1w3b1','N1w3b2','N1w3b3','N1w4b1','N1w4b2','N1w4b3','N2w1b1','N2w1b2','N2w1b3','N2w2b1','N2w2b2','N2w2b3','N2w3b1','N2w3b2','N2w3b3','N2w4b1','N2w4b2','N2w4b3','N3w1b1','N3w1b2','N3w1b3','N3w2b1','N3w2b2','N3w2b3','N3w3b1','N3w3b2','N3w3b3','N3w4b1','N3w4b2','N3w4b3','N4w1b1','N4w1b2','N4w1b3','N4w2b1','N4w2b2','N4w2b3','N4w3b1','N4w3b2','N4w3b3','N4w4b1','N4w4b2','N4w4b3','Hard','t60','t120','t249','t501','u120','u250','u500','u1000','hBPP','BPP','BPP_','TEST']
# Ruta donde se encuentran las instancias
path ='Instances/'
# Lista de instancias seleccionadas
lst = []
# Por cada subclase
for s in subclases:
    # Extraer las instancias de la ruta seleccionada
    if (s != 'BPP'):
        aux = [f for f in os.listdir(path) if (f.endswith(".txt") and (s in f))]
    else:
        aux = [f for f in os.listdir(path) if (f.endswith(".txt") and (s in f) and not('BPP_' in f) and not('hBPP' in f))]
    # Proporción de instancias necesarias
    p = round(len(aux)*c)
    # Lista para almacenar las instancias seleccionadas
    auxaux = []
    n = 0
    # Ciclo que selecciona los índices 
    while True:
        if (random.random() <= c):
            if not(n in auxaux):
                auxaux.append(n)
        n+=1
        # Condición de paro
        if (len(auxaux) >= p):
            break
        # Reinicio del contador
        if (n==len(aux)):
            n=0
    # Añade los nombres de las instancias
    for i in auxaux:
        lst.append(aux[i])
# Impresión de los nombres
print(lst)

