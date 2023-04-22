setwd('~/Documents/Simulator/')

library('ggplot2')

# Import the field
grid <- read.csv('field.csv')
rownames(grid) <- grid$X
grid <- as.data.frame(subset(grid,select=-c(X)))



grid <- as.matrix(grid)

test <- cbind(expand.grid(dimnames(grid)), value = as.vector(grid))
df <- as.data.frame(test)

df$value <- factor(df$value,
                   levels = c(".","c"))



plot <- ggplot(df, aes(x = Var2, y = Var1,fill=value)) +
  scale_fill_manual(values=c("#999999", "#E69F00")) +
  geom_tile()


print(plot)