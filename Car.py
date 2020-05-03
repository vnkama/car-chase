import pygame as pg
from config import *
from fw.functions import *

from Brezenhem import Brezenhem

class Car(pg.sprite.Sprite):
    CAR_RED=2
    CAR_GREEN=1

    SPRITE_SIZE_X = 150
    SPRITE_SIZE_Y = 150
    SPRITE_SIZE_XY = (SPRITE_SIZE_X,SPRITE_SIZE_Y)

    arr_img_srf = []

    #скорость вращения,
    # 1000 соответсвует 1 оборот в секеунду, 2000- два оборота в секунду итп
    rotate_speed__mturn_sec = 1000


    #скорость вращения: милли сектор в тик
    # на эту переменную увеличивается счечтк вращения каждый тик FPS
    # как только наберется 1000 , то спрайт поворачивается на 1/16
    rotate_msector_v = rotate_speed__mturn_sec * 32 // FPS_RATE

    for i in range(0,32):
        file_name = "./images/car-green/car_green_3_{:02d}.png".format(i)
        srf = pg.image.load(file_name).convert_alpha()
        arr_img_srf.insert(i,srf)


    def __init__(self,x,y,groups):
        super().__init__(groups)

        # self.map_rect координаты првязанные к карте, они неизменны (для неподвижных спрайтов)
        # self.rect координаты привязанные к камере, они пересчитываются при скроллинге карты

        self.map_rect = pg.Rect(
            x-Car.SPRITE_SIZE_X/2,
            y-Car.SPRITE_SIZE_Y/2,
            Car.SPRITE_SIZE_X,
            Car.SPRITE_SIZE_Y
        )
        self.rect = self.map_rect.copy()

        #self.setPos(params['centr_pos'])

        self.image = Car.arr_img_srf[0]
        self.brezenhem = Brezenhem()
        self.is_moving = 0
        self.real_speed = 0
        self.real_direction = 0  #реальное напраывление объекта направление для спрайта
        self.rotate_direction = 0   #направление вращения 0 против часовой стрелки
        self.need_direction = 0 #куда крутимся

        # params["cent_pos"][0] -
        # params["cent_pos"][1]
        #
        # self.rect = pg.rect(,())

    # def copyImg(dest_srf,dest_rect):
    #     dest_srf.blit(Oil.arr_img_srf[self.color],dest_rect)

    def update_camera(self,camera_rect):
        self.rect.left = self.map_rect.left - camera_rect.left
        self.rect.top = self.map_rect.top - camera_rect.top

    def setPos(self,newpos_pos):
        self.map_rect.center = newpos_pos.topleft
        #self.rect = pg.Rect(offsetPoint(pos,(-(Car.SPRITE_SIZE_X/2),-(Car.SPRITE_SIZE_Y/2))), Car.SPRITE_SIZE_XY)


    def update(self):
        if (self.need_direction != self.real_direction):

            #добавляем небольшой поворот
            self.rotate_msector_s += self.rotate_msector_v

            if (self.rotate_msector_s >= 1000):
                #повернулись на 1 румб
                self.rotate_msector_s %= 1000   #копейки оставим на следющий румб

                self.real_direction = (self.real_direction + self.rotate_direction) #поворачиваем на 1 румб
                self.real_direction = self.real_direction if (self.real_direction <= 31) else 0
                self.real_direction = self.real_direction if (self.real_direction >= 0) else 31

                #меняем спрайт
                self.setDirectionImage(self.real_direction)

        else:
            #двигаемся
            if (self.brezenhem.isEnded()):
                self.is_moving = 0
            else:
                self.setPos(pg.Rect(self.brezenhem.nextPoint(),(0,0)))

    def setTarget(self, target_rect):
        #задает цель для движения

        self.target_rect = target_rect
        self.is_moving = 1

        # координатат конца отрезка относитльно его начала
        #self.pathsection_vector = calcAbsToOffset(self.centr_pos,self.target_pos)
        self.brezenhem.start(self.map_rect.center,self.target_rect)

        #определим желаемое направление движения
        self.need_direction = self.brezenhem.getSpriteDirection32()


        if (self.need_direction != self.real_direction):
            if (self.need_direction > self.real_direction):
                if (self.need_direction - self.real_direction <= 16):
                    self.rotate_direction = 1
                else:
                    self.rotate_direction = -1
            else:
                if (self.real_direction - self.need_direction <= 16):
                    self.rotate_direction = -1
                else:
                    self.rotate_direction = 1



        self.real_speed = 0
        self.rotate_msector_s = 0          #1000

    def setDirectionImage(self,direction):
        self.image = Car.arr_img_srf[direction]