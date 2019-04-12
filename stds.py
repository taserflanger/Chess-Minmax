import operator
class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        if type(other)==Vector:
            return Vector(self.x+other.x, self.y+other.y)
        else:
            return Vector(self.x+other[0], self.y+other[1])
    def __mul__(self, value):
        return Vector(self.x*value, self.y*value)
    def __eq__(self, other):
        return self.x==other.x and self.y==other.y
    def __repr__(self):
        return "({}{})".format(chr(self.x+97), str(8-self.y))
    def isInBoard(self):
        return 0 <= self.x <= 7 and 0 <= self.y <= 7
            