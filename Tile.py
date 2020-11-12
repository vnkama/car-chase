import pygame as pg
from fw.functions import *

#
#
#
class Tile:
    SPRITE_SIZE_X = SPRITE_SIZE_Y = 128
    SPRITE_SIZE_XY = (SPRITE_SIZE_X, SPRITE_SIZE_Y)

    arr_tiles_img = []

    srf = pg.image.load("./images/land_grass04.png").convert()
    arr_tiles_img.insert(1, srf)

    srf = pg.image.load("./images/land_grass11.png").convert()
    arr_tiles_img.insert(2, srf)


    # def __init__(self,params):
    #     self.floor_type = params['floor_type']

    @staticmethod
    def copyImg(dest_srf, dest_rect, sprite_num):
        dest_srf.blit(Tile.arr_tiles_img[sprite_num], dest_rect)


class Tree(pg.sprite.Sprite):
    SPRITE_SIZE_X = SPRITE_SIZE_Y = 141
    SPRITE_SIZE_XY = (SPRITE_SIZE_X,SPRITE_SIZE_Y)

    image = pg.image.load("./images/tree_small.png").convert_alpha()

    def __init__(self, x, y, groups):
        super().__init__(groups)

        # self.map_rect координаты првязанные к карте, они неизменны (для неподвижных спрайтов)
        # self.rect координаты привязанные к камере, они пересчитываются при скроллинге карты

        self.map_rect = pg.Rect(
            x-Tree.SPRITE_SIZE_X/2,
            y-Tree.SPRITE_SIZE_Y/2,
            Tree.SPRITE_SIZE_X,
            Tree.SPRITE_SIZE_Y
        )

        self.rect = self.map_rect.copy()

    def updateCamera(self, camera_rect):
        self.rect.left = self.map_rect.left - camera_rect.left
        self.rect.top = self.map_rect.top - camera_rect.top


    # def copyImg(dest_srf,dest_rect):
    #     dest_srf.blit(Tree.surfaceImg,dest_rect)


class Oil(pg.sprite.Sprite):
    SPRITE_SIZE_X = 109
    SPRITE_SIZE_Y = 95
    SPRITE_SIZE_XY = (SPRITE_SIZE_X,SPRITE_SIZE_Y)

    image = pg.image.load("./images/oil.png").convert_alpha()

    def __init__(self,x,y,groups):
        super().__init__(groups)

        # self.map_rect координаты првязанные к карте, они неизменны (для неподвижных спрайтов)
        # self.rect координаты привязанные к камере, они пересчитываются при скроллинге карты

        self.map_rect = pg.Rect(
            x-Tree.SPRITE_SIZE_X/2,
            y-Tree.SPRITE_SIZE_Y/2,
            Tree.SPRITE_SIZE_X,
            Tree.SPRITE_SIZE_Y
        )

        self.rect = self.map_rect.copy()

    def updateCamera(self,camera_rect):
        self.rect.left = self.map_rect.left - camera_rect.left
        self.rect.top = self.map_rect.top - camera_rect.top


class Rock(pg.sprite.Sprite):
    SPRITE_SIZE_X = 73
    SPRITE_SIZE_Y = 68
    SPRITE_SIZE_XY = (SPRITE_SIZE_X,SPRITE_SIZE_Y)

    image = pg.image.load("./images/rock2.png").convert_alpha()

    def __init__(self,x,y,groups):
        super().__init__(groups)

        # self.map_rect координаты првязанные к карте, они неизменны (для неподвижных спрайтов)
        # self.rect координаты привязанные к камере, они пересчитываются при скроллинге карты

        self.dy = 3

        self.map_rect = pg.Rect(
            x-Tree.SPRITE_SIZE_X/2,
            y-Tree.SPRITE_SIZE_Y/2,
            Tree.SPRITE_SIZE_X,
            Tree.SPRITE_SIZE_Y
        )

        self.rect = self.map_rect.copy()


    def updateCamera(self, camera_rect):
        self.rect.left = self.map_rect.left - camera_rect.left
        self.rect.top = self.map_rect.top - camera_rect.top


    def update(self, *args):
        if self.map_rect.top > 600:
            self.dy = -3
        elif self.map_rect.top < 50:
            self.dy = 3

        self.map_rect.top = self.map_rect.top + self.dy



#
#
#
class Curb(pg.sprite.Sprite):

    def __init__(self, p0_xy, p1_xy, arr_lineEqualABC, groups):
        super().__init__(groups)

        self.arr_lineEqualABC = arr_lineEqualABC

        # левый верхний угол спрайта, относительно карты
        pos_xy = (
            min(p0_xy[0],p1_xy[0]),
            min(p0_xy[1],p1_xy[1])
        )

        # начало и конец. храним отдельно от map_rect, для быстродействия
        self.start_2fdot = p0_xy
        self.end_2fdot = p1_xy

        #print(self.start_2fdot,self.end_2fdot)


        # размер спрайта
        size_xy = (
            int(abs(p0_xy[0]-p1_xy[0]) + 1),
            int(abs(p0_xy[1]-p1_xy[1]) + 1)
        )
        self.map_rect = pg.Rect(pos_xy,size_xy)
        self.rect = self.map_rect.copy()


        self.image = pg.Surface(size_xy)
        self.image.set_alpha(0)   #0- прозрачный

        COLORKEY = (255,255,255)
        self.image.fill(COLORKEY)
        self.image.set_colorkey(COLORKEY)

        color = (200, 55, 25)

        # рисуем линию - границу дороги
        if (
            ((p0_xy[0] <= p1_xy[0]) and (p0_xy[1] <= p1_xy[1])) or
            ((p1_xy[0] <= p0_xy[0]) and (p1_xy[1] <= p0_xy[1]))
        ):
            pg.draw.line(self.image, color, (0, 0), (self.rect.size[0] - 1, self.rect.size[1] - 1), 1)

        else:
            pg.draw.line(self.image, color, (0,self.rect.size[1] - 1), (self.rect.size[0] - 1,0), 1)


    def updateCamera(self,camera_rect):
        self.rect.left = self.map_rect.left - camera_rect.left
        self.rect.top = self.map_rect.top - camera_rect.top




