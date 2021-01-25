import pandas as pd
import os

# Se define el directorio de resultados
directory = 'Results/'
# Se genera la lista con todos los archivos
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f))]
# Ciclo que itera sobre todos los archivos
csv1 = 'Instancia,Iteraciones Promedio,Iteraciones DE,Contenedores Promedio,Contenedores DE,FBPP Promedio,FBPP DE,Vecinos Visitados Promedio,Vecinos Visitados DE,Tiempo Promedio,Tiempo DE \n'
csv2 = 'Instancia,Mejor Puntaje Encontrado,Mejor Número Contenedores,Sólución Óptima,Porcentaje Soluciones Óptimas,Diferencia\n'
optimal = pd.read_csv('../Instances/optimalSolutions.csv')

for f in files:
    print(f)
    df = pd.read_csv(directory+f,header=None,encoding="unicode_escape")
    df = df.iloc[1:]
    df = df.reset_index(drop=True)
    convert_dict = {0: int,    #Iteración VNS
                    1: int,    #Iteraciones
                    2: int,    #Contenedores
                    3: float,  #FBPP
                    4: str,    #Solución
                    5: str,    #Representación
                    6: str,    #Pesos
                    7: int,    #Total Vecinos
                    8: int,    #Evaluaciones
                    9: float}  #Tiempo
    df = df.astype(convert_dict) 
    csv1 += f.replace('.csv','')+', '+'{:.3f}'.format(df[1].mean())+', '+'{:.3f}'.format(df[1].std())+', '+'{:.3f}'.format(df[2].mean())+', '+'{:.3f}'.format(df[2].std())+', '+'{:.3f}'.format(df[3].mean())+', '+'{:.3f}'.format(df[3].std())+', '+'{:.3f}'.format(df[7].mean())+', '+'{:.3f}'.format(df[7].std())+', '+'{:.3f}'.format(df[9].mean())+', '+'{:.3f}'.format(df[9].std())+'\n'
    ind = df[2].idxmax(axis=1)
    ind2 = optimal.index[optimal['Instance']==f.replace('.csv','')][0]
    porcentaje = len(df[df[2]==int(optimal['Optimal'].iloc[ind2])])/len(df)
    csv2 += f.replace('.csv','')+', '+'{:.3f}'.format(df[3].iloc[ind])+', '+'{:.3f}'.format(df[2].iloc[ind])+', '+'{:.3f}'.format(optimal['Optimal'].iloc[ind2])+', '+str(porcentaje)+','+'{:.3f}'.format(df[2].iloc[ind]-optimal['Optimal'].iloc[ind2])+'\n'
file = open('Results/Summary/Statistics.csv', 'w')
file.writelines(csv1)
file.close()
file = open('Results/Summary/BestSolutions.csv', 'w')
file.writelines(csv2)
file.close()
