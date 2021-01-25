import pandas as pd
import numpy as np
import random
import time
import copy
import os

def readInstance(name):
    # Función para leer una instancia, recibe el nombre del archivo
    # Apertura del archivo con datos de la instancia
    file = open(name, 'r') 
    lines = file.readlines() 
    # Variable de apoyo para identificar los datos
    count = 0
    # Variables de interes: número de objetos, capacidad de los contenedores y pesos de los objetos
    n_items = 0
    bin_capacity = 0
    weights = []
    # Lectura de las líneas del archivo
    for line in lines:
        # Lectura del número de objetos en la línea 1
        if count == 1:
            n_items = int(line.strip())
        # Lectura de la capacidad de los contenedores en la línea 3
        elif count == 3:
            bin_capacity = float(line.strip())
        # Lectura de los pesos de los objetos en la línea 7 en adelante
        elif count > 6:
            weights.append(float(line.strip()))
        count += 1
    # Cerrado del archivo con datos de la instancia
    file.close()
    # Return de las variables de interés
    return n_items, bin_capacity, weights

def readInstanceModified(name,escale):
    # Función para leer una instancia,recibe el nombre del archivo
    # Apertura del archivo con datos de la instancia
    file = open(name,'r') 
    lines = file.readlines() 
    # Variable de apoyo para identificar los datos
    count = 0
    # Variables de interes: número de objetos,capacidad de los contenedores y pesos de los objetos
    n_items = 0
    bin_capacity = 0
    weights = []
    # Lectura de las líneas del archivo
    for line in lines:
        # Lectura del número de objetos en la línea 1
        if count == 1:
            n_items = int(line.strip())
        # Lectura de la capacidad de los contenedores en la línea 3
        elif count == 3:
            bin_capacity = int(float(line.strip())*escale)
        # Lectura de los pesos de los objetos en la línea 7 en adelante
        elif count > 6:
            weights.append(int(float(line.strip())*escale))
        count += 1
    # Cerrado del archivo con datos de la instancia
    file.close()
    # Return de las variables de interés
    return n_items,bin_capacity,weights

def evaluateSolution(s,w,bc):
    # Función para evaluar una solución s, también recibe un vector de pesos w y la capacidad de los contenedores bc
    # Variables de interés, numero de contendores, pesos de cada contenedor, puntaje de la solución
    n_bins = 1
    solution = []
    bin_weights = []
    score = 0
    # Variables de apoyo:
    # total_weight que lleva el peso de un contenedor actual
    # aux que representa los objetos en un contenedor actual
    total_weight = 0
    aux = []
    # Ciclo que permite determinar el número de contenedores, el peso de cada uno, el número de objetos por contenedor y el puntaje de la solución
    # Por cada objeto en la solución
    for item in s:
        # Si el contenedor actual tiene capacidad para almacenar el objeto item de la solución s
        if (total_weight + w[item] <= bc):
            # Agregar el peso del objeto al contenedor
            total_weight += w[item]
            # Agregar el objeto al contenedor
            aux.append(item)
        else:
            # En caso de que no entre el objeto item, se agrega el peso del contenedor acual a la lista de pesos
            bin_weights.append(total_weight)
            # La representación del contenedor se agrega a la solución
            solution.append(aux)
            # Se crea otro contenedor
            n_bins +=1
            # Se define el peso del contenedor nuevo con el último objeto que no cupo
            total_weight = w[item]
            # Se agrega al contenedor nuevo el último objeto que no cupo
            aux = [item]
    # Se agrega el peso del último contenedor
    bin_weights.append(total_weight)
    # Se agrega la representación del último contenedor
    solution.append(aux)
    # Ciclo para calcular el puntaje de la solución
    # Se suman la la división elevada al cuadrado de cada peso del contenedor sobre la capacidad máxima
    for j in bin_weights:
        score += (j/bc)**2
    # Se divide entre el número de contenedores
    score /= n_bins
    # Se regresan las variables de interés
    return n_bins, solution, bin_weights, score
            
