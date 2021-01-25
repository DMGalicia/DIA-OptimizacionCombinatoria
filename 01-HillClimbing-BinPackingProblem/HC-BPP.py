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
    # Función para generar todos los vecino y obtener el mejor
    # Variables de interes, lista de objetos, número de contenedores, representación, lista de pesos y puntaje de la mejor solución
    bestSolution = []
    bestBins = 0
    bestRepresentation = []
    bestWeights = []
    bestScore = 0
    vNeighbors = 0
    nevaluations = 0
    # Doble ciclo para intercambiar dos objetos
    for i in range(ni):
        for j in range(i+1,ni):
            if (i !=j):
                vNeighbors +=1
                nevaluations += 1
                # Se crea la solución actual de la solución que recibe la función
                # Se utiliza un copiado profundo para que no se modifique la solución actual
                actualSolution = copy.deepcopy(s) 
                # Intercambio de los objetos i y j
                aux = actualSolution[i]
                actualSolution[i] = actualSolution[j]
                actualSolution[j] = aux
                # Se evalua la solución modificada
                n_bins, representation, bin_weights, score = evaluateSolution(actualSolution,w,bc)
                # Si la solución modificada es mejor que la actual, se actualizan las variables de interés 
                if(score > bestScore):
                    bestSolution = actualSolution
                    bestBins = n_bins
                    bestRepresentation = representation
                    bestWeights = bin_weights
                    bestScore = score
    # Se regresan las variables de interés
    return bestSolution, bestBins, bestRepresentation, bestWeights, bestScore, vNeighbors, nevaluations
            
def list2string(l):
    # Función que da formato a una lista para la representación de la solución
    return str(l).replace(',',';')

def startHCBP(nameInstance,cota,save):
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
        # En caso de que el vecino no sea mejor o no se encuentre una solución mejor en 3 iteraciones consecutivas se termina el ciclo
        else:
            stop_condition= False
        if ((solution_bins==L2)):
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
instances = [f for f in os.listdir(path) if f.endswith(".txt")]
instances = ['N4w1b1r0.txt', 'N4w1b2r5.txt', 'N4w1b3r1.txt', 'N4w2b1r1.txt', 'N4w2b2r0.txt', 'N4w2b3r0.txt', 'N4w3b1r3.txt', 'N4w3b2r3.txt', 'N4w3b3r9.txt', 'N4w4b1r0.txt', 'N4w4b2r9.txt', 'N4w4b3r0.txt', 'Hard2.txt', 't60_07.txt', 't60_19.txt', 't120_06.txt', 't120_17.txt', 't249_05.txt', 't249_06.txt', 'u120_00.txt', 'u120_05.txt', 'u250_01.txt', 'u250_07.txt','hBPP419.txt', 'hBPP814.txt', 'hBPP900.txt', 'BPP16.txt', 'BPP3.txt', 'BPP4.txt', 'BPP58.txt', 'BPP60.txt', 'BPP72.txt', 'BPP8.txt', 'BPP85.txt', 'BPP14.txt', 'BPP15.txt', 'BPP_100.txt', 'BPP_12.txt', 'BPP_14.txt', 'BPP_2.txt', 'BPP_20.txt', 'BPP_33.txt', 'BPP_4.txt', 'BPP_42.txt', 'BPP_48.txt', 'BPP_6.txt', 'TEST0084.txt', 'TEST0058.txt', 'u500_13.txt', 'u500_06.txt', 't501_19.txt', 't501_02.txt', 'u1000_00.txt', 'u1000_13.txt']
# Número de corridas por cada instancia
n_runs = 30
# Seleccionar una corrida aleatoria para guardar
selected_run = random.randint(0,n_runs-1)
# Variable que define si guardar los datos de una corrida
save_run = False

# Ciclo que itera sobre cada instancia del problema
for file in instances:
    print(file)
    # Variable que guarda los resultados de la mejor solución cada corrida
    results = 'Iteración, Número Contenedores, FBPP, Solución, Representación, Pesos, Total Vecinos Visitados, Evaluaciones, Tiempo Ejecución \n'
    # Se construye la ruta de cada archivo de la instancia
    nameInstance = path+file
    metricas = pd.read_csv('../instances/métricas.csv',encoding='unicode-escape')
    L2 = metricas[metricas['Instancias']==nameInstance.split('/')[-1]]['L2'].iloc[0]
    # Ciclo que permite hacer las repeticiones del Hill Climbing
    for i in range(n_runs):
        print(i,'corrida')
        # Se determina si se guarda o no la ejecución de una variable aleatoria
        if i == selected_run:
            # Se calcula el tiempo y se agrega a los resultados
            start_time = time.time()
            r = startHCBP(nameInstance,L2,save_run)
            execution_time = time.time() - start_time
            results += (r + ', ' + str(execution_time) + '\n')
        else:
            start_time = time.time()
            r = startHCBP(nameInstance,L2,False)
            execution_time = time.time() - start_time
            results += (r + ', ' + str(execution_time) + '\n')
    # Se guardan los resultados
    file = open('Results/'+nameInstance.split('/')[2].replace('.txt','')+'.csv', 'w')
    file.writelines(results)
    file.close()
    
    
    
