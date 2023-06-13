class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f'{self.x} - {self.y}'
    def __str__(self):
        return f'{self.x} + {self.y}'

p = Point(2, 3)

print(p) # 2 + 3
print(str(p)) # 2 + 3
print(eval(str(p))) # 5
print(repr(p)) # 2 - 3
print(eval(repr(p))) # -1