def generateBestNeighbor(s,ni,w,bc):
    # Función para generar los vecinos y obtener el mejor
    # Variables de interes, lista de objetos, número de contenedores, representación, lista de pesos y puntaje de la mejor solución
    bestSolution = []
    bestBins = 0
    bestRepresentation = []
    bestWeights = []
    bestScore = 0
    visitedNeighbors = 0
    evaluations = 0
    # Genera n vecinos semi-aleatorios
    for i in range(ni):
        j = int(random.random()*len(s))
        while (i==j):
            j = int(random.random()*len(s))
        visitedNeighbors +=1
        # Se crea la solución actual de la solución que recibe la función
        # Se utiliza un copiado profundo para que no se modifique la solución actual
        actualSolution = copy.deepcopy(s) 
        # Intercambio de los objetos i y j
        aux = actualSolution[i]
        actualSolution[i] = actualSolution[j]
        actualSolution[j] = aux
        # Se evalua la solución modificada
        n_bins, representation, bin_weights, score = evaluateSolution(actualSolution,w,bc)
        evaluations += 1
        # Si la solución modificada es mejor que la actual, se actualizan las variables de interés 
        if(score > bestScore):
            bestSolution = actualSolution
            bestBins = n_bins
            bestRepresentation = representation
            bestWeights = bin_weights
            bestScore = score
    # Se regresan las variables de interés
    return bestSolution, bestBins, bestRepresentation, bestWeights, bestScore, visitedNeighbors, evaluations
            
def list2string(l):
    # Función que da formato a una lista para la representación de la solución
    return str(l).replace(',',';')

def startHCBP(nameInstance,cota,iterations,save):
    # Función que inicia el Hill-Climbing y recibe una variabe booleana si se quiere guardar los resultados de una ejecución
    # Lectura de la instancia
    n_items, bin_capacity, weights = readInstanceModified(nameInstance,100)
    evaluations = 0
    visitedNeighbors = 0
    # Cota L2
    L2 = cota
    # Generación de una instancia aleatoria
    solution = np.random.permutation(n_items)
    # Evaluación de la solución inicial
    solution_bins, solution_representation, solution_weights, solution_score = evaluateSolution(solution,weights,bin_capacity)
    evaluations += 1
    # csv es una variable que almacena los resultados de la mejor solución cada iteración como un texto
    csv = 'Iteraciones, Numero Contenedores, FBPP, Solución, Representación, Pesos, Vecinos Visitados \n 0, ' + str(solution_bins) + ', ' + str(solution_score) + ', ' + list2string(solution.tolist()) + ', ' + list2string(solution_representation) + ', ' + list2string(solution_weights) + ', 0 \n'  
    # Variable que determina la condición de paro
    stop_condition = True
    # Contador del número de iteraciones
    count = 1
    # best es una variable que regresa en formato texto la mejor solución
    best = '0, ' + str(solution_bins) + ', ' + str(solution_score) + ', ' + list2string(solution.tolist()) + ', ' + list2string(solution_representation) + ', ' + list2string(solution_weights)
    # Mientras no se se cumpla la condición de paro
    while stop_condition:
        # Generar al mejor vecino de la solución
        neighborSolution, neighborBins, neighborRepresentation, neighborWeights, neighborScore, visitedN, nevaluations = generateBestNeighbor(solution,n_items,weights,bin_capacity)
        visitedNeighbors += visitedN
        evaluations += nevaluations
        if (count%100==0):
            print(count,'it',neighborScore)
        # Si el vecino es mejor, sustituye a la solución actual y sigue el ciclo
        if (neighborScore > solution_score):
            solution = neighborSolution
            solution_bins = neighborBins
            solution_representation = neighborRepresentation
            solution_weights = neighborWeights
            solution_score = neighborScore
            best =str(count) + ', ' + str(solution_bins) + ', ' + str(solution_score) + ', ' + list2string(solution.tolist()) + ', ' + list2string(solution_representation) + ', ' + list2string(solution_weights) 
            # Se agrega a csv la solución nueva
            csv += best + ', ' + str(visitedN) + '\n'
        # En caso de que el vecino no sea mejor, se llegue al número máximo de iteraciones, o se llegue a la cota se detiene el ciclo
        else:
            stop_condition= False
        if ((solution_bins==L2) or (count>iterations)):
                stop_condition= False
        # Se aumenta el contador de soluciones
        count += 1
    # Si la variable save es TRUE se guarda un csv con la mejor solución de cada iteración
    if save:
        file = open('Results/SelectedRun/'+nameInstance.split('/')[2].replace('.txt','')+'-Run'+'.csv', 'w')
        file.writelines(csv)
        file.close()
    # Se regresa la mejor solución
    return best+', '+str(visitedNeighbors)+', '+str(evaluations)

