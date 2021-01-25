import pandas as pd
import os

# Se define el directorio de resultados
directory = 'Results3/'
# Se genera la lista con todos los archivos
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f))]
# Ciclo que itera sobre todos los archivos
csv1 = 'instance, mean iterations, sd iterations, mean bins, sd bins, mean score, sd score, mean neighbors, sd neighbors, mean time, sd time \n'
csv2 = 'instance, mean, min, max, q1, q2, q3 \n'
csv3 = 'instance, best score, best bins, optimal solution, difference \n'
optimal = pd.read_csv('../Instances/optimalSolutions.csv')
for f in files:
    print(f)
    df = pd.read_csv(directory+f,header=None,encoding="unicode_escape")
    df = df.iloc[1:]
    df = df.reset_index(drop=True)
    convert_dict = {0: int,
                    1: int,
                    2: float,
                    3: str,
                    4: str,
                    5: str,
                    6: int,
                    7: float}
    df = df.astype(convert_dict) 
    csv1 += f.replace('.csv','')+', '+'{:.3f}'.format(df[0].mean())+', '+'{:.3f}'.format(df[0].std())+', '+'{:.3f}'.format(df[1].mean())+', '+'{:.3f}'.format(df[1].std())+', '+'{:.3f}'.format(df[2].mean())+', '+'{:.3f}'.format(df[2].std())+', '+'{:.3f}'.format(df[6].mean())+', '+'{:.3f}'.format(df[6].std())+', '+'{:.3f}'.format(df[7].mean())+', '+'{:.3f}'.format(df[7].std())+'\n'
    csv2 += f.replace('.csv','')+', '+'{:.3f}'.format(df[2].mean())+', '+'{:.3f}'.format(df[2].min())+', '+'{:.3f}'.format(df[2].max())+', '+'{:.3f}'.format(df[2].quantile(0.25))+', '+'{:.3f}'.format(df[2].quantile(0.5))+', '+'{:.3f}'.format(df[2].quantile(0.75))+'\n'
    ind = df[2].idxmax(axis=1)
    ind2 = optimal.index[optimal['Instance']==f.replace('.csv','')][0]
    csv3 += f.replace('.csv','')+', '+'{:.3f}'.format(df[2].iloc[ind])+', '+'{:.3f}'.format(df[1].iloc[ind])+', '+'{:.3f}'.format(optimal['Optimal'].iloc[ind2])+', '+'{:.3f}'.format(df[1].iloc[ind]-optimal['Optimal'].iloc[ind2])+'\n'
file = open('Results3/Summary/Statistics.csv', 'w')
file.writelines(csv1)
file.close()
file = open('Results3/Summary/ScoreDistribution.csv', 'w')
file.writelines(csv2)
file.close()
file = open('Results3/Summary/BestSolutions.csv', 'w')
file.writelines(csv3)
file.close()
