library(tidyverse)
library(ggplot2)
library(dplyr)
require(reshape2)

setwd("D:/Información/DIA-OptimizacionCombinatoria/05-VNS-BinPackingProblem/Results/SelectedRun")

files <- c('N1c1w1_a-Run.csv','N1c2w1_a-Run.csv','N1c3w1_a-Run.csv','N1w1b1r0-Run.csv','t60_00-Run.csv')

for(f in files){
  df <- read.csv(f)
  df <- df %>% mutate(Iteración %in% 1:30)
  df$Iteración <- factor(df$Iteración,1:30,1:30)
  name <- strsplit(f, "\\.")[[1]]
  name2 <- paste(name[[1]],".pdf",sep = "")
  pdf(file = paste("D:/Información/DIA-OptimizacionCombinatoria/05-VNS-BinPackingProblem/Results/Summary/",name2), width = 7, height = 5)
  plot(df[,c(1,3,4,8)] %>% melt(id.vars="Iteración") %>% 
         ggplot(aes(x=Iteración ,y=value, group=variable))+ geom_line() +
         ggtitle("Evolución de los indicadores de acuerdo al número de iteración",paste(paste("VNS (",f),")"))+
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
