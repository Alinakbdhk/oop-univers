import tkinter as tk
from random import randint

window = tk.Tk()
window.geometry("800x800")
window.title('Фигуры')

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self):
        canvas.create_oval(self.x, self.y, self.x + 5, self.y + 5, fill="red", outline="red")

class Line():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    def draw(self):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill="green")

class Rectangle():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    def draw(self):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="blue")

class Oval():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    def draw(self):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="pink")

def on_click(event):
    x, y = event.x, event.y
    point = Point(x, y)
    point.draw()
def line_drow():
    x1 = randint(0, 500)
    y1 = randint(0, 500)
    x2 = randint(0, 500)
    y2 = randint(0, 500)
    line = Line(x1, y1, x2, y2)
    line.draw()
def rectangle_draw():
    x1 = randint(0, 500)
    y1 = randint(0, 500)
    x2 = randint(0, 500)
    y2 = randint(0, 500)
    rectangle = Rectangle(x1, y1, x2, y2)
    rectangle.draw()
def oval_draw():
    x1 = randint(0, 500)
    y1 = randint(0, 500)
    x2 = randint(0, 500)
    y2 = randint(0, 500)
    oval = Oval(x1, y1, x2, y2)
    oval.draw()
def triangle_draw():
    x1 = randint(0, 500)
    y1 = randint(0, 500)
    x2 = randint(0, 500)
    y2 = randint(0, 500)
    x3 = randint(0, 500)
    y3 = randint(0, 500)
    line = Line(x1, y1, x2, y2)
    line.draw()
    line2 = Line(x2, y2, x3, y3)
    line2.draw()
    line3 = Line(x3, y3, x1, y1)
    line3.draw()

button = tk.Button(window, text="Создать овал", command=oval_draw)
button.pack(padx=20, pady=20, side=tk.TOP)

button = tk.Button(window, text="Создать прямоугольник", command=rectangle_draw)
button.pack(padx=20, pady=20, side=tk.TOP)

button = tk.Button(window, text="Создать линию", command=line_drow)
button.pack(padx=20, pady=20, side=tk.TOP)

button = tk.Button(window, text="Создать треугольник", command=triangle_draw)
button.pack(padx=20, pady=20, side=tk.TOP)


canvas = tk.Canvas(window, width=500, height=500, bg="white")
canvas.pack()
canvas.bind("<Button-1>", on_click)
window.mainloop()




