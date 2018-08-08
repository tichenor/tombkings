

class Rectangle:

    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        c_x = (self.x1 + self.x2) / 2
        c_y = (self.y1 + self.y2) / 2
        return int(c_x), int(c_y)

    def intersect(self, other):
        return self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1

    def inner_edges(self):
        edges = []
        for x in range(self.x1 + 1, self.x2):
            for y in range(self.y1 + 1, self.y2):
                edges.append((x, y))

        for x in range(self.x1 + 2, self.x2 - 1):
            for y in range(self.y1 + 2, self.y2 - 1):
                if (x, y) in edges:
                    edges.remove((x, y))

        for x in range(self.x1, self.x2):
            y = (self.y1 + self.y2) / 2
            if (x, y) in edges:
                edges.remove((x, y))

        return edges
