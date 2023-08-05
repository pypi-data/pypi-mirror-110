import math
import random


class Vec4:

    def __init__(self, x=0.0, y=0.0, w=0.0, h=0.0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.x

    def setY(self, y):
        self.y = y

    def getW(self):
        return self.w

    def setW(self, w):
        self.w = w

    def getH(self):
        return self.h

    def setH(self, h):
        self.h = h

    def setPos(self, newPos):
        self.x = newPos.x
        self.y = newPos.y
        self.w = newPos.w
        self.h = newPos.h

    def div(self, i):
        return self / i

    def mult(self, i):
        return self * i

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.w ** 2 + self.h ** 2)

    def normalize(self):
        self.setPos(self.div(self.length()))

    @classmethod
    def randomIntVec(cls, minX=-50, maxX=50, minY=-50, maxY=50, minW=-50, maxW=50, minH=-50, maxH=50):
        x = random.randint(minX, maxX)
        y = random.randint(minY, maxY)
        w = random.randint(minW, maxW)
        h = random.randint(minH, maxH)
        return Vec4(x, y, w, h)

    @classmethod
    def randomVec(cls, minX=-50, maxX=50, minY=-50, maxY=50, minW=-50, maxW=50, minH=-50, maxH=50):
        x = random.randrange(minX, maxX)
        y = random.randrange(minY, maxY)
        w = random.randint(minW, maxW)
        h = random.randint(minH, maxH)
        return Vec4(x, y, w, h)

    @classmethod
    def dist(cls, vectorA, vectorB):
        return math.sqrt((vectorA.x - vectorB.x) ** 2 + (vectorA.y - vectorB.y) ** 2 +
                         (vectorA.w - vectorB.w) ** 2 + (vectorA.h - vectorB.h) ** 2)

    @classmethod
    def lerp(cls, vecA, vecB, step):
        x = (1 - step) * vecA.x + step * vecB.x
        y = (1 - step) * vecA.y + step * vecB.y
        w = (1 - step) * vecA.w + step * vecB.w
        h = (1 - step) * vecA.h + step * vecB.h
        return Vec4(x, y, w, h)

    def __add__(self, other):
        return Vec4(self.x + other.x, self.y + other.y, self.w + other.w, self.h + other.h)

    def __sub__(self, other):
        return Vec4(self.x - other.x, self.y - other.y, self.w - other.w, self.h - other.h)

    def __mul__(self, other):
        return Vec4(self.x * other, self.y * other, self.w * other, self.h * other.h)

    def __truediv__(self, other):
        return Vec4(self.x / other, self.y / other, self.w / other, self.h / other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.w == other.w and self.h == other.h

    def __str__(self):
        return f"x = {self.x}, y = {self.y}, w = {self.w}, h = {self.h}"
