import pygame as pg

# from config import *
# from functions import *

#
#
#
class Camera:
    def __init__(self, size_w, size_h,map_size_w,map_size_h):
        self.position = pg.Rect(0, 0, size_w, size_h)
        self.width = size_w
        self.height = size_h
        self.map_size_w = map_size_w
        self.map_size_h = map_size_h

        self.dx = 0

    def apply(self,rect):
        pass

    def getPositionRect(self):
        #возвращает область камеры в системе координат большой карты
        return self.position


    def update(self,target_rect=None):
        #расчитывает позицию камеры в пределах map
        #камера наводится так, чтобы target_rect был по возможности по середине
        if (self.dx<0 and self.position.left < -self.dx):
            self.position = self.position.move(self.position.left, 0)
        elif (self.dx>0 and self.map_size_w - self.position.right < self.dx):
            self.position = self.position.move(self.map_size_w - self.position.right, 0)
        else:
            self.position = self.position.move(self.dx,0)

    def moveLeft(self):
        self.dx = -4

    def moveRight(self):
        self.dx = +4

    def moveStop(self):
        self.dx = 0


