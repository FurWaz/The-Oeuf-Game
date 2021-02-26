"""
Author: FurWaz
https://furwaz.github.io/

This module contains the main player object, and 
the special DemoPlayer object used to trigger the animations
in the tutorial.
"""
import math
from engine.gameworlds import *
from engine.gamegraphs import *
from engine.gameconst import *
from engine.gamefuncs import *
from engine.gametypes import *
from engine.gamescreen import Screen
from engine.gamesounds import Sounds

degToRad = math.pi/360

class Entity:
    def __init__(self, pos:Vec2=Vec2()) -> None:
        self.pos = pos
        self.graph = Rect(color=Constants.COLOR_TRANSPARENT)

    def update(self) -> None:
        pass

    def mapPosition(self) -> Vec2:
        return self.pos.toInt()

class Player(Entity):
    def __init__(self, pos:Vec2=Vec2()) -> None:
        super().__init__(pos)
        self.source = Image(path="resources/oeuf.png")
        self.rotation = 0
        self.rotationRatio = 1
        self.graph = Image(path="resources/oeuf.png")
        self.world:World = None
        self.moverequest = Movement()
        self.targetSpeed = 6
        self.speed = 0
        self.ymove = 0.1
        self.grounded = True

    def setWorld(self, world:World) -> None:
        self.world = world

    def changePosBy(self, delta:Vec2=Vec2()):
        self.pos = self.pos+delta

    def setPosTo(self, pos:Vec2=Vec2()):
        self.pos = pos

    def update(self) -> None:
        deltaPos = Vec2()
        if self.moverequest.right: self.targetSpeed = 6
        elif self.moverequest.left: self.targetSpeed = -6
        else: self.targetSpeed = 0
        self.speed += (self.targetSpeed-self.speed) * Screen.dt * 4
        deltaPos.x += Screen.dt * self.speed

        if not self.grounded: self.ymove += Constants.GRAVITY * Screen.dt
        deltaPos.y = self.ymove
        #if self.moverequest.up: deltaPos.y += 0.1
        #if self.moverequest.down: deltaPos.y -= 0.1
        
        #collision
        possibleMoves = Movement()
        possibleMoves.right = \
            Screen.scene.world.blockAt(self.pos+Vec2(1.05, 0.95)).transparent and \
            Screen.scene.world.blockAt(self.pos+Vec2(1.05, 0.05)).transparent
        possibleMoves.left = \
            Screen.scene.world.blockAt(self.pos+Vec2(-0.05, 0.95)).transparent and \
            Screen.scene.world.blockAt(self.pos+Vec2(-0.05, 0.05)).transparent
        possibleMoves.up = \
            Screen.scene.world.blockAt(self.pos+Vec2(0.05, -0.05)).transparent and \
            Screen.scene.world.blockAt(self.pos+Vec2(0.95, -0.05)).transparent
        possibleMoves.down = \
            Screen.scene.world.blockAt(self.pos+Vec2(0.05, 1.05)).transparent and \
            Screen.scene.world.blockAt(self.pos+Vec2(0.95, 1.05)).transparent

        if not self.grounded and not possibleMoves.down:
            self.grounded = True
            self.ymove = 0 
        if not self.grounded and not possibleMoves.up:
            self.ymove = 0

        #movements
        if not possibleMoves.up and deltaPos.y < 0: deltaPos.y = 0
        if not possibleMoves.down and deltaPos.y > 0: deltaPos.y = 0
        if not possibleMoves.right and deltaPos.x > 0: deltaPos.x = 0; self.speed = 0
        if not possibleMoves.left and deltaPos.x < 0: deltaPos.x = 0; self.speed = 0
        if possibleMoves.down: self.grounded = False
        if self.grounded and self.moverequest.up:
            Sounds.boing.play()
            self.ymove = -Constants.JUMP_FORCE
            self.grounded = False
        self.pos = self.pos+deltaPos
        if self.grounded: self.rotationRatio = 1
        else: self.rotationRatio *= 0.94
        self.rotation -= deltaPos.x*360*self.rotationRatio/math.pi

        #avoid sinking in ground
        self.pos.y = min(self.pos.y, Screen.scene.world.groundLevelAt(self.pos))

        # apply graphical changes
        size = 5000/Screen.scene.world.camera.fov
        self.graph.setPosTo((self.pos-Screen.scene.world.camera.pos) * size + Screen.dim/2)
        self.graph.setDimTo(Vec2(size, size))
        self.graph.data = pygame.transform.rotate(self.graph.data, self.rotation)
        isKilled = Screen.scene.world.killEnnemyAt(self.pos+Vec2(0.5, 0.5))
        
        if isKilled:
            Sounds.aie.play()
            Screen.scene.reloadScene()
        if self.pos.y >= len(Screen.scene.world.objects):
            Sounds.aie.play()
            Screen.scene.reloadScene()
        if Screen.scene.world.blockAt(self.pos+Vec2(0.5, 0.5)).code == Constants.WORLD_END:
            Screen.scene.loadNextLevel()

    def moveUp(self):
        self.moverequest.up = True
    def moveDown(self):
        self.moverequest.down = True
    def moveLeft(self):
        self.moverequest.left = True
    def moveRight(self):
        self.moverequest.right = True
    def stopMoveUp(self):
        self.moverequest.up = False
    def stopMoveDown(self):
        self.moverequest.down = False
    def stopMoveRight(self):
        self.moverequest.right = False
    def stopMoveLeft(self):
        self.moverequest.left = False

