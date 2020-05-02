import pygame as pg
import numpy as np
from config import *
from fw.functions import *

from fw.GuiWindow import GuiWindow
from CellWeed import *
from CellOvalis import *
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
        # self.slid_left = 0
        # self.slid_right = 0


        #группы спрайтов
        self.arr_sprites_update_camera = pg.sprite.Group()       # для взывова draw, карта отдельно копируемся
        self.arr_sprites_for_draw = pg.sprite.Group()       # для взывова draw, карта отдельно копируемся
        self.arr_sprites_for_update = pg.sprite.Group()     # то что двигаетсмя
        self.arr_sprites_for_collide = pg.sprite.Group()    # прверяиьт на столкновения с автомобилем


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

        self.arr_trees.append(
            Tree(200, 100, (self.arr_sprites_update_camera, self.arr_sprites_for_draw, self.arr_sprites_for_collide))
        )

        self.arr_trees.append(
            Tree(840, 270, (self.arr_sprites_update_camera, self.arr_sprites_for_draw, self.arr_sprites_for_collide))
        )

        self.arr_trees.append(
            Tree(2045, 614, (self.arr_sprites_update_camera, self.arr_sprites_for_draw, self.arr_sprites_for_collide))
        )

        # Tree.copyImg(
        #     self.background_srf,
        #     pg.Rect(200,100,0,0)        # размер rect значения не имеет
        # )
        #
        # Tree.copyImg(
        #     self.background_srf,
        #     pg.Rect(843,243,0,0)        # размер rect значения не имеет
        # )
        #
        # Tree.copyImg(
        #     self.background_srf,
        #     pg.Rect(2045,614,0,0)        # размер rect значения не имеет
        # )
        #
        #
        # Oil.copyImg(
        #     self.background_srf,
        #     pg.Rect(400, 400, 0, 0)  # размер rect значения не имеет
        # )




        self.sg_cells = pg.sprite.Group()
        self.arr_cells = [];


        ## 0
        cell = Car({
            'parent_obj': self,
            'centr_pos': (300, 60),
        })
        self.sg_cells.add(cell)
        self.arr_cells.append(cell)


        ## 1

        cell = CellWeed({
            'parent_obj': self,
            'centr_pos': (300, 60),
        })
        self.sg_cells.add(cell)
        self.arr_cells.append(cell)

        ## 2
        cell = CellWeed({
            'parent_obj':self,
            'centr_pos': (130,60),
        })
        self.sg_cells.add(cell)
        self.arr_cells.append(cell)


        ## 3
        cell = CellOvalis({
            'parent_obj':self,
            'centr_pos': (200,60),
        })
        self.sg_cells.add(cell)
        self.arr_cells.append(cell)


        getMainWnd().registerHandler_MOUSEBUTTONDOWN(self)
        getMainWnd().registerHandler_KEYDOWN(self)
        getMainWnd().registerHandler_KEYUP(self)


    def update(self):
        self.Camera.update()
        self.sg_cells.update()

    def draw_this(self):
        #копируем карту тайлов
        #self.drawBackground()       #удалить DEBUG

        #координаты окна показываемые камерой относительно карты
        camera_position_rect = self.Camera.getPositionRect()

        #копируем фон(тайловая карта)
        self.surface.blit(          # копируем в окно MapWnd
            self.background_srf,    # копируем из карты
            pg.Rect(0,0,0,0),       # копируем на все окно MapWnd
            camera_position_rect)   # из карты берем то что показывает камера
        self.sg_cells.draw(self.surface)

        #пересчитываем координаты в спрайтах с учетом камеры
        for sprite in self.arr_sprites_update_camera:
            sprite.update_camera(camera_position_rect)

        self.arr_sprites_for_draw.draw(self.surface)



    def handle_MOUSEBUTTONDOWN(self,event):
        if (event.button == 1):
            # нажата левая кнопка

            if (self.isPointInWindow(event.pos)):
                #кнопка нажата в зоне кнопки карты


                #абсолютные координаты мыши -> в относительные в окне
                point_pos = calcAbsToOffset(self.surface.get_abs_offset(),event.pos)

                self.arr_cells[0].setTarget(point_pos)


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
