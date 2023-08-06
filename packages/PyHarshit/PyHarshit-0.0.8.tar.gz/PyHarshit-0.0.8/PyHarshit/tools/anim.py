import turtle

t = turtle.Turtle()

def tricolor(colors):
    for i in range(300):
        t.color(colors[i%3])
        t.forward(i*1)
        t.left(59)
        t.width(3)
