"""
Author: FurWaz
https://furwaz.github.io/

This module contains the Camera, World and WorldElement objects
used to describe and interact with a world
"""

from engine.gameconst import *
from engine.gametypes import Vec2
from engine.gamescreen import Screen
from engine.gamegraphs import *
from typing import Iterable
from random import randint as rd

def getGraphFromCode(code:int=Constants.WORLD_AIR) -> GraphElement:
    if code==Constants.WORLD_GRASS: return Image(path="./resources/grass.png")
    elif code==Constants.WORLD_DIRT: return Image(path="./resources/dirt.png")
    elif code==Constants.WORLD_STONE: return Image(path="./resources/stone.png")
    elif code==Constants.WORLD_END: return Image(path="./resources/end.png")
    else: return Rect(color=Constants.COLOR_TRANSPARENT)

class Camera:
    def __init__(self, pos:Vec2=Vec2(), target:Vec2=Vec2(), fov:int=100) -> None:
        self.target = target
        self.pos = pos
        self.fov = fov

    def update(self) -> None:
        self.pos = self.pos + (self.target-self.pos) * Screen.dt * 3

    def setTarget(self, target:Vec2=Vec2()) -> None:
        self.target = target

class WorldElement:
    def __init__(self, pos:Vec2=Vec2(), code:int=Constants.WORLD_AIR) -> None:
        self.pos = pos
        self.code = int(code)
        self.transparent = (
            self.code == Constants.WORLD_AIR or self.code == Constants.WORLD_START or
            self.code == Constants.WORLD_END or self.code == Constants.WORLD_ENNEMY
        )
        self.graph = getGraphFromCode(self.code)

    def update(self):
        if Screen.scene.world == None: return
        size = 5000/Screen.scene.world.camera.fov
        self.graph.setPosTo((self.pos-Screen.scene.world.camera.pos) * size + Screen.dim/2)
        self.graph.setDimTo(Vec2(size, size))

    def __str__(self) -> str:
        return "WorldElement("+str(self.pos.x)+", "+str(self.pos.y)+", "+str(self.code)+")"

class World:
    def __init__(self, objects:Iterable[Iterable[WorldElement]]=[]) -> None:
        self.objects = objects
        self.camera = Camera()
        self.data = pygame.Surface(Screen.dim.toTuple())
        self.entities = []

    def update(self) -> None:
        for e in self.entities: e.update()
        for e in self.objects:
            for i in e:
                i.update()
        self.data.fill(Screen.scene.clearColor.toTuple())
        for le in self.objects:
            for el in le:
                self.data.blit(el.graph.data, (el.graph.pos-el.graph.dim/2).toTuple())
        for e in self.entities:
            self.data.blit(e.graph.data, (e.graph.pos-e.graph.dim/2).toTuple())

    def blockAt(self, pos:Vec2=Vec2()) -> WorldElement:
        default = WorldElement(Vec2(), Constants.WORLD_AIR)
        try:
            if pos.y < 0 or pos.y >= len(self.objects): return default
            if pos.x < 0 or pos.x >= len(self.objects[0]): return default
            return self.objects[int(pos.y)][int(pos.x)]
        except: return default

    def groundLevelAt(self, pos:Vec2=Vec2()) -> int:
        pos = Vec2(pos.x+0.5, pos.y)
        isEnd = pos.x < 0 or pos.x >= len(self.objects[0])
        isEnd = isEnd or pos.y < 0 or pos.y >= len(self.objects)
        index = round(pos.y)
        while not isEnd:
            if index >= len(self.objects): isEnd = True
            else:
                block = self.objects[index][int(pos.x)]
                if not block.transparent: return index-1
                index += 1
        return len(self.objects)

    def startPos(self) -> Vec2:
        y = 0
        for e in self.objects:
            x = 0
            for o in e:
                if o.code == Constants.WORLD_START: return Vec2(x, y)
                x+=1
            y+=1
        return Vec2()

    def ennemysPos(self) -> Iterable[Vec2]:
        result = []
        y_pos = 0
        for y in self.objects:
            x_pos = 0
            for x in y:
                if x.code == Constants.WORLD_ENNEMY:
                    result.append(Vec2(x_pos, y_pos))
                x_pos+=1
            y_pos+=1
        return result

    def killEnnemyAt(self, pos:Vec2=Vec2()) -> bool:
        """
        try to kill the ennemy under the given position, and return is the player
        is killed by the ennemy or not
        """
        isKilled = False
        try:
            if pos.y < 0 or pos.y >= len(self.objects): return False
            if pos.x < 0 or pos.x >= len(self.objects[0]): return False
            for e in self.entities:
                cur_pos = e.pos
                if cur_pos > pos+Vec2(-1, -1.2) and cur_pos < pos+Vec2(0, 0.1):
                    isKilled = True
                if cur_pos > pos+Vec2(-1, 0.1) and cur_pos < pos+Vec2(0, 0.5):
                    self.entities.remove(e)
                    Screen.scene.player.ymove = -Constants.JUMP_FORCE*0.7
            return isKilled
        except: return False

def loadWorldFromSave(path:str=None) -> Iterable[WorldElement]:
    if path == None: return []
    data = open(path).read()
    layers = data.split("\n")
    world = []
    for l in range(0, len(layers)):
        line = []
        blocks = layers[l]
        for b in range(0, len(blocks)):
            nbr = blocks[b]
            try: int(nbr)
            except: nbr = 0
            line.append(WorldElement(Vec2(b, l), nbr))
        world.append(line)
    return world