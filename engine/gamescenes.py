"""
Author: FurWaz
https://furwaz.github.io/

This module contains the Scene object as well as the createScene function
used to create all the scenes of the game.
"""
from engine.gameennemy import Ennemy
from engine.gamescreen import Screen
from engine.gamegraphs import *
from engine.gameplayer import Player, DemoPlayer
from engine.gameworlds import *
from engine.gamehuds import *
from engine.gameconst import *
import pygame, math
pygame.init()

MENU_SCENE = 0
GAME_SCENE = 1
OPTION_SCENE = 2
DEMO_SCENE = 3
SELECTION_SCENE = 4
ENDING_SCENE = 5

class Scene:
    def __init__(self, code:int=MENU_SCENE, world:World=None, hud:Hud=None, player:Player=None, color:Color=Constants.COLOR_SKY) -> None:
        self.code = code
        self.world = world
        self.hud = hud
        self.player = player
        self.askForQuit = False
        self.askForChangeRes = False
        self.askForFullscreen = False
        self.clearColor = color

        #place the player at the start
        if type(self.player) == Player and self.world != None:
            self.player.setPosTo(self.world.startPos())
        #place the ennemys
        if self.world != None:
            positions = self.world.ennemysPos()
            for pos in positions:
                self.world.entities.append(Ennemy(pos))

    def processEvents(self, events:Iterable[pygame.event.Event]) -> Iterable[pygame.event.Event]:
        evts = []
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                mousePos = Vec2()
                mousePos.fromTuple(pygame.mouse.get_pos())
                for o in self.hud.objects:
                    if isinstance(o, ClickElement):
                        o.click(mousePos)
            elif e.type == pygame.KEYDOWN:
                if type(self.player) == Player:
                    if e.key == pygame.K_z or e.key == pygame.K_w or e.key == pygame.K_SPACE or e.key == pygame.K_UP:
                        self.player.moveUp()
                    elif e.key == pygame.K_s or e.key == pygame.K_DOWN:
                        self.player.moveDown()
                    elif e.key == pygame.K_d or e.key == pygame.K_RIGHT:
                        self.player.moveRight()
                    elif e.key == pygame.K_q or e.key == pygame.K_a or e.key == pygame.K_LEFT:
                        self.player.moveLeft()
                if e.key == pygame.K_r: self.reloadScene()
                if e.key == pygame.K_ESCAPE: Screen.scene = createScene(MENU_SCENE)
            elif e.type == pygame.KEYUP:
                if type(self.player) == Player:
                    if e.key == pygame.K_z or e.key == pygame.K_w or e.key == pygame.K_SPACE or e.key == pygame.K_UP:
                        self.player.stopMoveUp()
                    elif e.key == pygame.K_s or e.key == pygame.K_DOWN:
                        self.player.stopMoveDown()
                    elif e.key == pygame.K_d or e.key == pygame.K_RIGHT:
                        self.player.stopMoveRight()
                    elif e.key == pygame.K_q or e.key == pygame.K_a or e.key == pygame.K_LEFT:
                        self.player.stopMoveLeft()
            else: evts.append(e)
        return evts

    def update(self) -> None:
        if self.world != None: self.world.camera.setTarget(self.player.pos); self.world.camera.update()
        if self.player != None: self.player.update()
        if self.world != None: self.world.update()
        mousePos = Vec2()
        mousePos.fromTuple(pygame.mouse.get_pos())
        for e in self.hud.objects: e.update(mousePos)
    
    def reloadScene(self) -> None:
        if self.code != GAME_SCENE: Screen.scene = createScene(self.code)
        else: loadLevel()

    def setSelectionScene(self) -> None:
        loadScene(SELECTION_SCENE)

    def loadNextLevel(self) -> None:
        Sounds.yes.play()
        Constants.LEVEL_NUMBER+=1
        loadLevel()

def askForQuit():
    Screen.scene.askForQuit = True
def changeRes():
    Screen.scene.askForChangeRes = True
def toogleFullScreen():
    Screen.scene.askForFullscreen = True

