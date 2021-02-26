"""
Author: FurWaz
https://furwaz.github.io/

This module contains all the variable types used in the game
such as the Vec2, Color and Mouvement types
"""
from typing import Iterable
from engine.gamefuncs import clamp
try:
    import pygame
except ImportError:
    import os, sys
    if sys.platform == "linux": os.system("python3 -m pip install pygame")
    if sys.platform == "win32": os.system("python -m pip install pygame")
    if sys.platform == "darwin": os.system("python -m pip install pygame")
    import pygame

class Vec2:
    def __init__(self, x:int=0, y:int=0) -> None:
        self.x = x
        self.y = y

    def toTuple(self) -> Iterable[int]:
        return (int(self.x), int(self.y))

    def fromTuple(self, target:Iterable[int]) -> object:
        self.x = target[0]
        self.y = target[1]

    def invertX(self, target=None) -> object:
        if target == None: target = Vec2()
        return Vec2(target.x-self.x, self.y)

    def invertY(self, target=None) -> object:
        if target == None: target = Vec2()
        return Vec2(self.x, target.y-self.y)

    def toInt(self) -> object:
        return Vec2(int(self.x), int(self.y))

    def __eq__(self, o: object) -> bool:
        if o == None: return False
        return o.x == self.x and o.y == self.y

    def __neg__(self) -> object:
        return Vec2(-self.x, -self.y)

    def __add__(self, o: object) -> object:
        return Vec2(self.x+o.x, self.y+o.y)

    def __sub__(self, o: object) -> object:
        return Vec2(self.x-o.x, self.y-o.y)

    def __mul__(self, o: object) -> object:
        return Vec2(self.x*o, self.y*o)

    def __truediv__(self, o: object) -> object:
        return Vec2(self.x/o, self.y/o)

    def __lt__(self, o: object) -> object:
        return self.x < o.x and self.y < o.y

    def __gt__(self, o: object) -> object:
        return self.x > o.x and self.y > o.y

    def __str__(self) -> str:
        return "Vec2("+str(round(self.x, 2))+", "+str(round(self.y, 2))+")"

class Color:
    def __init__(self, r:int=0, g:int=0, b:int=0, a:int=255) -> None:
        self.r = clamp(r, 0, 255)
        self.g = clamp(g, 0, 255)
        self.b = clamp(b, 0, 255)
        self.a = clamp(a, 0, 255)

    def toTuple(self) -> Iterable[int]:
        return (self.r, self.g, self.b, self.a)

    def fromTuple(self, target:Iterable[int]) -> None:
        self.r = clamp(target[0], 0, 255)
        self.g = clamp(target[1], 0, 255)
        self.b = clamp(target[2], 0, 255)
        if len(target > 3): self.a = clamp(target[3], 0, 255)

    def toDict(self) -> dict:
        return {"r": self.r, "g": self.g, "b": self.b}

    def __str__(self) -> str:
        return "Color("+str(self.r)+", "+str(self.g)+", "+str(self.b)+", "+str(self.a)+")"

class Movement:
    def __init__(self) -> None:
        self.up = False
        self.down = False
        self.left = False
        self.right = False