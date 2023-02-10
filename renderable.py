
class Renderable():
    def __init__(self, x, y, w, h, color, startIndex, amountOfVertices, angle = 0):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.angle = angle
        self.color = color
        self.startIndex = startIndex
        self.amountOfVertices = amountOfVertices
