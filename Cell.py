import pygame as pg
import copy
from functions import *
from GameObject import *
from Brezenhem import Brezenhem


class Cell(pg.sprite.Sprite):

    #direct_16_srf = pg.image.load("./images/direct-16-512.png").convert()

    def __init__(self,params):
        pg.sprite.Sprite.__init__(self)
        self.setPos(params['centr_pos'])
        self.brezenhem = Brezenhem()
        self.is_moving = 0
        self.real_speed = 0
        self.real_direction = 0  #реальное напраывление объекта направление для спрайта
        self.rotate_direction = 0   #направление вращения 0 против часовой стрелки
        self.need_direction = 0 #куда крутимся


    #--------------------------------------------------------------------------------
    #
    #
    def setTarget(self, target_pos):

        self.target_pos = target_pos
        self.is_moving = 1

        # координатат конца отрезка относитльно его начала
        #self.pathsection_vector = calcAbsToOffset(self.centr_pos,self.target_pos)
        self.brezenhem.start(self.centr_pos,self.target_pos)

        #определим желаемое направление движения
        self.need_direction = self.brezenhem.getSpriteDirection16()


        if (self.need_direction != self.real_direction):
            if (self.need_direction > self.real_direction):
                if (self.need_direction - self.real_direction <= 8):
                    self.rotate_direction = 1
                else:
                    self.rotate_direction = -1
            else:
                if (self.real_direction - self.need_direction <= 8):
                    self.rotate_direction = -1
                else:
                    self.rotate_direction = 1



        self.real_speed = 0
        self.rotate_msector_s = 0          #1000


        #self.setDirectionImage(self.real_direction)





    #--------------------------------------------------------------------------------
    #
    def setDirectionImage(self,direction):
        pass


    # def draw(self):
    #     pass






        # if (self.is_moving):
        #     if self.centr_pos[0] < 500:
        #     elif self.centr_pos[0] >= 300:
        #         self.is_moving = 0



    # def movePos(self,offset):
    #     #сдвигаем Cell
    #     self.setPos(offsetPoint(self.centr_pos,offset))



    #
    #
    # def getSpriteDirection(self,movement_vector):
    #     #возвращает напрвление спрайта по вектору движения
    #
    #     vector = list(movement_vector)     #тк movement_vector передан по ссылке !!
    #     max_size = max(abs(vector[0]), abs(vector[1]))
    #
    #     while (max_size > 512):
    #         vector[0] >>=  1
    #         vector[1] >>=  1
    #         max_size = max(abs(vector[0]), abs(vector[1]))
    #
    #     direction_clr = Cell.direct_16_srf.get_at((abs(vector[0]), abs(vector[1])))[0:3]
    #
    #
    #     if (direction_clr[0:3] == (0,0,0)):
    #         direction = 4
    #     elif (direction_clr[0:3] == (48,0,0)):
    #         direction = 3
    #     elif (direction_clr[0:3] == (0,48,0)):
    #         direction = 2
    #     elif (direction_clr[0:3] == (0,0,48)):
    #         direction = 1
    #     elif (direction_clr[0:3] == (48,48,48)):
    #         direction = 0
    #     else:
    #         direction = None
    #
    #     if (direction is not None):
    #         if (movement_vector[0] < 0 and  movement_vector[1] > 0):
    #             direction = 8 - direction
    #
    #         elif (movement_vector[0] < 0 and  movement_vector[1] < 0):
    #             direction += 8
    #
    #         elif (movement_vector[0] >= 0 and  movement_vector[1] < 0):
    #             direction = (16 - direction) & 0xF
    #
    #     return direction