import pygame as pg
import math

class circle:
    def __init__(self, position, radius, color, width):
        self.position = [float(position[0]), float(position[1])]
        self.radius = float(radius)
        self.color = color
        self.width = width

    def setPosition(self, position):
        self.position = [float(position[0]), float(position[1])]

    def setColor(self, color):
        self.color = color

    def checkCollision(self, p): #Detect collision
        #A collision is registered if at leat one line of the polygon intersects the circle
        #uses the equations of the lines to check for intersection
        p.calEdge()
        p.transformPoints()

        edges = p.getEdges()
        pts = p.getPointsTransformed()
        for i in range(-len(pts), 0):
            if (edges[i][0] == 0): #vertical line
                if (abs(self.position[0] - pts[i][0]) <= self.radius): #close by
                    rng = abs(edges[i][0]) #range
                    lb = abs(self.position[1] - pts[i][1])
                    ub = abs(self.position[1] - pts[i+1][1])
                    if ((lb <= rng) or (ub <= rng)):
                        return True #collision
                continue #no collision
                    
            m = edges[i][1] / edges[i][0] #slope of the line
            c = self.position[0] #x coordinate
            v = self.position[1] #y coordinate
            b = pts[i][1] - (m * pts[i][0]) #b value. y transform of the line

            A = 1 + m**2
            B = (-2*c) + (2*b*m) + (-2*m*v)
            C = b**2 + c**2 + (-2*b*v) + v**2 - self.radius**2

            det = B**2 - 4*A*C #determinant
            if (det < 0): #no collision
                continue

            det = math.sqrt(det)
            x = [(-B + det) / (2*A)]
            x.append((-B - det) / (2*A))
            for xv in x:
                #check for domain and range
                if ((pts[i][0] > xv) and (pts[i+1][0] < xv)):
                    return True #Collision
                if ((pts[i][0] < xv) and (pts[i+1][0] > xv)):
                    return True #Collision
        return False

    def getRenderBundle(self):
        return (self.position, self.radius, self.color, self.width)
