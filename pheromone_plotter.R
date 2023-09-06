#setwd('~/Documents/Symulator/Outputs')
setwd('C:/Users/Atlas/Desktop/Symulator/Outputs')

library('ggplot2')
library('hash')


#### Import the simulation parameters ####

readParameters <- function(filename) {
  dictionary <- hash()
  # Read in text file
  data = read.delim(filename,
                    sep="",
                    header = FALSE)
  colnames(data) <- c("parameter","value")
  
  # Process data into dictionary
  for (p in 1:nrow(data)){
    
    # Convert the list of saved generations
    if (data$parameter[p] == 'SAVED_GENERATIONS'){
      new_list <- data$value[p]
      new_list <- substring(new_list,2,nchar(new_list)-1)
      new_list <- strsplit(new_list,",")
      dictionary[data$parameter[p]] <- new_list
    } else {
      dictionary[data$parameter[p]] <- as.numeric(data$value[p])
    }
  }
  return(dictionary)
}

parameters = readParameters('../parameters.txt')

#### Useful functions for plotting ####

# Convert the odd coodinate layout I chose when I started this
convert_coordinates <- function(list_of_coords){
  # Loop through list of coordinates
  for (i in 1:length(list_of_coords)) {
    # Remove the axis letter
    list_of_coords[i] <- substring(list_of_coords[i],3,nchar(list_of_coords[i]))
  }
  return(list_of_coords)
}

# Generate the legend title for the plot
title_gen <- function(para,tick,gen) {
  population <- para[['POPULATION']]
  spacer = ""
  
  # Enter parameters here
  generation = gen
  gene_no = para[['GENES']]
  int_no = para[['INTERNAL_NEURONS']]
  mutation_no = para[['MUTATION_RATE']]
  grid_size = paste(para[['GRID_SIZE']],para[['GRID_SIZE']],sep="x")
  
  # Processing the parameters to readable text
  title <- "Simulation parameters:"
  population <- paste("No. organisms = ", population,sep="")
  generation <- paste("Generation = ",generation,sep="")
  tick <- paste("Tick = ",tick,sep="")
  gene_no <- paste("No. genes = ",gene_no,sep="")
  int_no <- paste("No. internal neurones = ",int_no,sep="")
  mutation_no <- paste("Mutation rate = ", mutation_no,sep="")
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
                      mutation_no,
                      spacer,
                      grid_size,
                      spacer,
                      sep = '\n')
  return(final_text)
}





# The plotting function
basic_plotter <- function(filename,tick,gen) {
  
  # Import the field
  grid <- read.csv(filename)
  rownames(grid) <- grid$X
  grid <- as.data.frame(subset(grid,select=-c(X)))
  
  grid <- as.matrix(grid)
  
  test <- cbind(expand.grid(dimnames(grid)), value = as.vector(grid))
  df <- as.data.frame(test)
  
  
  
  #df <- df[df$value == 'c',]
  df[df == "."] <- 0
  
  df$Var1 <- as.character((df$Var1))
  df$Var2 <- as.character((df$Var2))
  
  df$Var1 <- convert_coordinates(df$Var1)
  df$Var2 <- convert_coordinates(df$Var2)

  df$Var1 <- as.numeric((df$Var1))
  df$Var2 <- as.numeric((df$Var2))
  df$value <- as.numeric((df$value))
  
  plot <- ggplot(df, aes(x=Var2,y=Var1,fill=value)) +
    scale_fill_gradient2(
      low = ("darkmagenta"),
      mid = "navyblue",
      high = ("darkorange1"),
      limits = c(-1,1),
      midpoint = 0,
      space = "Lab",
      na.value = "grey50",
      guide = "colourbar",
      aesthetics = "fill"
    ) +
    geom_tile() +
    theme(axis.title = element_blank(),
          axis.text = element_blank(),
          axis.ticks = element_blank(),
          legend.text = element_text(size=15),
          legend.background = element_rect(fill="lightblue",
                                           linewidth=0.5, linetype="solid", 
                                           colour ="darkblue")) +
    guides(fill=guide_legend(title_gen(parameters,tick,gen))) +
    theme_bw()
  
  return(plot)
  
  
}


for (g in parameters[['SAVED_GENERATIONS']][[1]]) {
  
  gen_name <- paste("Generation",g,sep = "")
  print(paste("Plotting generation ",g,sep = ""))
  
  for (t in 0:(parameters[['TICKS']]-1)) {
    
    # Generate file names
    file_input <- paste(gen_name,'/',t,'_pheromone.csv',sep = '')
    file_output <- paste('../frames/',gen_name,'/',t,'_frame_pheromone.png',sep = "")
    # Plot field
    ggsave(basic_plotter(file_input,t,g),
           filename = file_output,
           width = 10,
           height = 7,
           device = 'png')
  }
}