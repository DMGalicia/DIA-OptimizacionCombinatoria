library(tidyverse)
library(ggplot2)
library(dplyr)

setwd("D:/Informaci�n/DIA-OptimizacionCombinatoria/05-VNS-BinPackingProblem/Results/Summary")
df <- read.csv(file = 'BestSolutions.csv', encoding="UTF-8")

df <- df %>% mutate(dff1 = case_when(Difference1 <0  ~ 'Cota menor al �ptimo',
                                    Difference1 ==0  ~ 'Cota igual al �ptimo',
                               TRUE ~ 'Cota mayor al �ptimo'))

df$Difference3 <- factor(df$Difference3)

pdf(file = "diferencias.pdf", width = 8, height = 5)

df %>% ggplot(aes(x=Difference3,fill = dff1))+
  ggtitle("Diferencia de contenedores entre la mejor soluci�n y el �ptimo", 
          "VNS") + theme(legend.title = element_blank()) +
  geom_bar() + ylab("N�mero de instancias") + xlab("N�mero de contenedores") +
  geom_text(stat='count',aes(label=..count..), 
            vjust=-0.15,position = position_stack(vjust = 1.01))#+
  #facet_wrap(.~Capacidad)
  
dev.off()
