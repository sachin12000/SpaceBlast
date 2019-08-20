import random
import Level2

info = None
music = None

#always function runs every frame
def always():
    global info
    info.updateObjects()
    
    if (info.stage == 0): #Stage 0
        if  (music.get_pos() > 21530):           
            info.stage = 1
        else:
            return
    elif (info.stage == 1): #Stage 1
        if (music.get_pos() < 168000):
            if (not(info.astGen)):
                info.astGen = True
                info.timeDelay -= 1500.0 / 138000
                info.speedFactor += (0.5 / 138000)
                info.info.addTimedEvent(info.timeDelay, [info.generateAsteroid], [(-1,-1,random.randrange(0,2),info.speedFactor)])
        elif ((music.get_pos() > 168000) and not(info.astGen)):
            info.astGen = True
            info.addTimedText("Get Ready For Stage 2", (255,0,0), (info.pfSize[0] * 0.3, info.pfSize[1] * 0.5), 7000)
        if(music.get_pos() > 188305): #188305
            info.stage = 2 #stage 2 begin            
            info.generateWave(0, info.lb, info.ub)
            info.addTimedText("Stage 2", (255,0,0), (info.pfSize[0] * 0.4 , info.pfSize[1] * 0.5), 3000)
    elif (info.stage == 2): #Stage 2
        if (music.get_pos() > 313530):
            info.stage = 3 #stage 2 end
        if (not(info.astGen)):
            info.astGen = True
            c = 3 / 313500.0
            info.lb = 3 + int(c * music.get_pos())
            info.ub = 2 + info.lb
            info.info.addTimedEvent((music.get_pos() - 188310) % 5000, [info.generateWave], [(0, info.lb, info.ub)])
    elif (info.stage == 3): #level 1 end
        info.addTimedText("Level 1 Completed", (255,0,0), (info.pfSize[0] * 0.35, info.pfSize[1] * 0.5), 7000)
        info.stage = 4
    else: #load level 2
        if (music.get_pos() > 324000):
            #start level 4
            info.info.removeEvent((always, ()))
            music.stop()
            Level2.init(info, music) #keep using the same music object
    
def init(i, m):
    global info
    global music

    info = i
    music = m

    info.stage = 0
    info.astGen = False #asteroid generation flag
    info.enemyGen = False #enemy generation flag

    info.timeDelay = 2000 #asteroid delay
    info.gunDelay = 500 #time between 2 shots
    info.dps = 25 #damage per shot

    #lower and upper bound for the number of asteroid
    info.lb = 3
    info.ub = 5

    info.addTimedText("Level 1 Stage 1", (255,0,0), (info.pfSize[0] * 0.4, info.pfSize[1] * 0.5), 7000)
    
    music.load("Dreamstate Logic - Ad Astra (To The Stars) 92.ogg")
    music.play()
    
    info.info.addEvent(always, ()) #Level event that runs every frame

def getKeyEvent():
    return info.keyEvent
