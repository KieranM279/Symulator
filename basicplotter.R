#setwd('~/Documents/Symulator/Outputs')
setwd('C:/Users/Atlas/Desktop/Symulator/Outputs')

library('ggplot2')

# Add in the simulation parameters



convert_coordinates <- function(list_of_coords){
  # Loop through list of coordinates
  for (i in 1:length(list_of_coords)) {
    # Remove the 
    list_of_coords[i] <- substring(list_of_coords[i],3,nchar(list_of_coords[i]))
  }
  return(list_of_coords)
}


title_gen <- function(df,tick) {
  population <- nrow(df)
  spacer = ""
  
  # Enter parameters here
  generation = 1
  gene_no = 16
  int_no = 3
  grid_size = "128x128"
  
  # Processing the parameters
  title <- "Simulation parameters:"
  population <- paste("No. organisms = ", population,sep="")
  generation <- paste("Generation = ",generation,sep="")
  tick <- paste("Tick = ",tick,sep="")
  gene_no <- paste("No. genes = ",gene_no,sep="")
  int_no <- paste("No. internal neurones = ",int_no,sep="")
  grid_size <- paste("Grid size = ",grid_size,sep="")
  
  # Generate final title
  final_text <- paste(title,
                      spacer,
                      population,
                      generation,
                      tick,
                      spacer,
                      gene_no,
                      int_no,
                      spacer,
                      grid_size,
                      spacer,
                      sep = '\n')
  return(final_text)
}



basic_plotter <- function(filename,tick) {
  
  # Import the field
  grid <- read.csv(filename)
  rownames(grid) <- grid$X
  grid <- as.data.frame(subset(grid,select=-c(X)))
  
  grid <- as.matrix(grid)
  
  test <- cbind(expand.grid(dimnames(grid)), value = as.vector(grid))
  df <- as.data.frame(test)

  
  df <- df[df$value == 'c',]
  df[df == "c"] <- "Creatures"
  
  df$Var1 <- as.character((df$Var1))
  df$Var2 <- as.character((df$Var2))
  
  df$Var1 <- convert_coordinates(df$Var1)
  df$Var2 <- convert_coordinates(df$Var2)
  
  df$Var1 <- as.numeric((df$Var1))
  df$Var2 <- as.numeric((df$Var2))
  
  
  plot <- ggplot(df,aes(x=Var2,y=Var1,fill=value)) +
    geom_point() +
    theme_bw(base_size = 15) +
    xlim(0,127) +
    ylim(0,127) +
    theme(axis.title = element_blank(),
          axis.text = element_blank(),
          axis.ticks = element_blank(),
          legend.text = element_text(size=15),
          legend.background = element_rect(fill="lightblue",
                                     size=0.5, linetype="solid", 
                                     colour ="darkblue")) +
    guides(fill=guide_legend(title_gen(df,tick)))
  return(plot)
  
  
}


#print(basic_plotter('0_field.csv',0))

for (i in seq(0,299,1)) {
  print(i)
  
  
  ggsave(basic_plotter(paste(i,'field.csv',sep="_"),i),
         filename = paste('../frames/',i,'_field.png',sep=""),
         width = 10,
         height = 7,
         device = 'png')
  
  
}



#print(basic_plotter('0_field.csv'))
#print(basic_plotter('1_field.csv'))
#print(basic_plotter('2_field.csv'))


#ggsave(basic_plotter('0_field.csv'),
#       filename = '0_field.png',
#       width = 10,
#       height = 10,
#       device = 'png')
