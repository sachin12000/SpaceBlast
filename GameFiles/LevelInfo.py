import random
import math
import pygame as pg
import Polygon
import Asteroid
import Enemy
import Bullet
import GameText
import Transform

class LevelInfo: #This class contains functions and data needed for levels
    #this class losely structured.
    def __init__(info): #replaced self with info for convenience
        info.pfSize = (160,200) #size of the playfield
        info.info = None #info class from the main loop
        info.menuKeyHandle = None #function that handles key presses for the menu
        info.music = None #music object of the game

        info.astList = []
        info.astList = [] #List of asteroids
        info.astEvents = [] #List of functions from asteroid class that run every frame
        info.nOfAst = -1 #number of asteroid (index)
        info.astGen = False #flag. turns false after an asteroid was generated
        info.enemyGen = False #flag. turns false after an enemy was generated
        info.nOfLives = 3 #number of lives

        info.enemies = [] #a list of enemies
        
        info.bullets = [[],[]] #list of bullets [bullet, polygons]
        info.enemyBullets = [[], []] #list of enemy bullets

        info.ship = None
        info.hit = False #Ship is hit
        info.surfaceSize = 0

        info.shipSpeed = 0 #Sideways speed of the ship
        info.leftKey = False #left key pressed
        info.rightKey = False #right key pressed
        info.score = 0

        info.scoreText = None
        info.lifeText = None
        info.healthText = None

        info.timeDelay = 2000 #A delay. could be used for anything 

        info.speedFactor = 0.5 #multiplication factor of asteroid speed
        info.astSpeed = 15

        info.stage = 1 #curent stage
        info.gunDelay = 500 #delay between firing
        info.dps = 25 #damage per shot

        #lower and upper bound. general purpose
        info.lb = 3
        info.ub = 5

    def initOtherData(info): #initializes remaining data
        info.lifeText = GameText.GameText("Lives: " + str(info.ship.getLives()), 8, None, (info.pfSize[0] * 0.8 , 3), (0,255,0)) #Displays # of lives
        info.info.visibleText.append(info.lifeText)
        Transform.resizeText(info.info.size, info.pfSize, info.lifeText)

        #Create amount of health text
        info.healthText = GameText.GameText("Health: " + str(int(info.ship.getHealth())), 8, None, (info.pfSize[0] * 0.8 , 8), (0,255,0)) #Displays current health
        Transform.resizeText(info.info.size, info.pfSize, info.healthText)
        info.info.visibleText.append(info.healthText)

        #create score text
        info.scoreText = GameText.GameText("Score: " + str(int(info.score)), 8, None, (info.pfSize[0] * 0.02, 3), (0,255,0))
        Transform.resizeText(info.info.size, info.pfSize, info.scoreText)
        info.info.visibleText.append(info.scoreText)
        
        #info.visiblePolygons.append(ship.getPolygons())
        info.info.visiblePolygons.append(info.astList) #show asteroid polygons
        info.info.visiblePolygons.append(info.enemies) #display enemies
        info.info.visiblePolygons.append(info.bullets[1]) #show bullet polygons
        info.info.visiblePolygons.append(info.enemyBullets[1])

        info.timedFire() #start firing

    def addTimedText(info, text, color, position, duration, font=None, size=10): #displays text for a certain time period
        txt = GameText.GameText(text, size, font, position, color) #Displays current health
        Transform.resizeText(info.info.size, info.pfSize, txt)
        info.info.visibleText.append(txt)
        info.info.addTimedEvent(duration, [info.info.visibleText.remove], [[txt]])

    def enableHit(info): #Enables ship hits
        info.hit = False

    def keyEvent(info, key, action): #Handle key presses, action 0 = KEYDOWN, 1 = KEYUP
        if (info.info.getPause()):
            #if already paused
            info.menuKeyHandle(key, action)
            return

        if ((key == pg.K_LEFT) or (key == pg.K_a)): #move left
            info.leftKey = action #action is either 1 or 0
        elif ((key == pg.K_RIGHT) or (key == pg.K_d)): #move right
            info.rightKey = action #action is either 1 or 0
        elif ((key == pg.K_ESCAPE) and (action == 1)): #0 = key down
            if (not(info.info.getPause())):
                #pause game
                info.music.pause()
                info.info.setPause(True, 1)

    def updateObjects(info): #updates all objects in the game
        if (info.leftKey & (info.ship.getPosition()[0] > 0)): #Move left
            info.ship.moveX(-info.shipSpeed)
        elif (info.rightKey & (info.ship.getPosition()[0] < info.pfSize[0])): #Move right            
            info.ship.moveX(info.shipSpeed)
        
        i = -1
        info.shipPos = info.ship.getPosition() #position of the ship
        info.shipWidth = info.ship.getSize()[0]
        while (i < info.nOfAst): #Run asteroid events and check for collision
            i += 1
            if ((info.astList[i].getPosition()[1] - info.astList[i].getRadius()) > info.pfSize[1]): #Removes if the asteroid if its outside the Screen
                del info.astList[i]
                del info.astEvents[i]
                info.nOfAst -= 1
                continue
            
            #Check asteroid collision with the ship
            if (not(info.hit)): #Ship is already hit
                dist = info.calDistance2D(info.shipPos, info.astList[i].getPosition()) #Distance between the asteroid an the ship
                dist -= info.astList[i].getRadius()
                dist = abs(dist)

                if (dist < info.shipWidth): #Asteroid closeby
                    if(info.ship.checkCollision(info.astList[i])):
                        info.collision(info.ship, 0) #update health
            info.astEvents[i][0](*info.astEvents[i][1])

        index = 0
        while(index < len(info.bullets[0])): #update bullet data
            info.bullets[0][index].updatePosition()
            if (info.bullets[0][index].getPosition()[1] < (info.pfSize[1] * -0.125)):
                #bullet outside the screen
                for i in range(len(info.bullets[0][index].getPolygons())): #remove bullet
                    del info.bullets[1][index]
                del info.bullets[0][index] #remove bullet
                continue
            for i in range(len(info.astList)):# Check bullets colliding with asteroids
                if(info.bullets[0][index].checkCollision(info.astList[i])): #collision check
                    #collided with an asteroid
                    info.bullets[0][index].setPosition((0, info.pfSize[0] * -2))
                    info.astList[i].hitEnable(0.15, (255,255,255)) #changes color for 0.15 seconds
                    info.astList[i].setHealth(info.astList[i].getHealth() - info.dps) #Set health
                    if (info.astList[i].getHealth() < 1): #asteroid destroyed
                        info.score += abs(int(info.astList[i].getRadius() * info.astList[i].getPosition()[1]) / 2) #update score
                        info.scoreText.setText("Score: " +  str(int(info.score)))
                        info.astList[i].setPosition([info.pfSize[0], info.pfSize[1] * 2])
                    break
            index += 1

        index = 0
        shipRadiusSqrd = (info.ship.getSize()[0])**2 #radius of the ship squared. Used for collision detection
        shipPos = info.ship.getPosition()
        while(index < len(info.enemyBullets[0])): #update all enemy bullet data
            info.enemyBullets[0][index].updatePosition()
            if (info.hit):
                index += 1
                continue #already hit.
            pos = info.enemyBullets[0][index].getPosition()
            if ((pos[1] > info.pfSize[1]) or (pos[0] < 0) or (pos[0] > info.pfSize[0])):
                #bullet outside the screen
                for i in range(len(info.enemyBullets[0][index].getPolygons())): #remove bullet
                    del info.enemyBullets[1][index]
                del info.enemyBullets[0][index] #remove bullet
                continue
            dist = (pos[0] - shipPos[0])**2
            dist += (pos[1] - shipPos[1])**2
            if (dist <= shipRadiusSqrd): #enemy bullet near the ship
                info.collision(info.ship, 1) #check for collision
                
            index += 1
    
    def randColor(info, s,e): #generates a random color
        r = random.randrange(s, e)
        g = random.randrange(s, e)
        b = random.randrange(s, e)
        return (r,g,b)
    
    def calDistance2D(info, p1, p2): #calculate distance between 2 2d points
        d = (p1[0] - p2[0])**2
        d += (p1[1] - p2[1])**2
        return math.sqrt(d)

    def collision(info, ship, colType):
        ret = False #return value. indicates if the game is over (lives < 0)
        if (colType == 0): #Asteroid Collision
            ship.setHealth(ship.getHealth() - 25)
        elif (colType == 1): #Bullet
            ship.setHealth(ship.getHealth() - 20)

        if (ship.getHealth() <= 0): #Life Lost
            ship.setLives(ship.getLives() - 1)
            ship.setHealth(100)
            info.lifeText.setColor((255,0,0))

        if (ship.getLives() < 0): #Game Over
            ship.setLives(0)
            ship.setHealth(0)
            info.info.setPause(True, 2, info.score)
            ret = True
        
        #update health text
        info.healthText.setText("Health: " + str(int(info.ship.getHealth())))
        info.healthText.setColor((255,0,0))
        #update life text
        info.lifeText.setText("Lives: " + str(int(info.ship.getLives())))

        #set flag to indicate that the ship is hit
        info.hit = True
        #clear the flag after 5 seconds
        info.info.addTimedEvent(5000, [info.enableHit, info.healthText.setColorRGB, info.lifeText.setColorRGB], [(), (0,255,0), (0,255,0)])

        return ret

    def timedFire(info): #fires periodically
        if (info.gunDelay < 1):
            return #firing disabled
        b = Bullet.bullet(info.ship.getPosition(), (0,-80), (255,255,255), info.info.fps)
        info.bullets[0].append(b)
        info.bullets[1] += b.getPolygons()

        info.info.addTimedEvent(info.gunDelay, [info.timedFire], [()])
        
    def generateAsteroid(info, radius=-1, x=-1, asteroidType = -1, speed=-1, speedFactor=1): #generates and asteroid
        info.astGen = False #clear flag
        factor = 1
        astRadius = 0
        
        if (asteroidType < 0): #random asteroid type
            asteroidType = random.randrange(0,3)
            
        if (asteroidType==0): #largest to smallest aseroid size
            factor= 0.25
            speed = 50
            astRadius = (10, 30)
        elif (asteroidType==1):
            factor = 0.5
            speed = 35
            astRadius = (30, 40)
        else:
            factor = 1
            speed = 20
            astRadius = (40, 50)
        if (speed < 0): #default speed
            speed *= speedFactor
            speed = (speed * random.random()) + (speed / 2.0)
        speed = (0, speed)
        
        radius = int(factor * random.random() * (astRadius[1] - astRadius[0])) + astRadius[0] #rotation
        radius = random.randrange(astRadius[0], astRadius[1]) * factor
        if (x < 0): #random position
            x = (random.random() * (info.pfSize[0] - radius)) + radius #x coordinate
        position = (x, -radius)

        health = 100 * (radius / (50.0 * factor))

        pts = Polygon.generatePolygon(radius, random.randrange(4,9), 0, (0,0)) #Asteroid with random radius
        a = Asteroid.asteroid(position, pts, 0.5*math.pi*random.random() - (0.25 * math.pi), speed, info.randColor(127, 256), 2, info.info.fps)

        a.setHealth(health)

        info.astList.append(a)
        info.astEvents.append((a.update, ()))
        info.nOfAst += 1

    def generateEnemy(info, difficulty=0, nOfSides=0, position=-1):
        info.enemyGen = False #clear flag
        if (nOfSides < 3): #not a polygon
            nOfSides = random.randrange(3, 10)
        #generate enemy
        enemy = Enemy.enemy(info.enemyBullets, info.ship, nOfSides, 2, info.info.fps, info.pfSize, difficulty, position)
        #info.enemies.append(enemy)
        info.astList.append(enemy)
        info.astEvents.append((enemy.update, ())) #List of functions from asteroid class that run every frame
        info.nOfAst += 1 #number of asteroid (index)

    def generateWave(info, difficulty=-1, lb=2, ub=3, Type=0): #generates a wave of asteroids
        #numberInWave = 0 
        if (difficulty < 0):
            diffifulty = 0
        numberInWave = random.randrange(lb, ub) #number of asteroids in the wave
        width = info.pfSize[0] * 0.9
        asteroidList = []
        percentages = [] #percentages of asteroids of different sizes
        if (difficulty == 0): #from easy to hard
            asteroidList += [0] * int(0.5 * numberInWave) #small asteroids
            asteroidList += [1] * int(0.4 * numberInWave) #medium asteroids
            asteroidList += [2] * int(0.1 * numberInWave) #large asteroids
        elif (difficulty == 1):
            asteroidList += [0] * int(0.4 * numberInWave)
            asteroidList += [1] * int(0.3 * numberInWave)
            asteroidList += [2] * int(0.3 * numberInWave)
        elif (difficulty == 2):
            asteroidList += [0] * int(0.2 * numberInWave)
            asteroidList += [1] * int(0.4 * numberInWave)
            asteroidList += [2] * int(0.4 * numberInWave)
        elif ((difficulty == 3) and (Type == 1)):
            #difficulty level 4 for enemies
            asteroidList += [1] * int(0.2 * numberInWave)
            asteroidList += [2] * int(0.4 * numberInWave)
            asteroidList += [3] * int(0.4 * numberInWave)
        random.shuffle(asteroidList) #randomize the order

        p = info.pfSize[0] / float(numberInWave)
        for i in range(len(asteroidList)): #generate asteroids
            if (Type == 0): #asteroid
                info.generateAsteroid(-1, -1 ,asteroidList[i], info.astSpeed, info.speedFactor)
            elif (Type == 1):
                x = (p * i) + (numberInWave * random.random()) #x coordinate
                info.generateEnemy(difficulty=asteroidList[i], position=(x, -50))

    def endGame(info): #final level is complete
        info.info.setPause(True, 3, info.score)
