"""
Author: FurWaz
https://furwaz.github.io/

This module contains the Sounds object used to load and store
all the necessary audio files.
"""
import pygame
class Sounds:
    bouh:pygame.mixer.Sound = None
    clic:pygame.mixer.Sound = None
    boing:pygame.mixer.Sound = None
    snif:pygame.mixer.Sound = None
    tulututu:pygame.mixer.Sound = None
    yes:pygame.mixer.Sound = None
    aie:pygame.mixer.Sound = None

    def init():
        Sounds.bouh = pygame.mixer.Sound('./resources/bouh.wav')
        Sounds.clic = pygame.mixer.Sound('./resources/clic.wav')
        Sounds.boing = pygame.mixer.Sound('./resources/boing.wav')
        Sounds.snif = pygame.mixer.Sound('./resources/snif.wav')
        Sounds.tulututu = pygame.mixer.Sound('./resources/tulututu.wav')
        Sounds.yes = pygame.mixer.Sound('./resources/yes.wav')
        Sounds.aie = pygame.mixer.Sound('./resources/aie.wav')