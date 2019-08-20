import random
import Level3

info = None #info about the level
music = None
genLargeAstro = False

enemyDifficulty = 0
enemyFrequency = 2000
textPut = False #flag for indicating if text was already written

def timedAstGen(info, difficulty=-1):
    global genLargeAstro
    
    if (difficulty < 0):
        #random difficulty
        difficulty = random.randrange(info.lb, info.ub)

    if (difficulty == 3):
        #Special case for large asteroid
        genLargeAstro = False
        info.generateAsteroid(-1, -1, difficulty, -1, 1)
        info.astGen = True
        return
    
    info.generateAsteroid(-1, -1, difficulty, -1, 1)
    
def always():
    #The actual level logic
    global info
    global music
    global genLargeAstro
    global enemyDifficulty
    global enemyFrequency
    global textPut
    
    info.updateObjects()
            
    if (info.stage == 0): #stage 1
        if (music.get_pos() > 124000):
            #go to stage 2
            info.gunDelay = 250
            info.dps = 50
            info.stage = 1
            textPut = False
            info.lb = 1
            info.ub = 3
            
        elif (music.get_pos() < 105000):
            if (not(info.astGen)):
                info.info.addTimedEvent(info.timeDelay, [timedAstGen], [[info]])
                info.astGen = True
            if (not(genLargeAstro)):
                #generate large asteroid every 10 seconds
                genLargeAstro = True
                info.info.addTimedEvent(2500, [timedAstGen], [(info, 3)])
            info.timeDelay -= 5.5555e-3
        elif ((not(textPut)) and (music.get_pos() > 113000)):
                textPut = True

                textPos = (info.pfSize[0] * 0.3, info.pfSize[1] * 0.5)
                info.addTimedText("Stage 1 Completed", (255,0,0), textPos, 7000)
                textPos = (info.pfSize[0] * 0.2, info.pfSize[1] * 0.5)
                info.info.addTimedEvent(7000, [info.addTimedText], [("Stage 2. Enemies Incoming!!!", (255,0,0), textPos, 4000)])
    elif (info.stage == 1): #stage 2
        if (music.get_pos() > 240000):
            #go to stage 3
            info.stage = 2
            info.gunDelay = 200
            textPut = False
            info.enemyGen = False
            info.astGen = False

            textPos = (info.pfSize[0] * 0.3, info.pfSize[1] * 0.5)
            info.addTimedText("Stage 2 Completed", (255,0,0), textPos, 4000)
            textPos = (info.pfSize[0] * 0.4, info.pfSize[1] * 0.5)
            info.info.addTimedEvent(4000, [info.addTimedText], [("Stage 3", (255,0,0), textPos, 4000)])
            return
        elif (music.get_pos() <= 214000):
            #update difficulty and frequency
            enemyDifficulty = int(2.2223e-5 * (music.get_pos() - 124000))
            enemyFrequency += 0.022222
        if (music.get_pos() < 225000):
            if (not(info.enemyGen)):
                info.enemyGen = True
                info.info.addTimedEvent(enemyFrequency, [info.generateEnemy], [[enemyDifficulty]])
        
    elif (info.stage == 2): #stage 3
        if (music.get_pos() < 330000): #350
            if (not(info.astGen) and not(info.enemyGen)):
                if (random.randrange(0,2) == 0):
                    #generate asteroid wave
                    info.info.addTimedEvent(5000, [info.generateWave], [(random.randrange(0,3), 5, 11, 0)])
                    info.astGen = True
                else:
                    #generate enemy
                    info.info.addTimedEvent(5000, [info.generateWave], [(random.randrange(0,4), 5, 11, 1)])
                    info.enemyGen = True
        else:
            #Go to level end  
            textPut = False
            info.stage = 3
    elif ((info.stage == 3) and not(textPut) and (music.get_pos() > 340000)): #level end
        textPos = (info.pfSize[0] * 0.3, info.pfSize[1] * 0.5)
        textPut = True
        info.addTimedText("Level 2 Completed", (255,0,0), textPos, 7000)
        info.stage = 4
    elif(music.get_pos() > 347000):
        #Finish level 2 and load level 3
        info.info.removeEvent((always, ()))
        music.stop()
        
        Level3.init(info, music) #begin level 3       
    
def init(i, m):
    global info
    global music
    
    info = i
    info.info.addEvent(always, ())
    
    music = m
    
    textPos = (info.pfSize[0] * 0.4, info.pfSize[1] * 0.5)
    info.addTimedText("Level 2 Stage 1", (255,0,0), textPos, 7000)

    info.astGen = False
    info.enemyGen = False

    info.stage = 0
    info.timeDelay = 1000
    info.gunDelay = 500
    info.dps = 25

    info.lb = 0
    info.ub = 2
    
    music.load("MogueHeart - The Dyson Sphere 89.ogg")
    music.play()
