import math

class Shape:
    def get_area(self):
        raise NotImplementedError
    def get_perimeter(self):
        raise NotImplementedError

    @property
    def area(self):
        return self.get_area()

    @property
    def perimeter(self):
        return self.get_perimeter()


class Circle(Shape):
    def __init__(self, radius):
        if radius <= 0:
            raise ValueError("Радиус должен быть положительным")
        self.radius = radius
    def get_area(self):
        return math.pi * self.radius ** 2
    def get_perimeter(self):
        return 2 * math.pi * self.radius

class Triangle(Shape):
    def __init__(self, a, b, c):
        if a <= 0:
            raise ValueError("Сторона должна быть положительной")
        self.a = a
        if b <= 0:
            raise ValueError("Сторона должна быть положительной")
        self.b = b
        if c <= 0:
            raise ValueError("Сторона должна быть положительной")
        self.c = c
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Треугольник с такими сторонами не существует")
    def get_area(self):
        p = (self.a + self.b + self.c)/2
        return math.sqrt(p * (p-self.a) * (p - self.b) * (p - self.c))
    def get_perimeter(self):
        return self.a + self.b + self.c

class Rectangle(Shape):
    def __init__(self, a, b):
        if a <= 0:
            raise ValueError("Сторона должна быть положительной")
        self.a = a
        if b <= 0:
            raise ValueError("Сторона должна быть положительной")
        self.b = b
    def get_area(self):
        return self.a*self.b
    def get_perimeter(self):
        return (self.a + self.b) * 2
    def get_diagonal(self):
        return math.sqrt(self.a ** 2 + self.b ** 2)

class Square(Rectangle):
    def __init__(self, m):
        super().__init__(m, m)

kk = [Circle(4), Rectangle(2, 4), Square(3), Triangle(12, 5, 8)]
for k in kk:
    print(f"{k.__class__.__name__}: area:{k.area:.2f}, perimeter:{k.perimeter:.2f}")


