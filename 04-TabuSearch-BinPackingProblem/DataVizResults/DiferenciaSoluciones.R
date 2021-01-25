library(tidyverse)
library(ggplot2)
library(dplyr)

setwd("C:/Users/David/Documents/GitHub/DIA-OptimizacionCombinatoria/03-TabuSearch-BinPackingProblem/Results/Summary")
df <- read.csv(file = 'BestSolutions.csv', encoding="UTF-8")

df <- df %>% mutate(dff1 = case_when(Difference1 <0  ~ 'Cota menor al óptimo',
                                    Difference1 ==0  ~ 'Cota igual al óptimo',
                               TRUE ~ 'Cota mayor al óptimo'))

df$Difference3 <- factor(df$Difference3)

pdf(file = "diferencias.pdf", width = 8, height = 5)

df %>% ggplot(aes(x=Difference3,fill = dff1))+
  ggtitle("Diferencia de contenedores entre la mejor solución y el óptimo", 
          "Búsqueda Tabú") + theme(legend.title = element_blank()) +
  geom_bar() + ylab("Número de instancias") + xlab("Número de contenedores") +
  geom_text(stat='count',aes(label=..count..), 
            vjust=-0.15,position = position_stack(vjust = 1.01))
  
dev.off()
