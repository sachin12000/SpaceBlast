import pygame as pg
import Polygon

#class for representing an asteroid
class asteroid(Polygon.polygon):    
    def __init__(self, position, pts, rotation, speed, color, width, fps):
        self.fps = float(fps) #fps

        self.rotationAngle = None #Rotation per frame
        self.rotation = rotation #Rotation rads/second
        self.rotating = False #Is it rotating?
        asteroid.setRotation(self, rotation) #Rotation per frame

        self.speed = None #(x,y) pixels per second
        self.setSpeed(speed)

        self.health = 100.0
        self.hit = 0 #is the asteroid hit. MSB contains enabled flag
        self.colorCopy = tuple(color) #tuple makes sure that the copy will not be changed (immutable)
        
        Polygon.polygon.__init__(self,pts, position, color, width)

    #accessors
    def getHealth(self):
        return self.health

    #mutators
    def setRotation(self, rotation): #Sets rotation values
        if (abs(rotation) < 1e-4): #rotation too small
            self.rotating = False
            return
        self.rotating = True
        self.rotationAngle = rotation / self.fps #radians/frame

    def setSpeed(self, speed):
        x = speed[0] / self.fps
        y = speed[1] / self.fps
        self.speed = (x,y)

    def rotateSelf(self): #Rotate
        self.rotate(self.rotationAngle)

    def rotateCustom(self, angle): #Rotates a custom angle Radians
        self.rotate(angle)

    def updatePosition(self):
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]

    def update(self): #updates position. rotation, color
        self.position = (self.position[0] + self.speed[0],self.position[1] + self.speed[1] )
        if (self.rotating):
            self.rotateSelf()
        if(self.hit & 0x80000000): #if hit enabled
            self.hit -= 1
            if (not(self.hit & 0x80000000)): #hit duration is over
                self.color = self.colorCopy
        
    def setHealth(self, health):
        self.health = health

    def hitEnable(self, amount, color): #changes the color for a given time after hit
        if ((amount > 0) and (int(amount * self.fps) < 0x8000)): #delay within limits?
            self.hit = (0x80000000 | (int(amount * self.fps)))
            self.setColor(color)
        
