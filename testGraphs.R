library('ggplot2')

x_axis <- c()
y_axis <- c()

for (i in seq(0,300,1)) {
  x_axis <- c(x_axis,i)
  y_axis <- c(y_axis,sin(i/5))
}

df <- data.frame(x=x_axis,y=y_axis)


plot <- ggplot(df,aes(x=x,y=y)) +
  geom_point() +
  theme_bw()

print(plot)