# Programa principal

path ='../Instances/'
# Nombre de las instancias
#instances = [f for f in os.listdir(path) if f.endswith(".txt")]
#instances = ['N1c1w1_o.txt', 'N1c1w1_p.txt', 'N1c1w2_c.txt', 'N1c1w2_d.txt', 'N1c1w4_d.txt', 'N1c1w4_i.txt', 'N1c2w1_b.txt', 'N1c2w1_q.txt', 'N1c2w2_l.txt', 'N1c2w2_f.txt', 'N1c2w4_f.txt', 'N1c2w4_l.txt', 'N1c3w1_c.txt', 'N1c3w1_f.txt', 'N1c3w2_d.txt', 'N1c3w2_h.txt', 'N1c3w4_c.txt', 'N1c3w4_b.txt', 'N2c1w1_d.txt', 'N2c1w1_s.txt', 'N2c1w2_h.txt', 'N2c1w2_o.txt', 'N2c1w4_h.txt', 'N2c1w4_q.txt', 'N2c2w1_d.txt', 'N2c2w1_e.txt', 'N2c2w2_b.txt', 'N2c2w2_f.txt', 'N2c2w4_k.txt', 'N2c2w4_r.txt', 'N2c3w1_d.txt', 'N2c3w1_i.txt', 'N2c3w2_q.txt', 'N2c3w2_a.txt', 'N2c3w4_i.txt', 'N2c3w4_m.txt', 'N3c1w1_k.txt', 'N3c1w1_c.txt', 'N3c1w2_d.txt', 'N3c1w2_g.txt', 'N3c1w4_a.txt', 'N3c1w4_j.txt', 'N3c2w1_n.txt', 'N3c2w1_q.txt', 'N3c2w2_s.txt', 'N3c2w2_g.txt', 'N3c2w4_a.txt', 'N3c2w4_d.txt', 'N3c3w1_d.txt', 'N3c3w1_g.txt', 'N3c3w2_b.txt', 'N3c3w2_d.txt', 'N3c3w4_t.txt', 'N3c3w4_j.txt', 'N4c1w1_l.txt', 'N4c1w1_e.txt', 'N4c1w2_k.txt', 'N4c1w2_m.txt', 'N4c1w4_s.txt', 'N4c1w4_b.txt', 'N4c2w1_c.txt', 'N4c2w1_k.txt', 'N4c2w2_a.txt', 'N4c2w2_q.txt', 'N4c2w4_b.txt', 'N4c2w4_d.txt', 'N4c3w1_r.txt', 'N4c3w1_b.txt', 'N4c3w2_s.txt', 'N4c3w2_i.txt', 'N4c3w4_m.txt', 'N4c3w4_c.txt', 'N1w1b1r7.txt', 'N1w1b2r1.txt', 'N1w1b3r3.txt', 'N1w2b1r8.txt', 'N1w2b2r0.txt', 'N1w2b3r5.txt', 'N1w3b1r2.txt', 'N1w3b2r9.txt', 'N1w3b3r4.txt', 'N1w4b1r3.txt', 'N1w4b2r1.txt', 'N1w4b3r1.txt', 'N2w1b1r2.txt', 'N2w1b2r0.txt', 'N2w1b3r2.txt', 'N2w2b1r0.txt', 'N2w2b2r9.txt', 'N2w2b3r2.txt', 'N2w3b1r5.txt', 'N2w3b2r7.txt', 'N2w3b3r0.txt', 'N2w4b1r2.txt', 'N2w4b2r9.txt', 'N2w4b3r6.txt', 'N3w1b1r7.txt', 'N3w1b2r0.txt', 'N3w1b3r5.txt', 'N3w2b1r0.txt', 'N3w2b2r6.txt', 'N3w2b3r7.txt', 'N3w3b1r3.txt', 'N3w3b2r2.txt', 'N3w3b3r1.txt', 'N3w4b1r5.txt', 'N3w4b2r9.txt', 'N3w4b3r6.txt', 'N4w1b1r0.txt', 'N4w1b2r5.txt', 'N4w1b3r1.txt', 'N4w2b1r1.txt', 'N4w2b2r0.txt', 'N4w2b3r0.txt', 'N4w3b1r3.txt', 'N4w3b2r3.txt', 'N4w3b3r9.txt', 'N4w4b1r0.txt', 'N4w4b2r9.txt', 'N4w4b3r0.txt', 'Hard2.txt', 't60_07.txt', 't60_19.txt', 't120_06.txt', 't120_17.txt', 't249_05.txt', 't249_06.txt', 't501_19.txt', 't501_02.txt', 'u120_00.txt', 'u120_05.txt', 'u250_01.txt', 'u250_07.txt', 'u500_13.txt', 'u500_06.txt','hBPP419.txt', 'hBPP814.txt', 'hBPP900.txt', 'BPP16.txt', 'BPP3.txt', 'BPP4.txt', 'BPP58.txt', 'BPP60.txt', 'BPP72.txt', 'BPP8.txt', 'BPP85.txt', 'BPP14.txt', 'BPP15.txt', 'BPP_100.txt', 'BPP_12.txt', 'BPP_14.txt', 'BPP_2.txt', 'BPP_20.txt', 'BPP_33.txt', 'BPP_4.txt', 'BPP_42.txt', 'BPP_48.txt', 'BPP_6.txt', 'TEST0084.txt', 'TEST0058.txt','u1000_00.txt',
instances = ['u1000_13.txt']
# Número de corridas por cada instancia
n_runs = 30
# Seleccionar una corrida aleatoria para guardar
selected_run = random.randint(0,n_runs-1)
# Variable que define si guardar los datos de una corrida
save = False
# Número de iteraciones
niterations = 500

