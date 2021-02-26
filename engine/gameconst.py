"""
Author: FurWaz
https://furwaz.github.io/

This module contains all the stuff about game variables, settings
and loading / saving things.
"""

from engine.gametypes import Color, Vec2
import json

class Constants:
    COLOR_BLACK=Color()
    COLOR_GREY=Color()
    COLOR_WHITE=Color()
    COLOR_TRANSPARENT=Color()
    COLOR_SKY=Color()
    COLOR_DIRT=Color()
    COLOR_GRASS=Color()
    COLOR_STONE=Color()
    
    GRAVITY=0
    JUMP_FORCE=0
    RESOLUTION=Vec2()
    FULLSCREEN=False
    LEVEL_NUMBER=0
    DEMOLEVEL_COMPLETE=False
    
    WORLD_AIR=0
    WORLD_GRASS=1
    WORLD_DIRT=2
    WORLD_STONE=3
    WORLD_START=4
    WORLD_END=5
    WORLD_ENNEMY=6

    def loadSettings():
        f = open("./resources/data.json")
        data = json.loads(f.read())
        f.close()

        res = data["resolution"].split("x")
        Constants.RESOLUTION = Vec2(int(res[0]), int(res[1]))
        Constants.FULLSCREEN = data["fullscreen"]
        Constants.LEVEL_NUMBER = data["level_number"]
        Constants.DEMOLEVEL_COMPLETE = data["demolevel_complete"]
        data = data["variables"]
        color=data["COLOR_BLACK"];Constants.COLOR_BLACK=Color(color["r"], color["g"], color["b"])
        color=data["COLOR_GREY"];Constants.COLOR_GREY=Color(color["r"], color["g"], color["b"])
        color=data["COLOR_WHITE"];Constants.COLOR_WHITE=Color(color["r"], color["g"], color["b"])
        color=data["COLOR_TRANSPARENT"];Constants.COLOR_TRANSPARENT=Color(color["r"], color["g"], color["b"])
        color=data["COLOR_SKY"];Constants.COLOR_SKY=Color(color["r"], color["g"], color["b"])
        color=data["COLOR_DIRT"];Constants.COLOR_DIRT=Color(color["r"], color["g"], color["b"])
        color=data["COLOR_GRASS"];Constants.COLOR_GRASS=Color(color["r"], color["g"], color["b"])
        color=data["COLOR_STONE"];Constants.COLOR_STONE=Color(color["r"], color["g"], color["b"])
        Constants.GRAVITY=data["GRAVITY"]
        Constants.JUMP_FORCE=data["JUMP_FORCE"]
        Constants.WORLD_AIR=data["WORLD_AIR"]
        Constants.WORLD_GRASS=data["WORLD_GRASS"]
        Constants.WORLD_DIRT=data["WORLD_DIRT"]
        Constants.WORLD_STONE=data["WORLD_STONE"]
        Constants.WORLD_START=data["WORLD_START"]
        Constants.WORLD_END=data["WORLD_END"]
        Constants.WORLD_ENNEMY=data["WORLD_ENNEMY"]

    def saveSettings():
        data = \
        {
            "resolution": str(Constants.RESOLUTION.x)+"x"+str(Constants.RESOLUTION.y),
            "fullscreen": Constants.FULLSCREEN,
            "demolevel_complete": Constants.DEMOLEVEL_COMPLETE,
            "level_number": Constants.LEVEL_NUMBER,
            "variables": {
                "COLOR_BLACK": Constants.COLOR_BLACK.toDict(),
                "COLOR_GREY": Constants.COLOR_GREY.toDict(),
                "COLOR_WHITE": Constants.COLOR_WHITE.toDict(),
                "COLOR_TRANSPARENT": Constants.COLOR_TRANSPARENT.toDict(),
                "COLOR_SKY": Constants.COLOR_SKY.toDict(),
                "COLOR_DIRT": Constants.COLOR_DIRT.toDict(),
                "COLOR_GRASS": Constants.COLOR_GRASS.toDict(),
                "COLOR_STONE": Constants.COLOR_STONE.toDict(),
                "GRAVITY": Constants.GRAVITY,
                "JUMP_FORCE": Constants.JUMP_FORCE,
                "WORLD_AIR": Constants.WORLD_AIR,
                "WORLD_GRASS": Constants.WORLD_GRASS,
                "WORLD_DIRT": Constants.WORLD_DIRT,
                "WORLD_STONE": Constants.WORLD_STONE,
                "WORLD_START": Constants.WORLD_START,
                "WORLD_END": Constants.WORLD_END,
                "WORLD_ENNEMY": Constants.WORLD_ENNEMY
            }
        }
        
        f = open("./resources/data.json", "w")
        f.write(json.dumps(data, sort_keys=True, indent=4))
        f.close()