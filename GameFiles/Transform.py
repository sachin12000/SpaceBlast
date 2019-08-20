import pygame as pg

coor = [] #Screen size, Surface

def setSize(Screen, Surface):
    coor.append(Screen)
    #screenSize = Screen
    
    coor.append(Surface)
    #screenSize = Surface

def transformAndRender(surface, screenSize, surfaceSize, clear, backColor, polygons):
    xF = screenSize[0] / float(surfaceSize[0])
    yF = screenSize[1] / float(surfaceSize[1])

    if (clear):
        surface.fill(backColor)
        
    for i in range(len(polygons)):
        rdr = polygons[i].getRenderBundle() #info needed for rendering
        points = [] #Tranformed points
        
        for pt in rdr[1]: #Transform each point
            x = (pt[0]  + rdr[0][0]) * xF
            y = (pt[1]  + rdr[0][1]) * yF
            points.append((x,y))
        #pg.draw.aalines(surface,rdr[2], True, points, rdr[3]) #Draw polygon
        if (polygons[i].isAAed()):
            pg.draw.aalines(surface,rdr[2], True, points, 0) #anti aliased polygon
        else:
            pg.draw.polygon(surface,rdr[2], points, rdr[3]) #non anti aliased polygon
        

def tranformTextRender(surface, origin, screenSize, surfaceSize, clear, backColor, text):
    xF = screenSize[0] / float(surfaceSize[0])
    yF = screenSize[1] / float(surfaceSize[1])
    
    if (clear):
        surface.fill(backColor)

    for t in text:
        position = t.getPosition()
        x = position[0] * xF
        y = position[1] * yF
        
        surface.blit(t.getSurface(), [x,y]) #blit the surface to display

def drawCircle(surface, screenSize, surfaceSize, clear, backColor, circles):
    xF = screenSize[0] / float(surfaceSize[0])
    yF = screenSize[1] / float(surfaceSize[1])
    for c in circles:
        b = c.getRenderBundle()
        x = int(b[0][0] * xF)
        y = int(b[0][1] * yF)
        pg.draw.circle(surface, b[2], (x,y), int(b[1] * xF), b[3]) #surface, color, position, radius, width


def resizeText(screenSize, surfaceSize, text):
    yF = screenSize[1] / float(surfaceSize[1])
    text.setSize(int(text.getSize() * yF))
    
#def renderSurface(originalSurface, size, surface, origin,
def drawS(source, dest, screenSize, surfaceSize): #DrawableSurface as an input
    xF = screenSize[0] / float(surfaceSize[0])
    yF = screenSize[1] / float(surfaceSize[1])
    
    for s in source:
        dest.blit(s[0], (s[1][0] * xF, s[1][1] * yF))

def transformCoordinate(screenSize, surfaceSize, coordinate):
    xF = screenSize[0] / float(surfaceSize[0])
    yF = screenSize[1] / float(surfaceSize[1])

    return (coordinate[0] * xF, coordinate[1] * yF)
