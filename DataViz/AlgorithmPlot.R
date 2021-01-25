library(tidyverse)
library(ggplot2)
library(plyr)
library(dplyr)
require(reshape2)

# Función para extraer percentiles
f <- function(x) {
  r <- quantile(x, probs = c(0, 0.25, 0.5, 0.75, 1))
  names(r) <- c("ymin", "lower", "middle", "upper", "ymax")
  r
}

# Técnicas estudiadas
alg <- c('02-ReducedHillClimbing', '03-SimmulatedAnnealing', '04-TabuSearch', '05-GRASP', '06-VNS')

# Indicadores estudiados
class <- c('Número Objetos','Peso Promedio','Capacidad Contenedores','Rango Normalizado')

# Categorias
ctn <- list(c(0,0.25), c(0.25,0.5), c(0.5,0.75), c(0.75,1))
ct <- c('0.00-0.24','0.25-0.49','0.50-0.74','0.75-1.00')

# Ruta 
path <- 'D:/Información/DIA-OptimizacionCombinatoria'

# Lectura de Métricas
p3 <- paste(path, '/DataViz/Métricas.csv', sep = '')
df3 <- read.csv(p3)
names(df3) <- c('Instancia','Capacidad Contenedores','Número Objetos','Rango Normalizado','Peso Promedio')
df3[c(2:5)] <- lapply(df3[c(2:5)], round, 2)

# Discretización
for (i in c(2,4)){
  for (j in c(1:4)){
    print(class[i])
    print(ctn[j])
    idx <- as.numeric(row.names(df3[df3[class[i]] >= ctn[[j]][[1]] & df3[class[i]] < ctn[[j]][[2]],]))
    df3[idx,class[i]] <- j+2
  }
}

# Formateo de los datos
df3$`Rango Normalizado` <- factor(df3$`Rango Normalizado`)
df3$`Peso Promedio` <- factor(df3$`Peso Promedio`)
df3$`Capacidad Contenedores` <- factor(df3$`Capacidad Contenedores`)
df3$`Número Objetos` <- factor(df3$`Número Objetos`)
df3$`Rango Normalizado` <- mapvalues(df3$`Rango Normalizado`, from = c(3:6), to = ct)
df3$`Peso Promedio` <- mapvalues(df3$`Peso Promedio`, from = c(3:6), to = ct)

# Conjunto de datos a construir
df1 <- data.frame(Instancia = character(),Iteraciones.Promedio = double(),Contenedores.Promedio = double(),
                  FBPP.Promedio =  double(), Vecinos.Visitados.Promedio = double(),Tiempo.Promedio = double(),
                  `Mejor Puntaje Encontrado` = double(),`Mejor Número Contenedores` = integer() ,
                  `Solución Óptima` = integer(),`Porcentaje Soluciones Óptimas` = double(),Diferencia = integer(),
                  `Capacidad Contenedores` = factor(),`Número Objetos` = factor(),
                  `Rango Normalizado` = factor(),`Peso Promedio`=factor(),Algoritmo=character())

# Recoleción de resultados
for (al in alg){
  print(al)
  # Definición del espacio de trabajo
  p <- paste(path, '/', al, '-BinPackingProblem/Results/Summary/', sep = '')
  setwd(p)
  
  # Lectura y unión de datos
  df <- read.csv('Statistics.csv',stringsAsFactors = F)
  df <- df[c(1,2,4,6,8,10)]
  
  # Métricas
  df2 <- read.csv('BestSolutions.csv')
  names(df2) <- c('Instancia','Mejor Puntaje Encontrado','Mejor Número Contenedores','Solución Óptima','Porcentaje Soluciones Óptimas','Diferencia')
  
  # Unión de los datos
  df <- merge(df, df2, by='Instancia', all = T)
  df2 <- df3
  x <- str_split(al,'-')[[1]][2]
  df2$Algoritmo <- x
  df <- merge(df, df2, by='Instancia', all = T)
  names(df1) <- names(df)
  df1 <- union(df1,df)
}

