#setwd('~/Documents/Symulator/Outputs')
setwd('C:/Users/Atlas/Desktop/Symulator/Outputs')

library('ggplot2')

# Add in the simulation parameters



convert_coordinates <- function(list_of_coords){
  
  for (i in 1:length(list_of_coords)) {
    list_of_coords[i] <- substring(list_of_coords[i],3,nchar(list_of_coords[i]))
  }
  return(list_of_coords)
}

basic_plotter <- function(filename) {
  
  # Import the field
  grid <- read.csv(filename)
  rownames(grid) <- grid$X
  grid <- as.data.frame(subset(grid,select=-c(X)))
  
  grid <- as.matrix(grid)
  
  test <- cbind(expand.grid(dimnames(grid)), value = as.vector(grid))
  df <- as.data.frame(test)

  
  df <- df[df$value == 'c',]
  
  df$Var1 <- as.character((df$Var1))
  df$Var2 <- as.character((df$Var2))
  
  df$Var1 <- convert_coordinates(df$Var1)
  df$Var2 <- convert_coordinates(df$Var2)
  
  df$Var1 <- as.numeric((df$Var1))
  df$Var2 <- as.numeric((df$Var2))
  
  
  
  plot <- ggplot(df,aes(x=Var2,y=Var1)) +
    geom_point() +
    theme_bw() +
    xlim(0,128) +
    ylim(0,128) +
    theme(axis.title = element_blank(),
          axis.text = element_blank(),
          axis.ticks = element_blank(),
          legend.position = "none")
  return(plot)
  
  
}

print(basic_plotter('0_field.csv'))
print(basic_plotter('1_field.csv'))
print(basic_plotter('2_field.csv'))