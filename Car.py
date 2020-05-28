import pygame as pg
from config import *
from fw.functions import *
from Vector import *
import math
from fRect import *


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

    SENSOR_COUNT = 5
    SENSOR_MAX_LEN = 500       # максимальная длинна сенсора

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

        self.velocity = 0.0         #сколоксть начальная



        self.max_velocity = 100.0          #максимальная скорость пиксель в секунду
        #self.velocity_nd2 = nd2_getMatrix((5,0),0)

        self.CAR_LEN = 70           #длинна машины , точнее расстояние между осями

        self.is_engine_on = 0
        self.engine_acceleration_dv = 10.0   #разгон под двигателем

        self.is_braking_on = 0
        self.K_braking = 0.4


        self.K_friction = 0.05          #коефициент торможения (об воздузх :)



        self.course_nd2 = nd2_getMatrix((1,0))  #матрица курса
        self.speering_wheel_alfa = 0.0          #положение руля     0-прямой

        self.speering_direction = 0     # -1 0 1 куда крутим руль
        self.MAX_SPEERING = grad2rad(30)           #максимальное отклонение руля
        self.SPEERING_DV = grad2rad(12)   #изменение угла на руле за 1 сек
        self.MIN_SPEERING = grad2rad(1)     #минимальное отклонение руля, если меньше него то ставим на ноль

        self.init_sensors()


    def init_sensors(self):

        #углы положения сенсоров
        self.arr_sensors_angles = [
            grad2rad(-90),
            grad2rad(-45),
            grad2rad(0),
            grad2rad(45),
            grad2rad(90),
        ]

        #значения сенсоров
        self.arr_sensors_value = np.zeros(5,float)

        self.arr_sensors_car_pos = np.empty(shape=[Car.SENSOR_COUNT],dtype = object)       #координаты относительно машины (константа), при курсе 0
        self.arr_nd2_sensors_map_pos = np.zeros(shape=(Car.SENSOR_COUNT,nd2_getMatrixSize()),dtype = float)       #координаты относительно карты, с учетом курса
        self.arr_sensors_wnd_pos = np.empty(shape=[Car.SENSOR_COUNT],dtype = list)         #координаты относительно окна

        #расчитаем координаты сенсоров , относительно машины
        # курс не учитываем
        for ai,v in np.ndenumerate(self.arr_sensors_angles):
            i=ai[0]
            #формируем вектор от центра машины на сенсор.
            self.arr_sensors_car_pos[i] = nd2_getScaleMatrix(Car.SENSOR_MAX_LEN) @ nd2_getRotateMatrix(v) @ nd2_getMatrix([1,0])





    def setAcceleration(self,on):
        self.is_engine_on = on



    def setBreaking(self,on):
        self.is_braking_on = on



    def setSpeering(self,dir):
        # -1    налево
        # 1     направо
        self.speering_direction = dir




    def update_camera(self,camera_rect):

        # положение автомобиля в окне
        self.wnd_rect.center = (self.map_rectpos.left - camera_rect.left, self.map_rectpos.top - camera_rect.top)

        # #пересчитаем положение сенсоров в окне
        for i in range(Car.SENSOR_COUNT):
            self.arr_sensors_wnd_pos[i] = (
                int(self.arr_nd2_sensors_map_pos[i][0]) - camera_rect.left,
                int(self.arr_nd2_sensors_map_pos[i][1]) - camera_rect.top
            )



    def setPos(self,new_rectpos):
        self.map_rectpos = new_rectpos


    def update(self):
        #print("update")
        self.update_movement()
        self.update_sensors()

    def update_movement(self):
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


        #положение руля
        self.speering_wheel_alfa += self.speering_direction*self.SPEERING_DV * dts

        #ограничим диапазон вращения руля
        self.speering_wheel_alfa = max(-self.MAX_SPEERING,min(self.speering_wheel_alfa, self.MAX_SPEERING))



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




        if (abs(self.speering_wheel_alfa) > 0.001):
            #движение по дуге

            #радиус поворота, скаляр
            #берем положительное значение тк скаляр
            R_turn = self.CAR_LEN / math.tan(abs(self.speering_wheel_alfa))

            #положение заднего колеса (оно идет по дуге поворота)
            back_wheel_nd2 = nd2_getScaleMatrix(self.CAR_LEN/2) @ (nd2_getRotateMatrix180() @ self.course_nd2)

            #вектор от заднего колеса на центр дуги , по которй едет машина
            #вектор перпендикулярен курсу машины
            if (self.speering_wheel_alfa > 0):
                R_turn_back_nd2 =  nd2_getScaleMatrix(R_turn) @ (nd2_getRotateMatrixRight90() @ self.course_nd2)
            else:
                R_turn_back_nd2 =  nd2_getScaleMatrix(R_turn) @ (nd2_getRotateMatrixLeft90() @ self.course_nd2)


            #центр дуги , по которй едет машина
            centr_turn_nd2 = back_wheel_nd2 + R_turn_back_nd2


            #угловой пробег (скаляр). (угол из центра вращения (centr_turn_nd2) на машину в начале и конце шага
            d_alfa = math.copysign((self.velocity * dts) / R_turn,self.speering_wheel_alfa)

            #матрица поворота
            rotateMatrix_nd2 = nd2_getRotateMatrix(d_alfa)
            self.map_pos_nd2 =  self.map_pos_nd2 + centr_turn_nd2 + rotateMatrix_nd2 @ nd2_getRotateMatrix180() @ centr_turn_nd2

            #пересчитаем курс
            self.course_nd2 = nd2_normalize(rotateMatrix_nd2 @ self.course_nd2)

        else:
             #движение по прямой
             self.map_pos_nd2 = self.map_pos_nd2 + (self.velocity * dts) * self.course_nd2

        angle = np2_getAngle(self.course_nd2)
        rumb_angle = PI / 16        # = 2 * PI / 32

        self.setDirectionImage((int ((angle + rumb_angle / 2) / rumb_angle)) & 0x1F)


        #новое положение
        #
        self.map_rectpos.topleft = (int(self.map_pos_nd2[0]), int(self.map_pos_nd2[1]))







    #
    #
    #
    def update_sensors(self):
        #print("update_sensors")

        rotate_nd2 = nd2_getRotateMatrix(np2_getAngle(self.course_nd2))
        for ai,sensor_car_pos in np.ndenumerate(self.arr_sensors_car_pos):
            i=ai[0]
            #повернем сенсор по курсу машины и разместим на карте
            self.arr_nd2_sensors_map_pos[i] = rotate_nd2 @ sensor_car_pos + self.map_pos_nd2


        ############################################################
        #
        # определим прмоугольник (его края парралелны карте) в который попадают все сенcоры (сенсор - это отрезок)


        arr_x = self.arr_nd2_sensors_map_pos[...,0]
        arr_y = self.arr_nd2_sensors_map_pos[...,1]

        x1 = np.amin(arr_x)
        x2 = np.amax(arr_x)
        y1 = np.amin(arr_y)
        y2 = np.amax(arr_y)

        all_sensors_map_rect = pg.Rect(x1,y1,x2-x1+1,y2-y1+1)



        ######################################################
        #
        #составим спсико спрайтов краев дороги, которые попадают (втч частично) в sensors_rect
        #с этими спрайтами в дальнейшем буди искать пересечения
        #
        counter1 = 0
        lst_curbs_4_all_sensors = []

        for sprite_curb in self.map.arr_sprites_curbs:
            if (all_sensors_map_rect.colliderect(sprite_curb.map_rect)):
                counter1 += 1
                lst_curbs_4_all_sensors.append(sprite_curb)

        # print("**")
        # print(f"all_sensors_map_rect {all_sensors_map_rect}")
        # for sprite_curb in lst_curbs_4_all_sensors:
        #     print(sprite_curb.map_rect)



        # для каждого сенсора найдем спрайты краев дорог которые возможно пересекаются с сенсором
        # пересечение ищем по rect-rect

        #инициируем массив пустыми листами
        arr_sensors_lst_curbs = np.empty(shape=[Car.SENSOR_COUNT],dtype=list)
        for i in range(arr_sensors_lst_curbs.size):
            arr_sensors_lst_curbs[i] = []


        test = np.full(shape=[Car.SENSOR_COUNT],fill_value=0,dtype = int)

        #sensor_rect = pg.Rect(0,0,0,0)

        car_rect = pg.Rect(
            nd2_getPoint(self.map_pos_nd2),
            (1,1)
        )


        for sensor_i in range(Car.SENSOR_COUNT):

            sensor_rect = car_rect.union(
                pg.Rect(
                    nd2_getPoint(self.arr_nd2_sensors_map_pos[sensor_i]),
                    (1,1)
                )
            )

            #print(sensor_rect)

            # пересечем sensor_rect с прмоугольниками curbs

            for sprite_curb in lst_curbs_4_all_sensors:
                if (sensor_rect.colliderect(sprite_curb.map_rect)):
                    arr_sensors_lst_curbs[sensor_i].append(sprite_curb)
                    test[sensor_i] += 1




        sss = str(test[0]) + ' ' + str(test[1]) + ' ' + str(test[2]) + ' ' + str(test[3]) + ' ' + str(test[4])
        self.message.sendMessage("WM_SET_PARAM_1", f"{sss}" )



    #
    #
    #
    # def draw(self,surface):
    #     print("draw")
    #     super().draw()
    #     self.draw_sensors()

    def draw_sensors(self):

        for ai,sensor_wnd_pos in np.ndenumerate(self.arr_sensors_wnd_pos):
            i=ai[0] #индекс


            pg.draw.line(
                self.map.surface,
                (255,0,128,128),
                self.wnd_rect.center,
                sensor_wnd_pos,
                1
            )



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
