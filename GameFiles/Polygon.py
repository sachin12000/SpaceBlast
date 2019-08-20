import math
import random

#Module Functions
def generatePolygon(radius, sides, pType, transform): #Generates a convex polygon
    points = [] #points of the polygon
    points.append((radius + transform[0], transform[1])) #First point
    
    interval = (2 * math.pi) / sides #interval to increase by

    for i in range(0, sides):
        if (pType == 0): #Random Polygon
            angle = (i * interval) + (interval * random.random())
        else:
            angle = i * interval #evenly spaced polygon

        x = (math.cos(angle) * radius) + transform[0] #x coordinate
        y = (math.sin(angle) * radius) + transform[1] #y coordinate
        points.append((x,y))
            
    return points

#Polygon Class
class polygon(object):
    
    def __init__(self, pts, position, color, width, antialiased=True):
        self.setPosition(position) #Position
        self.color = color #color
        self.width = width #Line width

        self.points = [] #Coordinates relative to (0,0)        
        self.centroid = None #Position of the centroid
        self.dCentroid = [] #distance to centre of mass
        self.radius = 0 #Distance between the furthest point and the center

        self.antiAliased = antialiased
        
        for i in range(len(pts)): #copy all points
            self.points.append((float(pts[i][0]), float(pts[i][1])))
        
        polygon.calCentroid(self)
        polygon.calDistToCentroidRadius(self)

        self.pointsTransformed = [] #Transformed points
        self.edges = [] #A list of edges

    def calCentroid(self): #Calculate centroid and the distance to points
        Cx = 0.0 #centre x
        Cy = 0.0 #centre y
        A = 0.0 #signed area
        s = 0.0 #temp variable
        
        for i in range(len(self.points) - 1):
            s = (self.points[i][0]*self.points[i+1][1]) - (self.points[i+1][0]*self.points[i][1]) #x*y1 - x1*y
            
            Cx += (self.points[i][0] + self.points[i+1][0]) * s
            Cy += (self.points[i][1] + self.points[i+1][1]) * s
            A += s

        A /= 2 #value of signed area

        A = 1 / (6*A)
        Cx *= A
        Cy *= A

        self.centroid = (Cx, Cy) #Centroid

    #Public functions
    def rotate(self, angle):
        sinAngle = math.sin(angle)
        cosAngle = math.cos(angle)
        
        for i in range(len(self.points)):
            x = (self.dCentroid[i][0] * cosAngle) - (self.dCentroid[i][1] * sinAngle)  #New x = centroidX + dCentroidRotated
            y = (self.dCentroid[i][0] * sinAngle) + (self.dCentroid[i][1] * cosAngle)  #New y = centroidX + dCentroidRotated

            self.dCentroid[i] = (x,y) #new centroid distance
            
            x += self.centroid[0]
            y += self.centroid[1]
            
            self.points[i] = (x,y) #Roatated point

    def calDistToCentroidRadius(self): #Calculates distance from each point to centroid
        self.dCentroid = []
        for p in self.points:
            dx = p[0] - self.centroid[0]
            dy = p[1] - self.centroid[1]
            self.dCentroid.append((dx, dy)) #x,y

            dist = (dx**2) + (dy**2) #Calculate radius
            if (dist > self.radius):
                self.radius = dist
        self.radius = math.sqrt(self.radius)
            
    #Accessors
    def getPoints(self):
        return self.points

    def getColor(self):
        return self.color

    def getWidth(self):
        return self.width

    def getPosition(self):
        return self.position

    def getRadius(self):
        return self.radius

    def getEdges(self):
        return self.edges

    def getPointsTransformed(self):
        return self.pointsTransformed

    def getRenderBundle(self): #Get all data needed for drawing
        return (self.position, self.points, self.color, self.width)

    def isAAed(self): #is anti aliased
        return self.antiAliased

    #Mutators
    def setColor(self, color):
        self.color = color

    def setWidth(self, width):
        self.width = width

    def setPosition(self, position):
        self.position = []
        self.position.append(float(position[0]))
        self.position.append(float(position[1]))

    def setAA(self, enabled): #set anti alias
        self.antiAliased = enabled

    def transformPoints(self): #Transforms all points. only used for collision detection
        self.pointsTransformed = []
        for p in self.points:
            x = p[0] + self.position[0]
            y = p[1] + self.position[1]
            self.pointsTransformed.append([x,y])

    def calEdge(self): #Calculate length of all edges. only used for collision detection
        self.edges = []
        for i in range(-len(self.points), 0): #Length of all edges
            x = self.points[i+1][0] - self.points[i][0]
            y = self.points[i+1][1] - self.points[i][1]
            self.edges.append((float(x), float(y)))