# Formateo de los datos recolectados
df1$Algoritmo <- factor(df1$Algoritmo)
df1$Algoritmo <- mapvalues(df1$Algoritmo, from = c('GRASP','ReducedHillClimbing','SimmulatedAnnealing','TabuSearch','VNS'), to = c('GRASP','Hill Climbing Reducido','Recocido Simulado','Búsqueda Tabú','Busqueda Vecindario Variable'))
df1 <- na.omit(df1)
df1$Diferencia <- factor(df1$Diferencia)

# Gráfica de números de objetos

pdf(paste(path,'/DataViz/','Bins-Items.pdf', sep = ''), width = 8, height = 6)
plot(df1 %>% ggplot(aes(x=`Número Objetos` ,y=Contenedores.Promedio, group = `Número Objetos`)) + 
  stat_summary(fun.data = f, geom="boxplot") + facet_wrap(~Algoritmo) +
  theme(axis.text.x = element_text(angle = 90)) + ylab("Contenedores Promedio") +
  stat_summary(fun=mean, geom="point", shape=20, size=4, colour="#5571D0", fill="red"))
dev.off()

pdf(paste(path,'/DataViz/','Iterations-Items.pdf', sep = ''), width = 8, height = 6)
plot(df1 %>% ggplot(aes(x=`Número Objetos` ,y=Iteraciones.Promedio, group = `Número Objetos`)) + 
  stat_summary(fun.data = f, geom="boxplot") + facet_wrap(~Algoritmo) +
  theme(axis.text.x = element_text(angle = 90)) + ylab("Iteraciones Promedio") +
  stat_summary(fun=mean, geom="point", shape=20, size=4, colour="#5571D0", fill="red"))
dev.off()

pdf(paste(path,'/DataViz/','Neighbors-Items.pdf', sep = ''), width = 8, height = 6)
plot(df1 %>% ggplot(aes(x=`Número Objetos` ,y=Vecinos.Visitados.Promedio, group = `Número Objetos`)) + 
  stat_summary(fun.data = f, geom="boxplot") + facet_wrap(~Algoritmo) +
  theme(axis.text.x = element_text(angle = 90)) + ylab("Vecinos Visitados Promedio") +
  stat_summary(fun=mean, geom="point", shape=20, size=4, colour="#5571D0", fill="red"))
dev.off()

# Gráfica de Rango Normalizado

pdf(paste(path,'/DataViz/','Bins-Range.pdf', sep = ''), width = 8, height = 6)
plot(df1 %>% ggplot(aes(x=`Rango Normalizado` ,y=Contenedores.Promedio, group = `Rango Normalizado`)) + 
  stat_summary(fun.data = f, geom="boxplot") + facet_wrap(~Algoritmo) +
  theme(axis.text.x = element_text(angle = 90)) + ylab("Contenedores Promedio") +
  stat_summary(fun=mean, geom="point", shape=20, size=4, colour="#5571D0", fill="red"))
dev.off()

pdf(paste(path,'/DataViz/','Iterations-Range.pdf', sep = ''), width = 8, height = 6)
plot(df1 %>% ggplot(aes(x=`Rango Normalizado` ,y=Iteraciones.Promedio, group = `Rango Normalizado`)) + 
  stat_summary(fun.data = f, geom="boxplot") + facet_wrap(~Algoritmo) +
  theme(axis.text.x = element_text(angle = 90)) + ylab("Iteraciones Promedio") +
  stat_summary(fun=mean, geom="point", shape=20, size=4, colour="#5571D0", fill="red"))
dev.off()

pdf(paste(path,'/DataViz/','Neighbors-Range.pdf', sep = ''), width = 8, height = 6)
plot(df1 %>% ggplot(aes(x=`Rango Normalizado` ,y=Vecinos.Visitados.Promedio, group = `Rango Normalizado`)) + 
  stat_summary(fun.data = f, geom="boxplot") + facet_wrap(~Algoritmo) +
  theme(axis.text.x = element_text(angle = 90)) + ylab("Vecinos Visitados Promedio") +
  stat_summary(fun=mean, geom="point", shape=20, size=4, colour="#5571D0", fill="red"))
dev.off()

# Graficas de peso promedio

