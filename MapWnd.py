import pygame as pg
from config import *
from functions import *

from GuiWindow import GuiWindow
from CellWeed import *
from CellOvalis import *
from Tile import *

import random


TAIL_MAP_SIZE_X   = 6
TAIL_MAP_SIZE_Y    = 20

#
# окно с органами управления игрой
#
class MapWnd(GuiWindow):

    def __init__(self,params):

        params['rect'] = MAP_WND_RECT
        params['bg_color'] = MAP_WND_BACKGROUND
        params['name'] = 'MapWnd'


        super().__init__(params)    # parent - GuiWindow

        #тайловая карта
        arrTailMap = [[0 for x in range(TAIL_MAP_SIZE_X)] for y in range(TAIL_MAP_SIZE_Y)]

        for tail in arrTailMap:
            tail=random.randint(0,1)


        self.sg_cells = pg.sprite.Group()
        self.arr_cells = [];

        ## 0

        cell = CellWeed({
            'parent_obj': self,
            'centr_pos': (300, 60),
        })
        self.sg_cells.add(cell)
        self.arr_cells.append(cell)

        ## 1
        cell = CellWeed({
            'parent_obj':self,
            'centr_pos': (130,60),
        })
        self.sg_cells.add(cell)
        self.arr_cells.append(cell)


        ## 2
        cell = CellOvalis({
            'parent_obj':self,
            'centr_pos': (200,60),
        })
        self.sg_cells.add(cell)
        self.arr_cells.append(cell)


        getMainWnd().registerHandler_MOUSEBUTTONDOWN(self)


    def update(self):
        self.sg_cells.update()

    def draw_this(self):
        self.drawBackground()
        self.sg_cells.draw(self.surface)

    def handle_MOUSEBUTTONDOWN(self,event):
        if (event.button == 1):
            # нажата левая кнопка

            if (self.isPointInWindow(event.pos)):
                #кнопка нажата в зоне кнопки карты


                #абсолютные координаты мыши -> в относительные в окне
                point_pos = calcAbsToOffset(self.surface.get_abs_offset(),event.pos)

                self.arr_cells[2].setTarget(point_pos)


