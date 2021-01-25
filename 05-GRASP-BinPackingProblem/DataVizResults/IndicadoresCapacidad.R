library(tidyverse)
library(ggplot2)
library(dplyr)
require(reshape2)

setwd("C:/Users/David/Documents/GitHub/DIA-OptimizacionCombinatoria/04-GRASP-BinPackingProblem/Results/Summary")


df <- read.csv('ModifiedStatistics.csv')
df$Capacidad <- factor(df$Capacidad)

f <- function(x) {
  r <- quantile(x, probs = c(0, 0.25, 0.5, 0.75, 1))
  names(r) <- c("ymin", "lower", "middle", "upper", "ymax")
  r
}

pdf(file = "indicadores.pdf", width = 7, height = 5)

df[,2:9] %>% melt(id.vars='Capacidad') %>% 
  ggplot(aes(x=Capacidad ,y=value, group=Capacidad))+ stat_summary(fun.data = f, geom="boxplot")+
  ggtitle('Desempeño promedio de los indicadores', 'GRASP')+facet_wrap(~variable, scales='free')+
  stat_summary(fun.y=mean, geom="point", shape=20, size=4, colour="#5571D0", fill="red")+
  ylab("")

dev.off()
