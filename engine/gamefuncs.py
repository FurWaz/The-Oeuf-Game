"""
Author: FurWaz
https://furwaz.github.io/

This module contains all the useful functions used in the game.
"""

def clamp(value:int=50, min_:int=0, max_:int=100) -> int:
    return max(min(value, max_), min_)