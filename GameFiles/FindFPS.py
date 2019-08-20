#Calculates the delay required for specified fps
from pygame import *

def Find(clk, fps):
    fps = float(fps)
    T = 1000 / fps
    br = 0 #Counter
    
    while (br < 20):
        c = 0
        while (c < 10):
            clk.tick()
            c += 1
            time.delay(int(T - clk.tick()))

        fps1 = clk.get_fps()
        if (abs(fps1 - fps) < 2):  #Timing is correct (almost; good enough)
            return int(T/2.0) #Pygame timing is not ver accurate

        T *= fps1 / fps #recalculate fps
        br += 1

    return int(1000/fps) #Appropiate timing not found
