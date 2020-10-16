import pygame as pg
import math

class Brezenhem:

    direction_16_srf = pg.image.load("./images/direct-16-512.png").convert()

    def __init__(self):
        self.x1,self.y1 = 0,0
        self.x2,self.y2 = 0,0
        self.x, self.y  = 0,0
        self.Clear()

    def Clear(self):
        self.Len_float = None
        self.Len_mpx = None
        self.sprite_direction_16 = None


    def start(self, point1, point2):
        self.Clear()

        self.x1 = point1[0]
        self.y1 = point1[1]
        self.x2 = point2[0]
        self.y2 = point2[1]


        #в самомо брезенхеме не применяются, но бывают нужны в других алгоритмах
        self.dx = self.x2 - self.x1
        self.dy = self.y2 - self.y1


        #dx dy - не меняются в процесе работы брезенхема
        # self.abs_dx = self.x2 - self.x1
        # self.abs_dy = self.y2 - self.y1

        self.sign_x = 1 if self.dx > 0 else -1 if self.dx < 0 else 0
        self.sign_y = 1 if self.dy > 0 else -1 if self.dy < 0 else 0

        # if self.dx < 0: self.dx = -self.dx
        # if self.dy < 0: self.dy = -self.dy

        self.abs_dx =  self.dx if self.dx > 0 else -self.dx
        self.abs_dy =  self.dy if self.dy > 0 else -self.dy


        if self.abs_dx > self.abs_dy:
            self.pdx, self.pdy = self.sign_x, 0
            self.es, self.el = self.abs_dy, self.abs_dx
        else:
            self.pdx, self.pdy = 0, self.sign_y
            self.es, self.el = self.abs_dx, self.abs_dy

        self.x, self.y = self.x1, self.y1
        self.error  = self.el / 2
        self.t = 0





    #-------------------------------------------------------------------
    #
    def nextPoint(self):
        # при первом вызове после start() возвращает ккординаты следующей после x1,y1 точки
        # x1,y1  - НЕ возвращает
        #
        # при каждом последующем вызове возвращает пару x,y для следующей точки линии

        if self.t < self.el:
            self.error -= self.es
            if self.error < 0:
                self.error += self.el
                self.x += self.sign_x
                self.y += self.sign_y
            else:
                self.x += self.pdx
                self.y += self.pdy
            self.t += 1

        return (self.x, self.y)


    def isEnded(self):
        #возаращет 1 если мы достигли конца
        return 1 if self.x == self.x2 and self.y == self.y2 else 0


    #-------------------------------------------------------------------
    #
    def getLen_float(self):
        # длинна отрезка
        # это гипотенуза, как если бы линейкой померяли
        # это не физическое число пикселй, оно почти всегда меньше

        if (self.Len_float is None):
            self.Len_float = math.sqrt(self.dx * self.dx + self.dy * self.dy)

        return self.Len_float



    #-------------------------------------------------------------------
    def getLen_mpx(self):
        if (self.Len_mpx is None):
            self.Len_mpx = int(self.getLen_float() * 1000)

        return self.Len_mpx



    #-------------------------------------------------------------------
    def getSpriteDirection32(self):
        #

        vector = [self.abs_dx,self.abs_dy]

        if (self.abs_dx == 0):
            #чтобы избежать деления на ноль пр ирасчете тангенса
            if (self.abs_dy >=0):
                direction = 15  #строго вниз
            else:
                direction = 0   #строго вверх
        else:
            #определяем направление спрайта в пределах 1го квадранта
            direction = int(math.atan(self.abs_dy / self.abs_dx) * 5.095 + 0.5)

            #пересчитаем в 4 разных квадранта
            if (self.dx < 0 and  self.dy > 0):
                direction = 16 - direction

            elif (self.dx < 0 and self.dy < 0):
                direction += 16

            elif (self.dx >= 0 and self.dy < 0):
                direction = (32 - direction) & 0x1F

        return direction

    def getSpriteDirection16(self):
        #возвращает напрвление спрайта по вектору движения, 16 возможных направлений

        if (self.sprite_direction_16 is not None):
            return self.sprite_direction_16

        vector = [self.abs_dx,self.abs_dy]


        max_size = max(vector[0], vector[1])

        while (max_size > 512):
            vector[0] >>=  1
            vector[1] >>=  1
            max_size = max(abs(vector[0]), abs(vector[1]))

        direction_clr = Brezenhem.direction_16_srf.get_at((vector[0], vector[1]))[0:3]


        if (direction_clr[0:3] == (0,0,0)):
            direction = 4
        elif (direction_clr[0:3] == (48,0,0)):
            direction = 3
        elif (direction_clr[0:3] == (0,48,0)):
            direction = 2
        elif (direction_clr[0:3] == (0,0,48)):
            direction = 1
        elif (direction_clr[0:3] == (48,48,48)):
            direction = 0
        else:
            direction = None

        if (direction is not None):
            if (self.dx < 0 and  self.dy > 0):
                direction = 8 - direction

            elif (self.dx < 0 and self.dy < 0):
                direction += 8

            elif (self.dx >= 0 and self.dy < 0):
                direction = (16 - direction) & 0xF

        return direction


