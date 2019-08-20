import random

info = None #info class
music = None #music object

difficulty = 0
enemyFrequency = 2000 #delay between 2 enemy generations

def always():
    global music
    global music
    global difficulty
    global enemyFrequency
    
    info.updateObjects()
    
    if (info.stage == 0):
        if (music.get_pos() < 185000):
            #update diffculty and frequency
            difficulty = int(2e-5 * (music.get_pos() - 7000))
            enemyFrequency = 2000 + (music.get_pos() * 1.3333e-2)
            if (not(info.enemyGen)):
                #generate enemy
                info.enemyGen = True
                time = (random.random() * enemyFrequency) + 1000
                info.info.addTimedEvent(time, [info.generateEnemy], [[difficulty]])
        else: #Level End
            info.stage = 1
    elif (music.get_pos() > 205000): #game completed
        info.endGame()
        
def init(i, m):
    global info
    global music

    info = i
    info.info.addEvent(always, ())
    
    music = m
    
    textPos = (info.pfSize[0] * 0.45, info.pfSize[1] * 0.5)
    info.addTimedText("Level 3", (255,0,0), textPos, 7000)

    info.astGen = False
    info.enemyGen = False

    info.stage = 0
    info.astGen = False
    info.timeDelay = 1000
    info.gunDelay = 250
    info.dps = 50

    info.lb = 0
    info.ub = 2
    
    music.load("HOME - Resonance 85.ogg")
    music.play()
