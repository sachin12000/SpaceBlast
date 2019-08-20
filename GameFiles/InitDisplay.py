#initializes display using given parameters
import FindFPS
import pygame as pg

def initDisplay(aspectRatio, heightFactor, gameTitle, fps):
    info = pg.display.Info()

    h = int(info.current_h * heightFactor) #Percentage of the screen to use
    w = int((float(h) / aspectRatio[1]) * aspectRatio[0])
    size =  (w,h)

    d = pg.display.set_mode(size) #Create surface
    pg.display.set_caption(gameTitle) #Set title
    clk = pg.time.Clock() #Timer
    T = FindFPS.Find(clk, fps) #Time per frame

    return d, size, clk, T
