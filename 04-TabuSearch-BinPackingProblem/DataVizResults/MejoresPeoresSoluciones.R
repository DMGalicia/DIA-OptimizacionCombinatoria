library(tidyverse)
library(ggplot2)
library(dplyr)
require(reshape2)

setwd("C:/Users/David/Documents/GitHub/DIA-OptimizacionCombinatoria/02-SimmulatedAnnealing-BinPackingProblem/Results/Summary")


df <- read.csv('ScoreDistribution.csv')

df <- df[order(df$mean),]
cols <- c("Promedio"="#5571D0")

df1 <- df[306:320,]
df1 %>% ggplot(aes(x = reorder(factor(instance),mean))) + 
  ggtitle("Instancias resueltas con el mejor puntaje promedio")+
  geom_boxplot(aes(ymin = min ,ymax = max,middle = q2 ,upper = q3,lower= q1), stat = 'identity')+
  geom_point(aes(y=mean,colour="Promedio"))+
  scale_colour_manual(name="",values=cols)+
  xlab("Instancia del problema")+
  ylab("Puntaje")+
  theme(legend.position = c(0.07, 1), axis.text.x = element_text(angle = 45,vjust=1,hjust=1),plot.title = element_text(hjust = 0.5))

df2 <- df[1:15,]  
df2 %>% ggplot(aes(x = reorder(factor(instance),mean))) + 
  ggtitle("Instancias resueltas con el peor puntaje promedio")+
  geom_boxplot(aes(ymin = min ,ymax = max,middle = q2 ,upper = q3,lower= q1), stat = 'identity')+
  geom_point(aes(y=mean,colour="Promedio"))+
  scale_colour_manual(name="",values=cols)+
  xlab("Instancia del problema")+
  ylab("Puntaje")+
  theme(legend.position = c(0.07, 1), axis.text.x = element_text(angle = 45,vjust=1,hjust=1),plot.title = element_text(hjust = 0.5))