# Ciclo que itera sobre cada instancia del problema
for file in instances:
    print(file)
    # Variable que guarda los resultados de la mejor solución cada corrida
    results = 'Iteración,Número Contenedores,FBPP,Solución,Representación,Pesos,Total Vecinos Visitados,Evaluaciones,Tiempo Ejecución\n'
    # Se construye la ruta de cada archivo de la instancia
    nameInstance = path+file
    metricas = pd.read_csv('../instances/métricas.csv',encoding='unicode-escape')
    L2 = metricas[metricas['Instancias']==nameInstance.split('/')[-1]]['L2'].iloc[0]
    # Ciclo que permite hacer las repeticiones del Hill Climbing
    for i in range(n_runs):
        print(i,'corrida')
        # Se determina si se guarda o no la ejecución de una variable aleatoria
        save_run = True
        if i == selected_run:
            if save == False:
                save_run = False
        else:
            save_run = False
        start_time = time.time()
        r = startHCBP(nameInstance,L2,niterations,save_run)
        execution_time = time.time() - start_time
        results += (r + ', ' + str(execution_time) + '\n')
    # Se guardan los resultados
    file = open('Results/'+nameInstance.split('/')[2].replace('.txt','')+'.csv', 'w')
    file.writelines(results)
    file.close()
    
    
    
