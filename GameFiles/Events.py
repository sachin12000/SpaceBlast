Events = []
T = [] #Time per frame (in milliseconds)

def init(time):
    T.append(float(time))

def insertEvent(time, ticks, functions, args):
    t = int(time / T[0]) + ticks - 1 #amount of frames for the delay

    index = 0
    while (index < len(Events)):
        if (t < Events[index][0]): #Event comes before
            Events.insert(index, [t, functions, args])
            return
        elif (t == [index][0]): #Event is runs at same time
            Events[index][1] += functions
            Events[index][2] += args
            return
        index += 1

    Events.append([t, functions, args])

def checkForEvents(ticks):
    if (len(Events) == 0):
        return False
    
    if (ticks > Events[0][0]):
        return True

    return False


def clearEvents(): #clears all timed events
    del Events[:]
