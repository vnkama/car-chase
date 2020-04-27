import pygame as pg
from Cell import *
from config import *




class CellOvalis(Cell):
    WEED_SIZE = (64,64)

    sprites_srf = []

    for i in range(0,16):
        file_name = "./images/ovalis-64-{:02d}.png".format(i)
        srf = pg.image.load(file_name).convert_alpha()
        sprites_srf.append(srf)

    max_speed       = 120      #максимальная скорость
#    max_speed_in_drift = 2     #максмальная скорость в дрифте (не соблюдая направление, можно плыть боком)
    #max_speed_in_rotate = 5   #максимальная скорость в повороте, на более выскоких скоростях, движение только прямо

#    max_rotate_speed = ((0,1),(5,2),(60,4),(90,0))       # кривая : (скорость движения, скорость поворота)

    rotate_speed__mturn_sec = 1000     # 1000 соответсвует 1 оборот в секеунду, 2000- два оборота в секунду итп

    #скорость вращения: милли сектор в тик
    # на эту переменную увеличивается счечтк вращения каждый тик FPS
    # как только наберется 1000 , то спрайт поворачивается на 1/16
    rotate_msector_v = rotate_speed__mturn_sec * 16 // FPS_RATE




    def __init__(self,params):
        super().__init__(params)
        self.image = CellOvalis.sprites_srf[0]



    def setPos(self,pos):
        self.centr_pos = pos
        self.rect = pg.Rect(offsetPoint(pos,(-(CellOvalis.WEED_SIZE[0]/2),-(CellOvalis.WEED_SIZE[1]/2))), CellOvalis.WEED_SIZE)

    def setDirectionImage(self,direction):
        self.image = CellOvalis.sprites_srf[direction]


    def update(self):
        if (self.need_direction != self.real_direction):

            #добавляем небольшой поворот
            self.rotate_msector_s += self.rotate_msector_v

            if (self.rotate_msector_s >= 1000):
                #повернулись на 1 румб
                self.rotate_msector_s %= 1000   #копейки оставим на следющий румб

                self.real_direction = (self.real_direction + self.rotate_direction) #поворачиваем на 1 румб
                self.real_direction = self.real_direction if (self.real_direction <= 15) else 0
                self.real_direction = self.real_direction if (self.real_direction >= 0) else 15

                #меняем спрайт
                self.setDirectionImage(self.real_direction)

        else:
            #двигаемся 22
            if (self.brezenhem.isEnded()):
                self.is_moving = 0
                return

            self.setPos(self.brezenhem.nextPoint())

            if (self.brezenhem.isEnded()):
                self.is_moving = 0








