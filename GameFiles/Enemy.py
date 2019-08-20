import Asteroid
import random
import math
import Polygon
import Bullet
import math

class enemy(Asteroid.asteroid): #represents an enemy
    def __init__(self, bulletlst, ship, nOfSides, width, fps, pfSize, difficulty=0, position=-1, rotation=None, speed=None):
        pts = list(Polygon.generatePolygon(2, nOfSides, 1, (0,0)))
        color = None
        if (difficulty == 0):  #easy to hard
            color = (74, 255, 120)
        elif(difficulty == 1):
            color = (129, 107, 255)
        elif(difficulty == 2):
            color = (251, 125, 0)
        elif(difficulty == 3):
            color = (243, 30, 18)
        else:
            raise TypeError
        radius = pfSize[1] * 0.05 #size of the enemy
        self.attackFrequency = int((4 - difficulty) * fps) #Frequency of attack
        self.attackCountDown = self.attackFrequency
    
        for i in range(len(pts)):
            x = pts[i][0] * radius
            y = pts[i][1] * radius
            pts[i] = (x,y)
        if (position == -1):
            #default location
            position = pfSize[0] - (radius * 1.5)
            position = (pfSize[0] - position) + (position * random.random())
            position = (position, -2 * radius)
        
        if (rotation == None):
            #default rotation
            rotation = (math.pi / 2) * random.random() + (math.pi / (4 - difficulty))
        if (speed == None):
            #default speed
            speed = (0, pfSize[1] / 20.0)
        rotation = math.pi / 5
        Asteroid.asteroid.__init__(self, position, pts, rotation, speed, color, width, fps) #init some parts

        self.setHealth(100 * (3.25 + difficulty)) #health
        self.ship = ship #needed for shooting at
        self.bullets = bulletlst
        self.pfSize = pfSize
        self.yLimit = pfSize[1] * 0.7 #dont fire after a certain y coordinate
            
    def update(self): #update enemy data
        Asteroid.asteroid.update(self) #update position, rotation, color
        if (self.position[1] > self.yLimit):
            return #dont fire bullets
        self.attackCountDown -= 1
        if (self.attackCountDown < 1):
            #fire bullet if count down is zero
            #fires at the ship
            #The code calculates the velcity vector that is pointing at the current position at the ship
            self.attackCountDown = self.attackFrequency #reset attack delay counter
            shipPos = self.ship.getPosition()
            dx = (shipPos[0] - self.position[0])
            dy = (shipPos[1] - self.position[1])
            k = math.sqrt(1600.0 / (dx**2 + dy**2)) #final speed must be 40.k is the scalar
            dx *= k #x speed componenet
            dy *= k #y speed componenet
            b = Bullet.enemyBullet(self.position, (dx,dy), self.colorCopy, self.fps)
            self.bullets[0].append(b)
            self.bullets[1] += b.getPolygons()       
