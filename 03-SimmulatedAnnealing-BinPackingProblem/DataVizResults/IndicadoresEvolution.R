library(tidyverse)
library(ggplot2)
library(dplyr)
require(reshape2)

setwd("C:/Users/David/Documents/GitHub/DIA-OptimizacionCombinatoria/02-SimmulatedAnnealing-BinPackingProblem/Results")

files <- c('N1c1w1_a.csv','N1c2w1_a.csv','N1c3w1_a.csv','N1w1b1r0.csv','t60_00.csv')

for(f in files){
  df <- read.csv(f)
  df <- df %>% mutate(Ejecuci�n = 1:30)
  df$Ejecuci�n <- factor(df$Ejecuci�n,1:30,1:30)
  name <- strsplit(f, "\\.")[[1]]
  name2 <- paste(name[[1]],".pdf",sep = "")
  pdf(file = paste("C:/Users/David/Documents/GitHub/DIA-OptimizacionCombinatoria/02-SimmulatedAnnealing-BinPackingProblem/Results/Summary/",name2), width = 8, height = 5)
  plot(df[,c(4,10,5,1,11,6,13,12,14)] %>% melt(id.vars="Ejecuci�n") %>% 
    ggplot(aes(x=Ejecuci�n ,y=value, group=variable))+ geom_line() +
    ggtitle("Evoluci�n de los indicadores de acuerdo al n�mero de ejecuci�n",paste(paste("Recocido Simulado (",f),")"))+
    facet_wrap(~variable, scales='free')+
    ylab("") + theme(axis.title.x=element_blank())+
    scale_x_discrete(labels=c("1"="","2"="","3"="","4"="",
                              "6"="","7"="","8"="","9"="",
                              "11"="","12"="","13"="","14"="",
                              "16"="","17"="","18"="","19"="",
                              "21"="","22"="","23"="","24"="",
                              "26"="","27"="","28"="","29"=""))
  )
  dev.off()
}
