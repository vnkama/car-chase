import pygame as pg
from fw.functions import *

class Tile(pg.sprite.Sprite):

    SPRITE_SIZE_X = SPRITE_SIZE_Y = 128
    SPRITE_SIZE_XY = (SPRITE_SIZE_X,SPRITE_SIZE_Y)

    arrTilesPng = []

    srf = pg.image.load("./images/land_grass04.png").convert_alpha()
    arrTilesPng.insert(1,srf)

    srf = pg.image.load("./images/land_grass11.png").convert_alpha()
    arrTilesPng.insert(2,srf)


    # def __init__(self,params):
    #     self.floor_type = params['floor_type']

    def copyImg(dest_srf,dest_rect,sprite_num):
        dest_srf.blit(Tile.arrTilesPng[sprite_num],dest_rect)


class Tree(pg.sprite.Sprite):
    SPRITE_SIZE_X = SPRITE_SIZE_Y = 141
    SPRITE_SIZE_XY = (SPRITE_SIZE_X,SPRITE_SIZE_Y)

    surfaceImg = pg.image.load("./images/tree_small.png").convert_alpha()

    def copyImg(dest_srf,dest_rect):
        dest_srf.blit(Tree.surfaceImg,dest_rect)


class Oil(pg.sprite.Sprite):
    SPRITE_SIZE_X = 109
    SPRITE_SIZE_Y = 95
    SPRITE_SIZE_XY = (SPRITE_SIZE_X,SPRITE_SIZE_Y)

    surfaceImg = pg.image.load("./images/oil.png").convert_alpha()

    def copyImg(dest_srf,dest_rect):
        dest_srf.blit(Oil.surfaceImg,dest_rect)

