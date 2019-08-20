import pygame as pg
import InitDisplay

import Polygon as p
import Transform
import Events
import Menus

class info(object): #Info needed for the level script
    #an instance of this class is passed as an arguement to the level scripts
    def __init__(self, addEvent, addTimedEvent, removeEvent, getFrameCount, getPause, setPause, quitGame, collidablePolygons, visiblePolygons, visibleText, visibleSurface, visibleCircles, size, fps, d):
        self.addEvent = addEvent
        self.addTimedEvent = addTimedEvent
        self.removeEvent = removeEvent
        self.getFrameCount = getFrameCount
        self.getPause = getPause
        self.setPause = setPause
        self.quitGame = quitGame
        
        self.collidablePolygons = collidablePolygons        
        self.visiblePolygons = visiblePolygons
        self.visibleText = visibleText
        self.visibleSurface = visibleSurface
        self.visibleCircles = visibleCircles

        self.size = size
        self.fps = fps
        self.d = d
        
def addEvent(function, args): #Adds event to run always list
    runAlways.append((function, args))
    
def addTimedEvent(time, functions, args): #Schedules events
    Events.insertEvent(time, frameCount, functions, args)

def removeEvent(func): #Remove event from run always
    #del runAlways[index]
    runAlways.remove(func)

def removeTimedEvent(index): #Removes timed event
    del Events.Events[index]

def getFrameCount():
    return frameCount

def getPause():
    return paused

def setPause(value, mode=None, additionalParam=None): #enables or disables pause
    global paused
    global callPause
    paused = value
    if ((mode != None) and (value == True)):
        callPause(mode, additionalParam) #parameter 1 indicates that it is currently in game

def quitGame():
    global playing
    playing = False

def initLevel():
    return info(addEvent, addTimedEvent, removeEvent, getFrameCount, getPause, setPause, quitGame, collidablePolygons, visiblePolygons, visibleText, visibleSurface, visibleCircles, size, fps, d)

fps = 40.0

pfSize = (160, 200) #Size of the playfield

pg.init()
inits = InitDisplay.initDisplay((0.8,1),0.8, "Space Blast", fps) #Initializes using InitDisplay module
d = inits[0] #display
size = inits[1] #size
clk = inits[2] #clock
T = inits[3] #time per frame
Events.init(T) #initialize events

fullScreen = False
playing = True #sentinel for the main loop

frameCount = 0 #Frame Counter

collidablePolygons = [] #Objects that can collide

visiblePolygons = [] #Polygons that are visible
visibleCircles = [] #Circles that are visible
visibleText = []
visibleSurface = [] #List of surfaces that are visible

runAlways = [] #functions that run every frame

lvlInfo = initLevel() #Info needed for the level scripts

pauseFunction, callPause = Menus.init(lvlInfo) #Init menues and level scripts. Return value is the pause function
setPause(True, 0) #call the main menu
#runAlways.append((lvlFunc[0], lvlFunc[1])) #level function that will run every iteration

keyEventFunc = Menus.getKeyEvent() #function that handles key presses

paused = True #is game paused

while (playing):
    clk.tick()
    if (not(paused)):
        frameCount += 1
    
    for event in pg.event.get(): #Event Handling
        if (event.type == pg.QUIT):
            #quit
            playing = False
            break
        elif ((event.type == pg.KEYDOWN) or (event.type == pg.KEYUP)):
            keyEventFunc(event.key, not(event.type - 2)) #event.type - 2 equals 1 or 0

    if (not(paused)):
        frameCount += 1

        for i in range(len(runAlways)): #run functions that run every frame
            runAlways[i][0](*runAlways[i][1]) #function (*args)
        
        if (Events.checkForEvents(frameCount)): #execute timed event
            for i in range(len(Events.Events[0][1])): #First event on the queue
                Events.Events[0][1][i] (*Events.Events[0][2][i])
            del Events.Events[0]
    else:
        #call the pause function if paused
        pauseFunction()
        
    #Draw polygons, text, surfaces
    for vp in visiblePolygons:
        Transform.transformAndRender(d, size, pfSize, False, None, vp)
    Transform.tranformTextRender(d, (0,0), size, pfSize, False, None, visibleText)
    Transform.drawS(visibleSurface, d, size, pfSize)
    Transform.drawCircle(d, size, pfSize, False, None, visibleCircles)


    pg.display.update()
    d.fill((0,0,0)) #clear
    pg.time.delay(T - clk.tick()) #delay until frame ends

pg.quit()
