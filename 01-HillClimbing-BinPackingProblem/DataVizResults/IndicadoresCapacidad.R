library(tidyverse)
library(ggplot2)
library(dplyr)
require(reshape2)

setwd("C:/Users/David/Documents/GitHub/DIA-OptimizacionCombinatoria/01-HillClimbing-BinPackingProblem/Agueda/Summary")


df <- read.csv('ModifiedStatistics.csv')
df$Capacidad <- factor(df$Capacidad)

f <- function(x) {
  r <- quantile(x, probs = c(0, 0.25, 0.5, 0.75, 1))
  names(r) <- c("ymin", "lower", "middle", "upper", "ymax")
  r
}

df[,2:7] %>% melt(id.vars='Capacidad') %>% 
  ggplot(aes(x=Capacidad ,y=value, group=Capacidad))+ stat_summary(fun.data = f, geom="boxplot")+
  facet_wrap(~variable, scales='free')+
  stat_summary(fun.y=mean, geom="point", shape=20, size=4, colour="#5571D0", fill="red")+
  ylab("")
