import pygame as pg
import numpy as np
from config import *
from fw.functions import *

from fw.GuiWindow import GuiWindow
# from CellWeed import *
# from CellOvalis import *
from Tile import *
from Car import *
from Camera import *

import random




#
# окно с органами управления игрой
#
class MapWnd(GuiWindow):

    def __init__(self,params):

        params['rect'] = MAP_WND_RECT
        params['bg_color'] = MAP_WND_BACKGROUND
        params['name'] = 'MapWnd'


        super().__init__(params)        # parent - GuiWindow

        self.background_srf = pg.Surface(MAP_SIZE_XY)
        self.Camera = Camera(MAIN_WND_WIDTH,MAIN_WND_HEIGHT,MAP_SIZE_X,MAP_SIZE_Y)


        #группы спрайтов
        self.arr_sprites_update_camera = pg.sprite.Group()  # для взывова draw, карта отдельно копируемся
        self.arr_sprites_draw = pg.sprite.Group()           # для взывова draw, карта отдельно копируемся
        self.arr_sprites_update = pg.sprite.Group()         # то что двигаетсмя
        self.arr_sprites_collide = pg.sprite.Group()        # прверяиьт на столкновения с автомобилем


        #тайловая карта
        #тайлы двух видов, определяются случайно
        #тайлы спрайтами не являются, а копируеются один раз прямо на фон
        for x in range(MAP_TAIL_SIZE_X):
            for y in range(MAP_TAIL_SIZE_Y):
                #номер типа тайла случайно
                rand = random.randint(0, 1)
                dest_rect = pg.Rect(
                    Tile.SPRITE_SIZE_X * x,
                    Tile.SPRITE_SIZE_Y * y,
                    Tile.SPRITE_SIZE_X,
                    Tile.SPRITE_SIZE_Y)

                Tile.copyImg(self.background_srf, dest_rect, rand)



        #нарисуем деревья

        self.arr_trees = []
        arr_groups = (self.arr_sprites_update_camera, self.arr_sprites_draw, self.arr_sprites_collide)

        self.arr_trees.append(
            Tree(0, 0, arr_groups)
        )

        self.arr_trees.append(
            Tree(200, 200, arr_groups)
        )

        self.arr_trees.append(
            Tree(2045, 614, arr_groups)
        )

        self.arr_oils = []

        self.arr_oils.append(
            Oil(400, 400, (self.arr_sprites_update_camera, self.arr_sprites_draw))
        )

        self.arr_rocks = []
        self.arr_rocks.append(
            Rock(600, 400, (self.arr_sprites_update_camera,self.arr_sprites_update, self.arr_sprites_draw))
        )

        self.arr_cars = []
        self.arr_cars.append(
            Car(400, 200, (self.arr_sprites_update_camera,self.arr_sprites_update, self.arr_sprites_draw))
        )


        arr_road_point = [[]*3]

        self.arr_road_point = [
            (0,   200),
            (100, 100),
            (200, 200),
            (300, 300),
            (350, 400),
        ]

        getMainWnd().registerHandler_MOUSEBUTTONDOWN(self)
        getMainWnd().registerHandler_KEYDOWN(self)
        getMainWnd().registerHandler_KEYUP(self)


    def update(self):
        self.Camera.update()



    def draw_this(self):
        #копируем карту тайлов
        #self.drawBackground()       #оригинальная родная заливка фона -

        #координаты окна показываемые камерой относительно карты
        camera_position_rect = self.Camera.getPositionRect()

        #копируем фон(тайловая карта)
        self.surface.blit(          # копируем в окно MapWnd
            self.background_srf,    # копируем из карты
            pg.Rect(0,0,0,0),       # копируем на все окно MapWnd
            camera_position_rect)   # из карты берем то что показывает камера

        #пересчитываем координаты в спрайтах с учетом камеры
        for sprite in self.arr_sprites_update_camera:
            sprite.update_camera(camera_position_rect)

        self.arr_sprites_update.update()

        sprite_lst = pg.sprite.spritecollide(
            self.arr_cars[0],           #машину сталикиваем
            self.arr_sprites_collide,    #
            False,
            pg.sprite.collide_mask
        )

        prev = None
        for point in self.arr_road_point:
            if (prev != None ):
                pg.draw.line(
                    self.surface,
                    (200,0,0),
                    prev,
                    point,
                    1
                )

            prev = point


        # if (sprite_lst):
        #     sprite_lst[0].kill()
        #     print("TOUCH !!")

        self.arr_sprites_draw.draw(self.surface)


    def handle_MOUSEBUTTONDOWN(self,event):
        if (event.button == 1):
            # нажата левая кнопка

            if (self.isPointInWindow(event.pos)):
                #кнопка нажата в зоне карты


                #абсолютные координаты мыши -> в относительные в окне
                # event.pos - абсолютные кордингаты клика относительно онка приложения
                # click_mapwnd_rect - координаты относительна окна mapwnd
                click_mapwnd_rect = pg.Rect(
                    calcAbsToOffset(self.surface.get_abs_offset(),event.pos),
                    (0,0)
                )

                # координаты окна показываемые камерой относительно карты
                camera_position_rect = self.Camera.getPositionRect()

                #координаты клика относительно карты
                click_map_rect =  camera_position_rect.move(click_mapwnd_rect.topleft)

                self.arr_cars[0].setTarget(click_map_rect)


    def handle_KEYDOWN(self,event):
        if (event.key == pg.K_LEFT):
            self.Camera.moveLeft()



        elif (event.key == pg.K_RIGHT):
            self.Camera.moveRight()



    def handle_KEYUP(self,event):
        if (event.key == pg.K_LEFT):
            self.Camera.moveStop()

        elif (event.key == pg.K_RIGHT):
            self.Camera.moveStop()
