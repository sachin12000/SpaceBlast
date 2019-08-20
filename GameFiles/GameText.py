import pygame as pg

#class for text that will displyed in game
class GameText:
    def __init__(self, text, size, fontName, position, color):
        self.text = text
        self.size = size
        self.name = fontName
        self.position = position
        self.color = color

        self.bold = False
        self.italic = False
        self.font = None

        self.textChanged = True
        self.surface = None
        
        pg.font.init()
        self.genFont() #Generate font
        self.genSurface() #Draw the surface

    #accessors
    def getText(self):
        return self.text
    def getSize(self):
        return self.size
        
    def getSurface(self):
        return self.surface

    def getFont(self):
        return self.font

    def getPosition(self):
        return self.position

    def textChanged(self):
        return self.textChanged

    #mutators
    def genFont(self): #Generates font
        self.font = pg.font.SysFont(self.name, self.size, self.bold, self.italic)

    def genSurface(self):
        #renders text on to surface and stores the surface
        #This way, the main loop wont have to render the text every frame
        self.surface = self.font.render(self.text, False, self.color)

    def setText(self, text):
        self.text = text
        self.genSurface() #Redraw the surface
        
    def setBold(self, bold):
        self.bold = setting
        self.genFont() #Regenerate font
        self.genSurface() #Redraw the surface

    def setItalic(self, italic):
        self.italic = italic
        self.genFont() #Regenerate font
        self.genSurface() #Redraw the surface

    def setSize(self, size):
        self.size = size
        self.genFont() #Regenerate font
        self.genSurface() #Redraw the surface

    def setColor(self, color):
        self.color = color
        self.genFont() #Regenerate font
        self.genSurface() #Redraw the surface

    def setColorRGB(self, r, g, b):
        self.setColor((r,g,b))

    def setSurface(self, s):
        self.surface = s
