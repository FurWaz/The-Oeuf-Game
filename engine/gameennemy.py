import math
from engine.gametypes import pygame, Vec2
from engine.gamegraphs import Image
from engine.gameplayer import Entity
from engine.gamescreen import Screen

class Ennemy(Entity):
    def __init__(self, pos:Vec2=Vec2()) -> None:
        super().__init__(pos)
        self.graph = Image(path="./resources/tomauvais.png")
        self.direction = Vec2(1, 0)
        self.speed = 2

    def update(self):
        # move the ennemy
        new_pos = self.pos + self.direction * Screen.dt * self.speed
        if Screen.scene.world == None: return
        if self.direction.x > 0: # right
            possibleMove = \
                Screen.scene.world.blockAt(new_pos+Vec2(1.05, 0.95)).transparent and \
                Screen.scene.world.blockAt(new_pos+Vec2(1.05, 0.05)).transparent and \
                (not Screen.scene.world.blockAt(self.pos+Vec2(0.95, 1.05)).transparent)
        else: # left
            possibleMove = \
                Screen.scene.world.blockAt(new_pos+Vec2(-0.05, 0.95)).transparent and \
                Screen.scene.world.blockAt(new_pos+Vec2(-0.05, 0.05)).transparent and \
                (not Screen.scene.world.blockAt(self.pos+Vec2(0.05, 1.05)).transparent)
        if possibleMove: self.pos = new_pos
        else: self.direction = self.direction.invertX()

        # apply graphical changes
        size = 5000/Screen.scene.world.camera.fov
        yshift = math.cos(self.pos.x*10) * 0.05
        self.graph.setPosTo((self.pos-Screen.scene.world.camera.pos+Vec2(0, yshift)) * size + Screen.dim/2)
        self.graph.setDimTo(Vec2(size, size))