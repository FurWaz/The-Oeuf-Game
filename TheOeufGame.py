"""
The Oeuf Game - Main file
Author: FurWaz

This file contains the game's main loop.
"""

from engine.gamescreen import *
from engine.gameconst import *
from engine.gamegraphs import *
from engine.gamescenes import *
from engine.gamesounds import Sounds

Constants.loadSettings()
Sounds.init()

screen = Screen(Vec2(0, 0), Constants.RESOLUTION, "The Oeuf Game", Rect(), 60, Constants.FULLSCREEN)
oeuf = Image(Vec2(0, 0), Vec2(100, 100), "./resources/oeuf.png")
screen.setIcon(oeuf)

screen.sceneCode = MENU_SCENE
Screen.scene = createScene(Screen.sceneCode)

while screen.isOpen:
    events = screen.getEvents()
    Screen.scene.processEvents(events)

    if screen.isOpen: Screen.scene.update()

    screen.clear(Screen.scene.clearColor)
    screen.drawScene(Screen.scene)
    screen.update()

Constants.saveSettings()
pygame.quit()