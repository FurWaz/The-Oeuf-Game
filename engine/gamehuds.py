"""
Author: FurWaz
https://furwaz.github.io/

This module contains the hud object,
used to store all the graphical elements
of a scene.
"""
from typing import Iterable
from engine.gamegraphs import GraphElement

class Hud:
    def __init__(self, objects:Iterable[GraphElement]=[]) -> None:
        self.objects = objects

# START MENU HUD
MENU_HUD = Hud()
# END MENU HUD