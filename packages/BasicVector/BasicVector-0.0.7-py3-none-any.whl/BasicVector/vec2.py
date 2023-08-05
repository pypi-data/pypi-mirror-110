import math
import random


class Vec2:

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.x

    def setY(self, y):
        self.y = y

    def setPos(self, newPos):
        self.x = newPos.x
        self.y = newPos.y

    def div(self, i):
        return self / i

    def mult(self, i):
        return self * i

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        self.setPos(self.div(self.length()))

    @classmethod
    def randomIntVec(cls, minX=-50, maxX=50, minY=-50, maxY=50):
        x = random.randint(minX, maxX)
        y = random.randint(minY, maxY)
        return Vec2(x, y)

    @classmethod
    def randomVec(cls, minX=-50, maxX=50, minY=-50, maxY=50):
        x = random.randrange(minX, maxX)
        y = random.randrange(minY, maxY)
        return Vec2(x, y)

    @classmethod
    def dist(cls, vecA, vecB):
        return math.sqrt((vecA.x - vecB.x) ** 2 + (vecA.y - vecB.y) ** 2)

    @classmethod
    def degreesToVec2(cls, degrees):
        radians = degrees * (math.pi / 180)
        return Vec2(math.cos(radians), math.sin(radians))

    @classmethod
    def radiansToVec2(cls, radians):
        return Vec2(math.cos(radians), math.sin(radians))

    @classmethod
    def lerp(cls, vecA, vecB, step):
        x = (1 - step) * vecA.x + step * vecB.x
        y = (1 - step) * vecA.y + step * vecB.y
        return Vec2(x, y)

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vec2(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vec2(self.x / other, self.y / other)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"x = {self.x}, y = {self.y}"
