"""
Author: FurWaz
https://furwaz.github.io/

This module contains the Screen element, that is used to create the Window
but also used to store the current displayed scene, get the events, update and draw the scene.
"""
from engine.gameconst import Constants
from typing import Any, Iterable
from engine.gamegraphs import GraphElement
from engine.gametypes import pygame, Vec2, Color

class Screen:
    dim = Vec2()
    dt = 0.016
    scene=None
    sceneCode=0
    monitorDims = Vec2()
    RES = [Vec2(640, 360), Vec2(1280, 720), Vec2(1600, 900), Vec2(1920, 1080), Vec2(2560, 1440)]
    RES_INDEX = 0
    def __init__(self, pos:Vec2=Vec2(), dim:Vec2=Vec2(640, 360), t:str="Title", i:GraphElement=GraphElement(), fps:int=60, fullscreen:bool=False) -> None:
        Screen.dim = dim
        Screen.dt = 0.016
        displayDims = pygame.display.Info()
        Screen.monitorDims = Vec2(displayDims.current_w, displayDims.current_h)
        self.fullscreen = fullscreen
        self.clock = pygame.time.Clock()
        self.pos = pos
        self.title = t
        self.icon = i
        self.fps = fps
        self.openWindow()
        self.surface = pygame.display.get_surface()
        self.isOpen = True

    def changeRes(self) -> None:
        if self.fullscreen: return
        Screen.RES_INDEX = (Screen.RES_INDEX+1) % len(Screen.RES)
        newRes = Screen.RES[Screen.RES_INDEX]
        self.setDimTo(newRes)

    def setIcon(self, i:GraphElement=None) -> None:
        if i == None: return
        pygame.display.set_icon(pygame.transform.scale(i.data, (32, 32)))

    def setTitle(self, t:str="Title") -> None:
        pygame.display.set_caption(t)

    def toogleFullscreen(self) -> None:
        self.fullscreen = not self.fullscreen
        self.openWindow()

    def setDimAndPos(self, dim:Vec2=Vec2(), pos:Vec2=Vec2()) -> None:
        Screen.dim = dim
        self.pos = pos
        self.resizeWindow()

    def setPosTo(self, pos:Vec2=Vec2()) -> None:
        self.pos = pos
        self.moveWindow()

    def changePosBy(self, delta:Vec2=Vec2()) -> None:
        self.pos = self.pos+delta
        self.moveWindow()

    def changeDimBy(self, delta:Vec2=Vec2()) -> None:
        Screen.dim = Screen.dim+delta
        self.resizeWindow()

    def setDimTo(self, dim:Vec2=Vec2()) -> None:
        Screen.dim = dim
        self.resizeWindow()

    def getEvents(self) -> Iterable[pygame.event.Event]:
        events = []
        if Screen.scene.askForQuit: self.closeWindow(); return []
        if Screen.scene.askForChangeRes: self.changeRes()
        if Screen.scene.askForFullscreen: self.toogleFullscreen(); self.scene.askForFullscreen = False
        for e in pygame.event.get():
            if e.type == pygame.QUIT: self.closeWindow()
            elif e.type == pygame.VIDEORESIZE:
                Screen.dim = Vec2(e.w, e.h)
                self.resizeWindow()
            else: events.append(e)
        return events

    def openWindow(self) -> None:
        self.moveWindow()
        self.resizeWindow()
        pygame.display.set_caption(self.title)
        pygame.display.set_icon(pygame.transform.scale(self.icon.data, (32, 32)))
    
    def moveWindow(self) -> None:
        #os.environ['SDL_VIDEO_WINDOW_POS'] = str(self.pos.x)+","+str(self.pos.y)
        #os.environ['SDL_VIDEO_CENTERED'] = "0"
        self.resizeWindow()

    def resizeWindow(self) -> None:
        if self.fullscreen: pygame.display.set_mode(Screen.monitorDims.toTuple(), pygame.FULLSCREEN)
        else: pygame.display.set_mode(Screen.RES[Screen.RES_INDEX].toTuple())
        Constants.FULLSCREEN = self.fullscreen
        Constants.RESOLUTION.fromTuple(pygame.display.get_surface().get_size())
        pygame.display.set_icon(pygame.transform.scale(self.icon.data, (32, 32)))
        try: Screen.scene.reloadScene()
        except: pass

    def closeWindow(self) -> None:
        self.isOpen = False;
        pygame.display.quit()

    def clear(self, color:Color=Color(0,0,0)) -> None:
        if not self.isOpen: return
        self.surface.fill(color.toTuple())

    def drawElement(self, element:GraphElement=None) -> None:
        if element == None: return
        if not self.isOpen: return
        self.surface.blit(element.data, element.pos.toTuple())

    def drawScene(self, scene:Any=None) -> None:
        if scene == None: return
        if not self.isOpen: return
        if scene.world != None:
            self.surface.blit(scene.world.data, (0, 0))
        if scene.player != None:
            self.surface.blit(scene.player.graph.data, (scene.player.graph.pos-scene.player.graph.dim/2).toTuple())
        for el in scene.hud.objects:
            self.surface.blit(el.data, (el.pos-el.dim/2).toTuple())

    def update(self) -> None:
        if not self.isOpen: return
        Screen.dt = self.clock.tick(self.fps) / 1000
        pygame.display.flip()