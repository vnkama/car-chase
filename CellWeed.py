import pygame as pg
from Cell import *



class CellWeed(Cell):
    image = pg.image.load("./images/weed-24.png").convert_alpha()

    WEED_SIZE = (32,32)

    def __init__(self,params):
        #params['rect'] = pg.Rect(offsetPoint(params['centr_pos'],(-16,-16)), CellWeed.WEED_SIZE)

        super().__init__(params)


    def setPos(self,pos):
        self.centr_pos = pos
        self.rect = pg.Rect(offsetPoint(pos,(-(CellWeed.WEED_SIZE[0]/2),-(CellWeed.WEED_SIZE[1]/2))), CellWeed.WEED_SIZE)

    # def update(self):
    #     pass


    #def draw(self):
#        pass


