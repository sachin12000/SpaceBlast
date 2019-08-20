#handles all menu related functions. Starts levels.
import LevelInfo
import pygame
import GameText
import Ship
import Transform
import Level1
import Level2
import Level3

info = LevelInfo.LevelInfo() #utility class for the level scripts
music = pygame.mixer.music
pygame.mixer.init()

loopInfo = None #info class from the main loop

currentMenu = 0 #current menu, ex: main menu
currentChoice = [-1,-1,-1] #current menu choice, number of total choices, number of text objects

initIsDone = False #flag indicating if level data was initialized

menuStack = [] #A list that contains menu choices in order. used to going back the menu
pauseMode = -1 #pause mode

menuColors = [(213,37,28), (125,36,223)]

def initLevel(): #initializes data needed for levels
    global initIsDone
    global info

    if (initIsDone):
        #dont initialize if it is already initialized
        return
    initIsDone = True #set flag
    #clear all lists
    del info.info.visiblePolygons[:]
    del info.info.visibleText[:]
    del info.info.visibleCircles[:]
    
    #Create ship
    info.shipSpeed = float(info.pfSize[0]) / info.info.fps / 3 #Sideways speed of the ship
    shipPos = (0,0)    
    info.ship = Ship.SpaceShip(shipPos, (0,0), info.randColor(127, 256), 3)
                            
    shipPos = [info.pfSize[0] / 2, 3]#Position of the ship
    shipPos[1] = info.pfSize[1] - (info.ship.getSize()[1] * 1.5)
    info.ship.setPosition(shipPos)
    info.info.visibleCircles.append(info.ship.getOutline())
    info.initOtherData()

def selected(key): #A choice from the menu is selected
    global currentMenu
    global currentChoice
    global pauseMode

    if ((key == pygame.K_ESCAPE) or (key == pygame.K_q)): #go back or quit
        if (pauseMode == 0):
            if (len(menuStack) > 0):
                generatePauseMenu(-1) #clear previous menu
                generatePauseMenu(0) #go back to main menu
                del menuStack[-1]                
        elif (pauseMode == 1): #return to game
            generatePauseMenu(-1) #remove all text
            if (key == pygame.K_ESCAPE):
                info.info.setPause(False) #go back to the game
            else:
                info.info.quitGame() #quit if key == q
            music.unpause()
        elif (((pauseMode == 2) or (pauseMode == 3)) and (key == pygame.K_q)): #game over or game complete menu
            info.info.quitGame()
        return
    
    if (key == pygame.K_RETURN): #go to the next menu
        generatePauseMenu(-1) #remove menu text from the screen
        if (currentMenu == 0):
            #currently at the main menu
            menuStack.append(currentMenu)
            if (currentChoice[0] == 0):
                #go to level selction
                generatePauseMenu(3) #generate level selection menu
            elif (currentChoice[0] == 1):
                #show Help
                generatePauseMenu(5)
            elif (currentChoice[0] == 2):
                #quit
                currentChoice = [0,0]
                info.info.quitGame()
        elif(currentMenu == 3): #level selection
            initLevel() #initialized level data
            info.info.setPause(False) #disble pause mode
            if (currentChoice[0] == 0): #start level 1
                Level1.init(info, music)
            elif (currentChoice[0] == 1):
                Level2.init(info, music)
            else:
                Level3.init(info, music)
        elif ((pauseMode == 2) or (pauseMode == 3)): #game over
              info.info.quitGame()
    
def menuKeyHandle(key, action): #handle key presses for the menu
    global currentChoice
    
    if (not(action)): #not keydown
        return
    handled = False
    if (not(currentChoice[1] < 1)): #not a menu without any selections
        temp = currentChoice[0] #temp needed for ading and removing the arrow
        if (key == pygame.K_UP):            
            if (currentChoice[0] > 0): #Go up the menu
                currentChoice[0] -= 1
            else:
                #Currently at the top of the menu
                currentChoice[0] = currentChoice[1] - 1
            handled = True
        elif (key == pygame.K_DOWN): #go down the menu
            currentChoice[0] += 1
            handled = True
        currentChoice[0] %= currentChoice[1] #make sure the selection doesnt do out side the length of the menu
        
        if (temp != currentChoice[0]): #selection changed
            i1 = temp - currentChoice[1] #index of the previous choice
            i2 = currentChoice[0] - currentChoice[1] #index of the current choice

            t = info.info.visibleText[i1].getText() #temp vairable
            info.info.visibleText[i1].setText(t[3:-3]) #remove >> << from the previous choice

            t = info.info.visibleText[i2].getText()
            t = ">> " + t + " <<"
            info.info.visibleText[i2].setText(t) #add >> << to the current choice

    if (not(handled)): #key press was not arrow up or down
        selected(key)
    
