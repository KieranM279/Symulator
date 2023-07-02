library('ggplot2')

x_axis <- c()
y_axis <- c()

for (i in seq(0,65535,1)) {
  x_axis <- c(x_axis,i)
  y_axis <- c(y_axis,-4 + 8*(i/65535))
}

df <- data.frame(x=x_axis,y=y_axis)


plot <- ggplot(df,aes(x=x,y=y)) +
  geom_point() +
  theme_bw()

print(plot)