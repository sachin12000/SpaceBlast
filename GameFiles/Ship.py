import Polygon
import pygame as pg
import circle

class SpaceShip:
    def __init__(self, position, speed, color, lives):
        self.width, self.height = 9.5, 8.5 #Width, Height
        
        self.position = []
        self.position.append(float(position[0]))
        self.position.append(float(position[1]))
            
        self.speed = (float(speed[0]), float(speed[1]))
        self.color = color

        self.health = 100.0
        self.lives = lives #number of lives

        self.outLine = circle.circle(position, 5, color, 2) #Outline of the ship

    #accessors
    def getSize(self):
        return (self.outLine.radius, self.outLine.radius)

    def getPosition(self):
        return self.position

    def getSurface(self):
        return self.s
    
    def getPolygons(self):
        return self.polygons

    def getOutline(self):
        return self.outLine

    def getHealth(self):
        return self.health

    def getLives(self):
        return self.lives

    #mutators
    def setPosition(self, position):
        self.position = [float(position[0]), float(position[1])]
        self.outLine.setPosition(position)
        
    def setColor(self, color):
        self.color = color

    def moveX(self, amount):
        self.position[0] += amount
        self.setPosition([self.position[0], self.position[1]])

    def moveY(self, amount):
        self.position[1] += amount

    def setHealth(self, health):
        self.health = float(health)

    def setLives(self, lives):
        self.lives = lives

    #other
    def checkCollision(self, p): #check collision with a polygon
        return self.outLine.checkCollision(p)