def generatePauseMenu(menuType, param=None): #param are special parameters
    #generates a menu of a type or clears menu text out of the text buffer
    global info
    global currentChoice
    global currentMenu

    text = info.info.visibleText
    if (menuType == -1):
        #clear menu text
        for i in range(currentChoice[2]):
            del text[-1]
        return
    elif (menuType == 0):
        #main menu
        currentChoice = [0, 3, 8]
        currentMenu = 0
        text.append(GameText.GameText("Game Designed by Sachin Samarasinghe", 10, None, (info.pfSize[0]*0.1, info.pfSize[1]*0.1), (113,230,100)))
        text.append(GameText.GameText("Use Up and Down Arrow Keys to Navigate", 10, None, (info.pfSize[0]*0.1, info.pfSize[1]*0.1+10), (201,120,207)))
        text.append(GameText.GameText("Through the Menu", 10, None, (info.pfSize[0]*0.1, info.pfSize[1]*0.1+20), (201,120,207)))
        text.append(GameText.GameText("Press Enter to Select an Option", 10, None, (info.pfSize[0]*0.1, info.pfSize[1]*0.1+30), (97,169,182)))
        text.append(GameText.GameText("Press Escape to Go Back", 10, None, (info.pfSize[0]*0.1, info.pfSize[1]*0.1+40), (113,230,100)))
        text.append(GameText.GameText(">> Start Game <<", 10, None, (info.pfSize[0]*0.4, info.pfSize[1]*0.4+10), menuColors[0]))
        text.append(GameText.GameText("How to Play", 10, None, (info.pfSize[0]*0.4, info.pfSize[1]*0.4+20), menuColors[1]))
        text.append(GameText.GameText("Quit", 10, None, (info.pfSize[0]*0.4, info.pfSize[1]*0.4+30), menuColors[1]))
    elif (menuType == 1):
        #pause menu
        currentChoice = [0, 0, 3]
        currentMenu = 1
        text.append(GameText.GameText("Paused", 10, None, (info.pfSize[0]*0.44, info.pfSize[1]*0.4), menuColors[0]))
        text.append(GameText.GameText("Press Escape to Resume", 10, None, (info.pfSize[0]*0.25, info.pfSize[1]*0.4+10), menuColors[1]))
        text.append(GameText.GameText("Press Q to Quit", 10, None, (info.pfSize[0]*0.35, info.pfSize[1]*0.4+20), menuColors[1]))
    elif (menuType == 2):
        #game over menu
        currentChoice = [0, 0, 3]
        currentMenu = 2
        text.append(GameText.GameText("Game Over", 10, None, (info.pfSize[0]*0.4, info.pfSize[1]*0.4), menuColors[0]))
        text.append(GameText.GameText("Your Score: " + str(param) , 10, None, (info.pfSize[0]*0.35, info.pfSize[1]*0.4+10), menuColors[1]))
        text.append(GameText.GameText("Press q to quit", 10, None, (info.pfSize[0]*0.357, info.pfSize[1]*0.4+20), menuColors[1]))
    elif (menuType == 3):
        #choose level
        currentChoice = [0, 3, 3]
        currentMenu = 3
        text.append(GameText.GameText(">> Level 1 (Asteroids only) <<", 10, None, (info.pfSize[0]*0.25, info.pfSize[1]*0.4), (255,0,0)))
        text.append(GameText.GameText("Level 2 (Asteroids and Enemies)", 10, None, (info.pfSize[0]*0.25, info.pfSize[1]*0.4+10), (255,0,0)))
        text.append(GameText.GameText("Level 3 (Enemies only)", 10, None, (info.pfSize[0]*0.25, info.pfSize[1]*0.4+20), (255,0,0)))
    elif (menuType == 4):
        #finished game menu
        currentChoice = [0, 0, 3]
        currentMenu = 4
        text.append(GameText.GameText("Congradulations!!! You Beat The final Level", 10, None, (info.pfSize[0]*0.05, info.pfSize[1]*0.4), menuColors[0]))
        text.append(GameText.GameText("Your Score: " + str(param) , 10, None, (info.pfSize[0]*0.35, info.pfSize[1]*0.4+10), menuColors[1]))
        text.append(GameText.GameText("Press q to quit", 10, None, (info.pfSize[0]*0.357, info.pfSize[1]*0.4+20), menuColors[1]))
    elif (menuType == 5):
        #help menu
        currentChoice = [0, 0, 5]
        currentMenu = 5
        text.append(GameText.GameText("Use A,D or Arrow Keys to move", 10, None, (info.pfSize[0]*0.05, info.pfSize[1]*0.4), menuColors[0]))
        text.append(GameText.GameText("Shoot at Asteroids and Enemies" , 10, None, (info.pfSize[0]*0.05, info.pfSize[1]*0.4+10), menuColors[1]))
        text.append(GameText.GameText("Avoid Getting Hit by Asteroids, Enemies or", 10, None, (info.pfSize[0]*0.05, info.pfSize[1]*0.4+20), (113,230,100)))
        text.append(GameText.GameText("Bullets Fired by Enemies", 10, None, (info.pfSize[0]*0.05, info.pfSize[1]*0.4+30), (113,230,100)))
        text.append(GameText.GameText("Press Escape to Pause", 10, None, (info.pfSize[0]*0.05, info.pfSize[1]*0.4+40), (97,169,182)))

        
    for i in range(-currentChoice[2], 0):
        #display text
        Transform.resizeText(info.info.size, info.pfSize, text[i])

def updateMenu():
    if (currentChoice[1] > 0):
        #more than one selectable choice
        for i in range(-currentChoice[1], 0):
            info.info.visibleText[i].setColor(menuColors[1])

        #change the color of the selected selection
        info.info.visibleText[currentChoice[0] - currentChoice[1]].setColor(menuColors[0])

def callPause(mode, additionalParameters=None):
    global pauseMode
    
    #pauses the game in a certain mode
    if (mode == 0): #main menu
        pauseMode = 0
        generatePauseMenu(0)
    elif (mode == 1): #paused during the game
        pauseMode = 1
        generatePauseMenu(1)
    elif (mode == 2): #game over menu
        pauseMode = 2
        generatePauseMenu(2, additionalParameters)
    elif (mode == 3): #game complete
        pauseMode = 3
        generatePauseMenu(4, additionalParameters)
        

def init(i):
    #initialization
    global loopInfo
    global info

    loopInfo = i
    info.info = i
    info.menuKeyHandle = menuKeyHandle
    info.music = music
    
    return updateMenu, callPause

def getKeyEvent():
    #return key handle function
    return info.keyEvent
