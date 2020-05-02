import pygame as pg
import copy
from fw.functions import *
from fw.GameObject import *
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


        self.setDirectionImage(self.real_direction)





    #--------------------------------------------------------------------------------
    #
    def setDirectionImage(self,direction):
        pass

