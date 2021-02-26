"""
Author: FurWaz
https://furwaz.github.io/

This module contains all the graphical elements such as
images, text, buttons, ...
"""

from engine.gameconst import *
from engine.gametypes import *
from engine.gamesounds import Sounds

FONT_BIG = "./resources/Roboto-Bold.ttf"
FONT_MEDIUM = "./resources/Roboto-Medium.ttf"
FONT_SMALL = "./resources/Roboto-Thin.ttf"

def EMPTY_FUNCTION(): pass

class GraphElement:
    def __init__(self, pos:Vec2=Vec2(), dim:Vec2=Vec2()) -> None:
        self.pos = pos
        self.dim = dim
        self.data = pygame.Surface(dim.toTuple())
    
    def changePosBy(self, delta:Vec2=Vec2()) -> None:
        self.pos = Vec2(self.pos.x+delta.x, self.pos.y+delta.y)
    
    def setPosTo(self, pos:Vec2=Vec2()) -> None:
        self.pos = pos

    def changeDimBy(self, delta:Vec2=Vec2()) -> None:
        self.dim = Vec2(self.dim.x+delta.x, self.dim.y+delta.y)
    
    def setDimTo(self, dim:Vec2=Vec2()) -> None:
        self.dim = dim
        self.data = pygame.Surface(dim.toTuple())

    def update(self, mousePos:Vec2=Vec2()) -> None:
        pass

class ClickElement(GraphElement):
    def __init__(self, pos: Vec2, dim: Vec2, callback=EMPTY_FUNCTION, argument=None) -> None:
        super().__init__(pos, dim)
        self.callback = callback
        self.argument = argument

    def click(self, mousePos:Vec2=Vec2()) -> bool:
        if mousePos > self.pos-self.dim/2 and mousePos < self.pos+self.dim/2:
            Sounds.clic.play()
            if self.argument == None: self.callback()
            else: self.callback(self.argument)
            return True
        return False

class Rect(GraphElement):
    def __init__(self, pos:Vec2=Vec2(), dim:Vec2=Vec2(), color:Color=Constants.COLOR_WHITE) -> None:
        super().__init__(pos, dim)
        self.color = color
        self.data.fill(self.color.toTuple())

    def changeDimBy(self, delta:Vec2=Vec2()) -> None:
        self.dim = Vec2(self.dim.x+delta.x, self.dim.y+delta.y)
        self.data = pygame.Surface(self.dim.toTuple())
        self.data.fill(self.color.toTuple())
    
    def setDimTo(self, dim:Vec2=Vec2()) -> None:
        self.dim = dim
        self.data = pygame.Surface(self.dim.toTuple())
        self.data.fill(self.color.toTuple())

class Image(GraphElement):
    def __init__(self, pos:Vec2=Vec2(), dim:Vec2=Vec2(), path=""):
        super().__init__(pos, dim)
        self.path = path
        if path != "": self.data = pygame.image.load(path).convert_alpha()
        self.source = self.data
        self.setDimTo(self.dim)
    
    def setPathTo(self, path:str="") -> None:
        self.path = path
        self.data = pygame.Surface(self.dim.toTuple())
        if path != "": self.data = pygame.image.load(path).convert_alpha()
        self.source = self.data
    
    def changeDimBy(self, delta:Vec2=Vec2()) -> None:
        super().changeDimBy(delta)
        self.data = pygame.transform.scale(self.source, self.dim.toTuple())
    
    def setDimTo(self, dim:Vec2=Vec2()) -> None:
        super().setDimTo(dim)
        self.data = pygame.transform.scale(self.source, self.dim.toTuple())

class Text(GraphElement):
    def __init__(self, pos:Vec2=Vec2(), text:str="Text", size:int=30, color:Color=Constants.COLOR_WHITE, fontCode=FONT_MEDIUM) -> None:
        self.text = text
        self.size = size
        self.color = color
        self.fontCode = fontCode
        super().__init__(pos, Vec2())
        self.generateFont()

    def generateFont(self) -> None:
        self.font = pygame.font.Font(self.fontCode, self.size)
        self.dim.fromTuple(self.font.size(self.text))
        self.data = self.font.render(self.text, True, self.color.toTuple())

    def setSizeTo(self, size:int=30) -> None:
        self.size = size
        self.generateFont()

    def changeSizeBy(self, delta:int=0) -> None:
        self.size += delta
        self.generateFont()

    def setColorTo(self, color:Color=Constants.COLOR_WHITE) -> None:
        self.color = color
        self.data = self.font.render(self.text, True, self.color.toTuple())
    
    def setTextTo(self, text:str="Text") -> None:
        self.text = text
        self.data = self.font.render(self.text, True, self.color.toTuple())
    
    def setFontTo(self, fontCode:int=FONT_MEDIUM) -> None:
        self.fontCode = fontCode
        self.generateFont()

class Button(ClickElement):
    def __init__(self, pos: Vec2, dim: Vec2, callback=EMPTY_FUNCTION, argument=None, color:Color=Constants.COLOR_BLACK, hover:Color=Constants.COLOR_BLACK, text:Text=None) -> None:
        super().__init__(pos, dim, callback, argument)
        self.text = text
        self.color = color
        self.hover = hover
        self.data = pygame.Surface(self.dim.toTuple())
        self.data.fill(color.toTuple())
        if self.text != None: self.data.blit(text.data, (self.dim/2-self.text.dim/2).toTuple())

    def update(self, mousePos:Vec2=Vec2()) -> None:
        if mousePos > self.pos-self.dim/2 and mousePos < self.pos+self.dim/2:
            self.data.fill(self.hover.toTuple())
        else:
            self.data.fill(self.color.toTuple())
        if self.text != None: self.data.blit(self.text.data, (self.dim/2-self.text.dim/2).toTuple())