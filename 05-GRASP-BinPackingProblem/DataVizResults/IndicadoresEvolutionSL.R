library(tidyverse)
library(ggplot2)
library(dplyr)
require(reshape2)

setwd("D:/Informaci�n/DIA-OptimizacionCombinatoria/04-GRASP-BinPackingProblem/Results/SelectedRun")

files <- c('N1c1w1_a-Run.csv','N1c2w1_a-Run.csv','N1c3w1_a-Run.csv','N1w1b1r0-Run.csv','t60_00-Run.csv')

for(f in files){
  df <- read.csv(f)
  df <- df %>% mutate(Iteraci�n %in% 1:30)
  df$Iteraci�n <- factor(df$Iteraci�n,-1:30,-1:30)
  name <- strsplit(f, "\\.")[[1]]
  name2 <- paste(name[[1]],".pdf",sep = "")
  pdf(file = paste("D:/Informaci�n/DIA-OptimizacionCombinatoria/04-GRASP-BinPackingProblem/Results/Summary/SL-",name2), width = 7, height = 5)
  plot(df[,c(1,3,4,8)] %>% melt(id.vars="Iteraci�n") %>% 
         ggplot(aes(x=Iteraci�n ,y=value, group=variable))+ geom_line() +
         ggtitle("Evoluci�n de los indicadores de acuerdo al n�mero de iteraci�n",paste(paste("VNS (",f),")"))+
         facet_wrap(~variable, scales='free')+
         ylab("") + theme(axis.title.x=element_blank(),
                          axis.text.x=element_blank())
  )
  dev.off()
}
