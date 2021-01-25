library(ggplot2)
library(ggcorrplot)

path <- 'D:/Información/DIA-OptimizacionCombinatoria'
# Métricas
p2 <- paste(path, '/DataViz/Métricas.csv', sep = '')
df2 <- read.csv(p2)
names(df2) <- c('Instancia','Cpcd','Objt','Rng','PsPr')

alg <- c('02-ReducedHillClimbing', '03-SimmulatedAnnealing', '04-TabuSearch', '05-GRASP', '06-VNS')

for (al in alg){
  print(al)
  # Definición del espacio de trabajo
  p <- paste(path, '/', al, '-BinPackingProblem/Results/Summary/', sep = '')
  setwd(p)
  
  # Lectura y unión de datos
  if (al != '06-VNS'){
    df1 <- read.csv('Statistics.csv')
    df1 <- df1[c(1,2,4,6,8,10)]
    names(df1) <- c('Instancia','Itrs','Cnts','FBPP','VcVs','Tmp')
  }
  else{
    df1 <- read.csv('Statistics.csv')
    df1 <- df1[c(1,2,4,6,8,10)]
    names(df1) <- c('Instancia','Itrs','Cnts','FBPP','VcVs','Tmp')
  }
  df3 <- merge(df1, df2, by='Instancia', all = T)
  df3 <- df3[c(2:10)]
  
  
  # Cálculo de correlación
  corr <- round(cor(df3, use = "complete.obs"), 1)
  
  # Gráfica
  pdf(paste(path, '/', al, '-BinPackingProblem/', al, '-correlation.pdf', sep = ''), width = 9, height = 9)
  plot(ggcorrplot(corr, hc.order = T, type = 'upper', lab = T, lab_size = 6, tl.cex = 20, outline.col = "white", show.legend = F))
  dev.off()
}