class DemoPlayer(Entity):
    def __init__(self, pos:Vec2=Vec2()) -> None:
        super().__init__(pos)
        self.time = 0
        self.events = [
            {"time": 3, "callback": self.spawnFemboy},
            {"time": 4, "callback": self.turnOeufRight},
            {"time": 4.5, "callback": self.turnOeufLeft},
            {"time": 4.5, "callback": self.turnOeufLeft},
            {"time": 5, "callback": self.turnOeufRight},
            {"time": 5, "callback": self.turnOeufRight},
            {"time": 5.5, "callback": self.turnOeufLeft},
            {"time": 5.5, "callback": self.turnOeufLeft},
            {"time": 6, "callback": self.turnOeufRight},
            {"time": 6, "callback": self.turnOeufRight},
            {"time": 6.5, "callback": self.turnOeufLeft},
            {"time": 6.5, "callback": self.turnOeufLeft},
            {"time": 7, "callback": self.turnOeufRight},
            {"time": 7, "callback": self.turnOeufRight},
            {"time": 10, "callback": self.spawnTomauvais},
            {"time": 10.1, "callback": self.moveTomauvaisLeft},
            {"time": 10.2, "callback": self.moveTomauvaisLeft},
            {"time": 10.3, "callback": self.moveTomauvaisLeft},
            {"time": 10.4, "callback": self.moveTomauvaisLeft},
            {"time": 10.5, "callback": self.moveTomauvaisLeft},
            {"time": 10.6, "callback": self.moveTomauvaisLeft},
            {"time": 10.7, "callback": self.moveTomauvaisLeft},
            {"time": 10.8, "callback": self.moveTomauvaisLeft},
            {"time": 11.1, "callback": self.moveTomauvaisRight},
            {"time": 11.1, "callback": self.moveFemboyRight},
            {"time": 11.2, "callback": self.moveTomauvaisRight},
            {"time": 11.2, "callback": self.moveFemboyRight},
            {"time": 11.3, "callback": self.moveTomauvaisRight},
            {"time": 11.3, "callback": self.moveFemboyRight},
            {"time": 11.4, "callback": self.moveTomauvaisRight},
            {"time": 11.4, "callback": self.moveFemboyRight},
            {"time": 11.5, "callback": self.moveTomauvaisRight},
            {"time": 11.5, "callback": self.moveFemboyRight},
            {"time": 11.6, "callback": self.moveTomauvaisRight},
            {"time": 11.6, "callback": self.moveFemboyRight},
            {"time": 11.7, "callback": self.moveTomauvaisRight},
            {"time": 11.7, "callback": self.moveFemboyRight},
            {"time": 11.8, "callback": self.moveTomauvaisRight},
            {"time": 11.8, "callback": self.moveFemboyRight},
            {"time": 12, "callback": self.moveTomauvaisRight},
            {"time": 12, "callback": self.moveFemboyRight},
            {"time": 12.2, "callback": self.moveTomauvaisRight},
            {"time": 12.2, "callback": self.moveFemboyRight},
            {"time": 13, "callback": self.makeOeufSad},
            {"time": 14, "callback": self.zoomOnScene},
            {"time": 15, "callback": self.showControls},
            {"time": 16, "callback": self.spawnBackButton}
        ]

    def update(self) -> None:
        self.time += Screen.dt
        if len(self.events) < 1: return
        if self.time > self.events[0]["time"]:
            self.events[0]["callback"]()
            self.events.pop(0)

    def spawnFemboy(self) -> None:
        Screen.scene.hud.objects.append(Image(Screen.dim/2-Vec2(50, 0), Vec2(100, 100), "./resources/oeuf.png"))
        Screen.scene.hud.objects.append(Image(Screen.dim/2, Vec2(150, 150), "./resources/oeuf_UwU.png"))
        Screen.scene.hud.objects[0].source = Screen.scene.hud.objects[0].data

    def turnOeufLeft(self) -> None:
        Screen.scene.hud.objects[0].data = pygame.transform.rotate(Screen.scene.hud.objects[0].source, -10)
    
    def turnOeufRight(self) -> None:
        Screen.scene.hud.objects[0].data = pygame.transform.rotate(Screen.scene.hud.objects[0].source, 10)

    def spawnTomauvais(self) -> None:
        Sounds.bouh.play()
        Screen.scene.hud.objects.append(
            Image(Vec2(Screen.dim.x, Screen.dim.y/2+40), Vec2(100, 100), "./resources/tomauvais.png")
        )
        Screen.scene.hud.objects[-1].source = Screen.scene.hud.objects[-1].data

    def moveTomauvaisLeft(self) -> None:
        Screen.scene.hud.objects[-1].changePosBy(Vec2(-Screen.dim.x*0.06, 0))

    def moveTomauvaisRight(self) -> None:
        Screen.scene.hud.objects[-1].changePosBy(Vec2(Screen.dim.x*0.06, 0))

    def moveFemboyRight(self) -> None:
        Screen.scene.hud.objects[1].changePosBy(Vec2(Screen.dim.x*0.06, 0))

    def makeOeufSad(self) -> None:
        Screen.scene.hud.objects[0] = \
            Image(Screen.dim/2-Vec2(50, 0), Vec2(100, 100), "./resources/oeuf_cry.png")
    
    def zoomOnScene(self) -> None:
        Sounds.snif.play()
        Screen.scene.world.camera.fov = 25
        Screen.scene.hud.objects[0].setDimTo(Vec2(400, 400))
    
    def showControls(self) -> None:
        Screen.scene.world.camera.fov = 25
        Screen.scene.hud.objects[0].setPosTo(Screen.dim/2+Vec2(300, 0))
        Screen.scene.hud.objects.append(
            Text(Screen.dim/2+Vec2(-200, -100), "Move: ZQSD - WASD - Arrow", 40, Constants.COLOR_WHITE)
        )
        Screen.scene.hud.objects.append(
            Text(Screen.dim/2+Vec2(-200, -50), "Jump: Z - W - SPACE", 40, Constants.COLOR_WHITE)
        )
        Screen.scene.hud.objects.append(
            Text(Screen.dim/2+Vec2(-200, 0), "Restart: R", 40, Constants.COLOR_WHITE)
        )
        Screen.scene.hud.objects.append(
            Text(Screen.dim/2+Vec2(-200, 50), "Quit: ECHAP", 40, Constants.COLOR_WHITE)
        )

    def spawnBackButton(self) -> None:
        Screen.scene.hud.objects.append(
            Button(Vec2(Screen.dim.x/2, Screen.dim.y-100), Vec2(180, 40), Screen.scene.setSelectionScene, None,
                Constants.COLOR_BLACK, Constants.COLOR_GREY, Text(Vec2(), "Continuer", 28, Constants.COLOR_WHITE))
        )