# Script for prototyping the pheromone spread

library('ggplot2')



# Make a grid

grid_size = 128

x_list = c()
y_list = c()
value_list = c()


for (y in 1:100) {
  for (x in 1:100) {
    x_list <- c(x_list,x)
    y_list <- c(y_list,y)
    
    if (x == 50 & y == 50) {
      value_list <- c(value_list,-1)
    } else{
      value_list <- c(value_list,0)
    }
  }
}

grid = data.frame(x = x_list,
                  y = y_list,
                  value = value_list)


distance_calculator <- function(x1,y1,x2,y2) {
  
  # Calculate the x axis delta
  if (x1 >= x2) {
    x_delta = x1-x2
  } else if (x1<x2) {
    x_delta = x2-x1
  }
  
  # Calculate the y axis delta
  if (y1 >= y2) {
    y_delta = y1-y2
  } else if (y1<y2) {
    y_delta = y2-y1
  }
  
  dist = sqrt((x_delta**2) + (y_delta**2))
  
  return(dist)
}
rm_old_circle <- function(df) {
  
  for (i in 1:nrow(df)) {
    if (df$value[i] > 0) {
      df$value[i] = 0
    }
  }
  
  
  return(df)
}
add_circle <- function(r,df,c) {
  for (i in 1:nrow(df)) {
    
    if ((df$x[i] > c[1]+r) | (df$x[i] < c[1]-r)) {
      next
    } else if ((df$y[i] > c[2]+r) | (df$y[i] < c[2]-r)) {
      next
    } else {
    
      dist = distance_calculator(c[1],c[2],df$x[i],df$y[i])
    
      if (round(dist,0) == r) {
        
        conc <- ((5-(r-1))*0.2)
        
        df$value[i] = conc
      }
    }
    
  }
  return(df)
}

plot <- ggplot(grid, aes(x=x,y=y,fill = value)) +
  #scale_fill_gradient(limits = c(-1,1),colours=c("navyblue", "darkmagenta", "darkorange1")) +
  geom_tile() +
  theme_bw()
print(plot)

start = Sys.time()

for (t in 1:5) {
  
  grid <- rm_old_circle(grid)
  grid <- add_circle(t,grid,c(50,50))
  
  plot <- ggplot(grid, aes(x=x,y=y,fill = value)) +
    #scale_fill_gradient(limits = c(-1,1),colours=c("navyblue", "darkmagenta", "darkorange1")) +
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
    theme_bw()
  
  print(plot)
}

end = Sys.time()

print("Time elapsed: ")
print(paste(as.character(end-start), "seconds", sep = " "))
