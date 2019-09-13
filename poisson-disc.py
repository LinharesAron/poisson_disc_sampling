import numpy as np
import matplotlib.pyplot as plt
import math
import random

class Point:
    def __init__(self, x,y):
        self.x = x
        self.y = y

    def __add__(self, o):
        return Point(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Point(self.x - o.x, self.y - o.y)
    
    def __mul__(self, f):
        return Point( self.x * f, self.y * f)

    @property
    def sqrt_magnetude(self):
        return float(self.x * self.x + self.y * self.y)


def poission_disc(width, height, radius, n_tries):    
    cellSize = radius / math.sqrt(2)

    widthXCell = math.ceil(width / cellSize)
    heightYCell = math.ceil(height / cellSize)

    grid = [[0 for _ in range(widthXCell)] for _ in range(heightYCell)]
    points = []
    spawns = [Point(width/2, height/2)]
    
    while spawns:
        random_point = random.choice(spawns)
        found = False
        
        for _ in range(n_tries):
            angle = random.random() * math.pi * 2
            dir = Point(math.sin(angle), math.cos(angle))
            next = random_point + dir * random.randrange(radius, 2 * radius)
            if is_valid(next, cellSize, radius, grid, points, width, height):
                points.append(next)
                spawns.append(next)
                grid[int(next.x / cellSize)][int(next.y / cellSize)] = len(points)
                found = True
                break

        if not found:
            spawns.remove(random_point)

    return points

def is_valid(next, cellSize, radius, grid, points, width, height):
    if next.x <= 0 or next.x >= width or next.y <= 0 or next.y >= height:
        return False

    xcell = int(next.x / cellSize)
    ycell = int(next.y / cellSize)

    startX = max([xcell-2, 0])
    endX = min([xcell+2, len(grid[0]) - 1])
    startY = max([ycell-2,0])
    endY = min([ycell+2,len(grid) - 1])

    for x in range(startX, endX + 1):
        for y in range(startY, endY + 1):
            compare = grid[x][y] - 1
            if compare != -1:
                sqrDst = (next - points[compare]).sqrt_magnetude
                if sqrDst < radius * radius:
                    return False
    return True

    


aspect = 3/3

width = 100
height = width / aspect

radius = 50

points = [[p.x, p.y] for p in poission_disc(width, height, radius, 30)]
s = [ radius * radius for _ in points]

plt.scatter( *zip(*points), s=s, c='g', alpha=0.6, lw=0)

plt.xlim(0,width)
plt.ylim(0,height)
# plt.axis('off')
plt.show()