pdf(paste(path,'/DataViz/','Bins-Weight.pdf', sep = ''), width = 8, height = 6)
plot(df1 %>% ggplot(aes(x=`Peso Promedio` ,y=Contenedores.Promedio, group = `Peso Promedio`)) + 
  stat_summary(fun.data = f, geom="boxplot") + facet_wrap(~Algoritmo) +
  theme(axis.text.x = element_text(angle = 90)) + ylab("Contenedores Promedio") +
  stat_summary(fun=mean, geom="point", shape=20, size=4, colour="#5571D0", fill="red"))
dev.off()

pdf(paste(path,'/DataViz/','Iterations-Weight.pdf', sep = ''), width = 8, height = 6)
plot(df1 %>% ggplot(aes(x=`Peso Promedio` ,y=Iteraciones.Promedio, group = `Peso Promedio`)) + 
  stat_summary(fun.data = f, geom="boxplot") + facet_wrap(~Algoritmo) +
  theme(axis.text.x = element_text(angle = 90)) + ylab("Iteraciones Promedio") +
  stat_summary(fun=mean, geom="point", shape=20, size=4, colour="#5571D0", fill="red"))
dev.off()

pdf(paste(path,'/DataViz/','Neighbors-Weight.pdf', sep = ''), width = 8, height = 6)
plot(df1 %>% ggplot(aes(x=`Peso Promedio` ,y=Vecinos.Visitados.Promedio, group = `Peso Promedio`)) + 
  stat_summary(fun.data = f, geom="boxplot") + facet_wrap(~Algoritmo) +
  theme(axis.text.x = element_text(angle = 90)) + ylab("Vecinos Visitados Promedio") +
  stat_summary(fun=mean, geom="point", shape=20, size=4, colour="#5571D0", fill="red"))
dev.off()

# Graficas de capacidad

pdf(paste(path,'/DataViz/','Bins-Capacity.pdf', sep = ''), width = 8, height = 6)
plot(df1 %>% ggplot(aes(x=`Capacidad Contenedores` ,y=Contenedores.Promedio, group = `Capacidad Contenedores`)) + 
  stat_summary(fun.data = f, geom="boxplot") + facet_wrap(~Algoritmo) +
  theme(axis.text.x = element_text(angle = 90)) + ylab("Contenedores Promedio") +
  stat_summary(fun=mean, geom="point", shape=20, size=4, colour="#5571D0", fill="red"))
dev.off()

pdf(paste(path,'/DataViz/','Iterations-Capacity.pdf', sep = ''), width = 8, height = 6)
plot(df1 %>% ggplot(aes(x=`Capacidad Contenedores` ,y=Iteraciones.Promedio, group = `Capacidad Contenedores`)) + 
  stat_summary(fun.data = f, geom="boxplot") + facet_wrap(~Algoritmo) +
  theme(axis.text.x = element_text(angle = 90)) + ylab("Iteraciones Promedio") +
  stat_summary(fun=mean, geom="point", shape=20, size=4, colour="#5571D0", fill="red"))
dev.off()

pdf(paste(path,'/DataViz/','Neighbors-Capacity.pdf', sep = ''), width = 8, height = 6)
plot(df1 %>% ggplot(aes(x=`Capacidad Contenedores` ,y=Vecinos.Visitados.Promedio, group = `Capacidad Contenedores`)) + 
  stat_summary(fun.data = f, geom="boxplot") + facet_wrap(~Algoritmo) +
  theme(axis.text.x = element_text(angle = 90)) + ylab("Vecinos Visitados Promedio") +
  stat_summary(fun=mean, geom="point", shape=20, size=4, colour="#5571D0", fill="red"))
dev.off()

# Gráfica de Sóluciones óptimas y no tan óptimas por algoritmos

pdf(paste(path,'/DataViz/','OptimalSolutions.pdf', sep = ''), width = 8, height = 6)
plot(df1 %>% ggplot(aes(x=Diferencia)) + facet_wrap(~Algoritmo) +
  geom_bar() + geom_text(aes(label=..count..), stat = 'count', nudge_y = 6)+
  theme(axis.text.x = element_text(angle = 90)) + ylab("Número de instancias") +
  xlab('Diferencia de contenedores entre la solución óptima y la mejor solución encontrada'))
dev.off()

