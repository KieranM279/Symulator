setwd('~/Documents/Symulator/Outputs')

library('ggplot2')

basic_plotter <- function(filename) {
  
  # Import the field
  grid <- read.csv(filename)
  rownames(grid) <- grid$X
  grid <- as.data.frame(subset(grid,select=-c(X)))
  
  grid <- as.matrix(grid)
  
  test <- cbind(expand.grid(dimnames(grid)), value = as.vector(grid))
  df <- as.data.frame(test)
  
  df$value <- factor(df$value,
                     levels = c(".","c"))
  
  plot <- ggplot(df, aes(x = Var2, y = Var1,fill=value)) +
    scale_fill_manual(values=c("grey80", "dodgerblue2")) +
    geom_tile()
  
  
  return(plot)
  
  
}

print(basic_plotter('0_field.csv'))
print(basic_plotter('1_field.csv'))
print(basic_plotter('2_field.csv'))