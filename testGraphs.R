library('ggplot2')

x_axis <- c()
y_axis <- c()

for (i in seq(-3,3,0.001)) {
  x_axis <- c(x_axis,i)
  y_axis <- c(y_axis,tanh(i))
}

df <- data.frame(x=x_axis,y=y_axis)


plot <- ggplot(df,aes(x=x,y=y)) +
  geom_point() +
  theme_bw()

print(plot)