def createScene(sceneCode:int=MENU_SCENE):
    if sceneCode == MENU_SCENE:
        return Scene(sceneCode, None, Hud([
            Text(Vec2(Screen.dim.x/2, 100), "The Oeuf Game", 60, Constants.COLOR_WHITE, FONT_BIG),
            Button(Screen.dim/2+Vec2(0, 0), Vec2(100, 40), loadScene, SELECTION_SCENE, Constants.COLOR_BLACK, Constants.COLOR_GREY,
                Text(Vec2(), "Play", 26, Constants.COLOR_WHITE, FONT_MEDIUM)
            ),
            Button(Screen.dim/2+Vec2(0, 50), Vec2(140, 40), loadScene, DEMO_SCENE, Constants.COLOR_BLACK, Constants.COLOR_GREY,
                Text(Vec2(), "Tutorial", 26, Constants.COLOR_WHITE, FONT_MEDIUM)
            ),
            Button(Screen.dim/2+Vec2(-55, 100), Vec2(100, 40), loadScene, OPTION_SCENE, Constants.COLOR_BLACK, Constants.COLOR_GREY,
                Text(Vec2(), "Settings", 26, Constants.COLOR_WHITE, FONT_MEDIUM)
            ),
            Button(Screen.dim/2+Vec2(55, 100), Vec2(100, 40), askForQuit, None, Constants.COLOR_BLACK, Constants.COLOR_GREY,
                Text(Vec2(), "Quit", 26, Constants.COLOR_WHITE, FONT_MEDIUM)
            ),
            Image(Vec2(Screen.dim.x*0.8, Screen.dim.y/2+50), Vec2(Screen.dim.y-200, Screen.dim.y-200), "resources/oeuf.png")
        ]), None, Constants.COLOR_SKY)

    if sceneCode == GAME_SCENE:
        try:
            return  Scene(sceneCode, World(
                    loadWorldFromSave("./resources/levels/"+str(Constants.LEVEL_NUMBER)+".world")
                ), Hud(), Player(), Constants.COLOR_SKY)
        except: # ending
            Sounds.tulututu.play()
            return Scene(sceneCode, None, Hud([
                Text(Screen.dim/2, "The End", 80, Constants.COLOR_WHITE),
                Button(
                    Vec2(Screen.dim.x/2, Screen.dim.y-100), Vec2(80, 80), loadScene, MENU_SCENE,
                    Constants.COLOR_WHITE, Constants.COLOR_GREY, Text(Vec2(), "Ok", 40, Constants.COLOR_BLACK)
                )
            ]), None, Constants.COLOR_BLACK)

    if sceneCode == DEMO_SCENE:
        return Scene(
            sceneCode, World(loadWorldFromSave("./resources/demolevel.world")),
            Hud(), DemoPlayer(Vec2(15, 0)), Constants.COLOR_SKY
        )

    if sceneCode == SELECTION_SCENE:
        amount = 0
        done = False
        while not done:
            try: open('./resources/levels/'+str(amount+1)+'.world'); amount+=1
            except: done = True
        objects = [
            Button(Vec2(85, 35), Vec2(80, 30), loadScene, MENU_SCENE, Constants.COLOR_BLACK, Constants.COLOR_GREY,
                Text(Vec2(), "Back", 24, Constants.COLOR_WHITE, FONT_MEDIUM)
            )
        ]
        BUTTON_SIZE=Vec2(120, 30)
        BUTTON_SPACE=10
        x = Screen.dim.x/2 - ((math.ceil(amount/2)+1) * (BUTTON_SIZE.x+BUTTON_SPACE))/2
        for i in range(amount):
            if (i+1) < Constants.LEVEL_NUMBER: button_color = Constants.COLOR_GRASS
            else: button_color = Constants.COLOR_BLACK
            y = 0
            if i%2 == 0: x += BUTTON_SIZE.x+BUTTON_SPACE; y = (Screen.dim.y-BUTTON_SIZE.y-BUTTON_SPACE)/2
            else: y = (Screen.dim.y+BUTTON_SIZE.y+BUTTON_SPACE)/2
            objects.append(
                Button(Vec2(x, y), BUTTON_SIZE, loadLevel, (i+1), button_color, Constants.COLOR_GREY,
                    Text(Vec2(), "Level "+str(i+1), 24, Constants.COLOR_WHITE, FONT_MEDIUM)
                )
            )
        return  Scene(sceneCode, None, Hud(objects), None, Constants.COLOR_SKY)

    if sceneCode == OPTION_SCENE:
        return  Scene(sceneCode, None, Hud([
            Text(Vec2(Screen.dim.x/2, 32), "Settings", 30, Constants.COLOR_WHITE, FONT_BIG),
            Button(Vec2(85, 35), Vec2(80, 30), loadScene, MENU_SCENE, Constants.COLOR_BLACK, Constants.COLOR_GREY,
                Text(Vec2(), "Back", 24, Constants.COLOR_WHITE, FONT_MEDIUM)
            ),
            Button(Screen.dim/2+Vec2(0, -100), Vec2(260, 30), changeRes, None, Constants.COLOR_BLACK, Constants.COLOR_GREY,
                Text(Vec2(), "Change resolution", 26, Constants.COLOR_WHITE, FONT_MEDIUM)
            ),
            Button(Screen.dim/2+Vec2(0, -50), Vec2(160, 30), toogleFullScreen, None, Constants.COLOR_BLACK, Constants.COLOR_GREY,
                Text(Vec2(), "Fullscreen", 26, Constants.COLOR_WHITE, FONT_MEDIUM)
            )
        ]), None, Constants.COLOR_SKY)

def loadScene(argument:int=MENU_SCENE):
    Screen.scene.hud.objects.clear()
    Screen.scene = createScene(argument)

def loadLevel(number=0):
    if number > 0: Constants.LEVEL_NUMBER = number
    Screen.scene = createScene(GAME_SCENE)