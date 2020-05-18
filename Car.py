import pygame as pg
from config import *
from fw.functions import *
from Vector import *
import math

from Brezenhem import Brezenhem

#
#
#
class Car(pg.sprite.Sprite):
    CAR_RED=2
    CAR_GREEN=1

    SPRITE_SIZE_X = 80
    SPRITE_SIZE_Y = 80
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


    def __init__(self,map,x,y,groups,message):
        super().__init__(groups)

        #указатель "наверх" на карту
        self.map = map

        # self.map_rectpos координаты центра спрайта привязанные к карте, они неизменны (для неподвижных спрайтов)
        # self.map_rectpos здесь только объявлен, будет переопределен в setPos
        #self.map_rectpos = None
        self.map_rectpos = pg.Rect(0,0,0,0)

        self.map_pos_nd2 = nd2_getMatrix((x,y),1)



        # self.wnd_rectpos координаты привязанные к камере,
        # пересчитываются при скроллинге карты
        # имя self.rect это хардкод PYGAME, координата topleft спрайта относительно окна на карте при копировании
        # используется в pygame.draw !!!
        # self.wnd_rectpos здесь только объявлен, будет переопределен в setPos
        # self.rect и self.wnd_rectpos это просто синониы
        self.rect = self.wnd_rect = pg.Rect(0,0,Car.SPRITE_SIZE_X,Car.SPRITE_SIZE_Y)

        self.setPos(pg.Rect(x,y,0,0))

        self.image = Car.arr_img_srf[0]
        self.brezenhem = Brezenhem()
        self.is_moving = 0
        self.real_speed = 0
        self.real_direction = 0  #реальное напраывление объекта направление для спрайта
        self.rotate_direction = 0   #направление вращения 0 против часовой стрелки
        self.need_direction = 0 #куда крутимся

        self.message = message

        self.velocity = 1.0         #сколоксть начальная



        self.max_velocity = 100.0          #максимальная скорость пиксель в секунду
        self.velocity_nd2 = nd2_getMatrix((5,0),0)

        self.is_engine_on = 0
        self.is_braking_on = 0

        self.engine_acceleration_dv = 10.0   #разгон под двигателем
        self.K_friction = 0.15
        self.K_braking = 0.4


        self.course_rad = 0.0           #курс (угол)
        self.speering = 0.0             #положение руля
        self.speering_direction = 0     # -1 0 1
        self.MAX_SPEERING = grad2rad(30)           #максимальное отклонение руля
        self.SPEERING_DV = grad2rad(5)   #изменение угла на руле за 1 сек
        self.MIN_SPEERING = grad2rad(1)     #минимальное отклонение руля, если меньше него то ставим на ноль

    def setAcceleration(self,on):
        self.is_engine_on = on

    def setBreaking(self,on):
        self.is_braking_on = on

    def setSpeering(self,dir):
        # -1    налево
        # 1     направо
        self.speering_direction = dir




    def update_camera(self,camera_rect):
        self.wnd_rect.center = (self.map_rectpos.left - camera_rect.left, self.map_rectpos.top - camera_rect.top)


    def setPos(self,new_rectpos):
        self.map_rectpos = new_rectpos


    def update(self):
        # if (self.need_direction != self.real_direction):
        #
        #     #добавляем небольшой поворот
        #     self.rotate_msector_s += self.rotate_msector_v
        #
        #     if (self.rotate_msector_s >= 1000):
        #         #повернулись на 1 румб
        #         self.rotate_msector_s %= 1000   #копейки оставим на следющий румб
        #
        #         self.real_direction = self.real_direction + self.rotate_direction #поворачиваем на 1 румб
        #         self.real_direction = self.real_direction if (self.real_direction <= 31) else 0
        #         self.real_direction = self.real_direction if (self.real_direction >= 0) else 31
        #
        #         #меняем спрайт
        #         self.setDirectionImage(self.real_direction)
        #
        # else:
        #     #двигаемся
        #     if (self.brezenhem.isEnded()):
        #         self.is_moving = 0
        #     else:
        #         self.setPos(pg.Rect(self.brezenhem.nextPoint(),(0,0)))


        #пересчитаем скорость print
        dts = self.map.dt / 1000

        ###################
        print(self.speering_direction)

        #положение руля
        self.speering += self.speering_direction*self.SPEERING_DV * dts
        # if ((self.speering < self.MIN_SPEERING) ):#and (self.speering > -self.MIN_SPEERING)
        #     self.speering = 0

        #ограничим диапазон вращения руля
        self.speering = max(-self.MAX_SPEERING,min(self.speering, self.MAX_SPEERING))

        self.course_rad += self.speering * dts
        if (self.course_rad < 0):
            self.course_rad += 6.2831852
        elif (self.course_rad > 6.2831852):
            self.course_rad -= 6.2831852

        #self.course_rad = max(-self.MAX_SPEERING,min(self.speering, self.MAX_SPEERING))




        #ускорения
        #вектор ускорения совпадает с направлением машины
        engine_dv = (self.engine_acceleration_dv ) if self.is_engine_on else 0



        abs_velocity = abs(self.velocity)
        abs_friction_dv = abs_velocity if (abs_velocity < 0.2) else (abs_velocity * self.K_friction)
        friction_dv = math.copysign(abs_friction_dv,-1 if self.velocity >= 0 else 1) # знак наоборот

        if (self.is_braking_on):
            abs_braking_dv = abs_velocity if (abs_velocity < 0.9) else (abs_velocity * self.K_braking)
            braking_dv = math.copysign(abs_braking_dv,-1 if self.velocity >= 0 else 1)      # знак наоборот
        else:
            braking_dv = 0

        #прирост скорости (скаляр)
        dv = (engine_dv + braking_dv + friction_dv) * dts

        #новая скорость (скаляр)
        self.velocity = max(-self.max_velocity,min(self.max_velocity, self.velocity+dv))

        #матрица скорости c extnjvс учотом курса
        velocity_nd2 = nd2_getRotateMatrix(self.course_rad) @ nd2_getMatrix((self.velocity,0),0)


        #новое положение
        self.map_pos_nd2 = self.map_pos_nd2 + velocity_nd2 * dts

        self.map_rectpos.topleft = (self.map_pos_nd2[0], self.map_pos_nd2[1])

        self.message.sendMessage("WM_SET_SPEED", self.course_rad)


    def setTarget(self, target_rect):
        #задает цель для движения

        self.target_rect = target_rect
        self.is_moving = 1

        # координатат конца отрезка относитльно его начала
        self.brezenhem.start(self.map_rectpos.center,self.target_rect.topleft)

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
