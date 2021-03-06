library(tidyverse)
library(ggplot2)
library(dplyr)

setwd("C:/Users/David/Documents/GitHub/DIA-OptimizacionCombinatoria/01-HillClimbing-BinPackingProblem/Agueda/Summary")
df <- read.csv(file = 'BestSolutions.csv', encoding="UTF-8")

df %>% ggplot(aes(x=difference))+
  ggtitle("Diferencia en el n�mero de contenedores entre\nla mejor soluci�n encotrada y la soluci�n �ptima")+
  geom_bar(aes(fill = ..count..))+
  geom_text(stat='count',aes(label=..count..), vjust=-0.15)+
  theme(legend.position = "none")+
  ylab("N�mero de instancias")+
  scale_x_continuous("Diferencia de contendores",
                     limits=c(-0.5,2.5),breaks = seq(0, 2, by = 1),1)
