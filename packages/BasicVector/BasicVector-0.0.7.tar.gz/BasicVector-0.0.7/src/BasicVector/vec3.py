import math
import random


class Vec3:

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.x

    def setY(self, y):
        self.y = y

    def getZ(self):
        return self.z

    def setZ(self, z):
        self.z = z

    def setPos(self, newPos):
        self.x = newPos.x
        self.y = newPos.y
        self.z = newPos.z

    def div(self, i):
        return self / i

    def mult(self, i):
        return self * i

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        self.setPos(self.div(self.length()))

    @classmethod
    def randomIntVec(cls, minX=-50, maxX=50, minY=-50, maxY=50, minZ=-50, maxZ=50):
        x = random.randint(minX, maxX)
        y = random.randint(minY, maxY)
        z = random.randint(minZ, maxZ)
        return Vec3(x, y, z)

    @classmethod
    def randomVec(cls, minX=-50, maxX=50, minY=-50, maxY=50, minZ=-50, maxZ=50):
        x = random.randrange(minX, maxX)
        y = random.randrange(minY, maxY)
        z = random.randint(minZ, maxZ)
        return Vec3(x, y, z)

    @classmethod
    def dist(cls, vectorA, vectorB):
        return math.sqrt((vectorA.x - vectorB.x) ** 2 + (vectorA.y - vectorB.y) ** 2 + (vectorA.z - vectorB.z) ** 2)

    @classmethod
    def lerp(cls, vecA, vecB, step):
        x = (1 - step) * vecA.x + step * vecB.x
        y = (1 - step) * vecA.y + step * vecB.y
        z = (1 - step) * vecA.z + step * vecB.z
        return Vec3(x, y, z)

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vec3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        return Vec3(self.x / other, self.y / other, self.z / other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return f"x = {self.x}, y = {self.y}, z = {self.z}"
