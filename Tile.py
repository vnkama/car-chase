import pygame as pg
from functions import *

class Tile(pg.sprite.Sprite):

    SPRITE_SIZE_X = SPRITE_SIZE_Y = 128
    SPRITE_SIZE_XY = (SPRITE_SIZE_X,SPRITE_SIZE_Y)

    arrTilesPng = []

    srf = pg.image.load("./images/land_grass04.png").convert_alpha()
    arrTilesPng.insert(1,srf)

    srf = pg.image.load("./images/land_grass11.png").convert_alpha()
    arrTilesPng.insert(2,srf)


    def __init__(self):
        pass

