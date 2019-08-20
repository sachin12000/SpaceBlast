import Polygon

#class for bullet
class bullet:
    def __init__(self, position, speed, color, fps): #bullet has a fixed size and speed
        self.fps = fps
        
        self.polygons = [] #polygons that make up the bullet
        for i in range(1, 5):
            r = int(color[0] / float(i))
            g = int(color[1] / float(i))
            b = int(color[2] / float(i))
            color = (r, g, b)
            p = Polygon.polygon([[0,i-1], [1,i-1], [1,i], [0,i]], position, color, 0, False) #points, position, color, width (0=filled), anti aliased
            self.polygons.append(p)

        self.position = []
        self.setPosition(position)

        self.speed = []
        self.setSpeed(speed)

    #Accessors
    def getPolygons(self):
        return self.polygons

    def getPosition(self):
        return self.position

    #mutators
    def setPosition(self, position):
        self.position = []
        self.position.append(float(position[0]))
        self.position.append(float(position[1]))
        for p in self.polygons:
            p.setPosition(self.position)

    def setSpeed(self, speed):
        self.speed = [] #pixels/frame
        self.speed.append(float(speed[0]) / self.fps)
        self.speed.append(float(speed[1]) / self.fps)

    def moveX(self, amount):
        self.setPosition(self.position[0] + amount, self.position[1]) #x, y

    def moveY(self, amount):
        self.setPosition(self.position[0], self.position[1] + amount) #x, y

    def updatePosition(self):
        x = self.position[0] + self.speed[0] #x
        y = self.position[1] + self.speed[1] #y
        self.setPosition([x,y])

    #other
    def checkCollision(self, p):
        p.calEdge()
        p.transformPoints()

        edges = p.getEdges()
        pts = p.getPointsTransformed()
        position = self.getPosition()
        for i in range(-len(pts), 0):
            lb = abs(position[0] - pts[i][0])
            ub = abs(position[0] - pts[i+1][0])
            domain = abs(edges[i][0]) #domain
            if ((lb > domain) or (ub > domain)):
                continue #x value is outside the domain
            
            m = edges[i][1] / edges[i][0] #slope of the line
            b = pts[i][1] - (m * pts[i][0]) #b value. y transform of the line

            yb = (m*position[0]) + b #expected value
            diff = abs(yb - position[1]) #difference compared to the actual value
            if (diff <= 2):
                return True #collision
        return False #no collision

class enemyBullet(bullet): #Bullet Fired by enemy
    def __init__(self, position, speed, color, fps):
        bullet.__init__(self, position, speed, color, fps)

        p = Polygon.polygon([[0,0], [1,0], [1,1], [0,1]], position, color, 0, False) #points, position, color, width (0=filled), anti aliased
        p.setPosition(self.position)
        self.polygons = [p]
