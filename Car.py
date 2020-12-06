import pygame as pg
from config import *
from fw.functions import *
from Vector import *
import math
from fRect import *
from Brezenhem import Brezenhem
from fw.neural_network import FeedForwardNetwork
import numpy as np




#
#
#
class Car(pg.sprite.Sprite):

    CAR_RED = 2
    CAR_GREEN = 1

    SPRITE_SIZE_X = 80
    SPRITE_SIZE_Y = 80
    SPRITE_SIZE_XY = (SPRITE_SIZE_X, SPRITE_SIZE_Y)

    #SENSORS_COUNT = 5
    SENSOR_MAX_LEN = 500       # максимальная длинна сенсора


    # скорость машины - 1
    # текущее положение руля - 1
    # сенсоры - SENSORS_COUNT = 5
    # итого входов : 7
    #NN_INPUTS_COUNT = SENSORS_COUNT + 2

    # выходы SPEERING - воздействие на руль !!! не положение на руль а воздействие на него,
    # ACCELERATOR / BRAKE - газ /тормоз
    # итого 2 выхода
    #NN_OUTPUTS_COUNT = 2

#    NN_HIDDEN_LAYERS_SIZE = [5, 4]    # скрытые слои нейросети





    arr_img_srf = []

    # скорость вращения,
    # 1000 соответсвует 1 оборот в секеунду, 2000- два оборота в секунду итп
    rotate_speed__mturn_sec = 1000


    # скорость вращения: милли сектор в тик
    # на эту переменную увеличивается счечтк вращения каждый тик FPS
    # как только наберется 1000 , то спрайт поворачивается на 1/16
    rotate_msector_v = rotate_speed__mturn_sec * 32 // TRAINING_UPDATE_GTIME_FPS

    for i in range(0, 32):
        file_name = "./images/car-green/car_green_3_{:02d}.png".format(i)
        srf = pg.image.load(file_name).convert_alpha()
        arr_img_srf.insert(i, srf)


    #
    #
    #
    def __init__(
            self,
            map,
            x, y,
            groups,
            message,        # куда отправлять sendMessage, скорее всего Tool_wnd
    ):


        self.arr_sensors_angles = None
        self.arr_sensors_car_pos = None
        self.arr_sensors_end_3mfdot = None
        self.arr_sensors_wnd_pos = None
        self.arr_sensors_value = None

        super().__init__(groups)

        # указатель "наверх" на карту
        self.map = map

        # self.map_rectpos координаты центра спрайта привязанные к карте, они неизменны (для неподвижных спрайтов)
        # self.map_rectpos здесь только объявлен, будет переопределен в setPos
        self.map_rectpos = pg.Rect(0, 0, 0, 0)
        self.map_pos_nd2 = nd2_getMatrix((x, y), 1)



        # self.wnd_rectpos координаты привязанные к камере,
        # пересчитываются при скроллинге карты
        # имя self.rect это хардкод PYGAME, координата topleft спрайта относительно окна на карте при копировании
        # используется в pygame.draw !!!
        # self.wnd_rect здесь только объявлен, будет переопределен в setPos
        # self.rect и self.wnd_rect это просто синониы
        self.rect = self.wnd_rect = pg.Rect(0, 0, Car.SPRITE_SIZE_X, Car.SPRITE_SIZE_Y)

        self.setPos(pg.Rect(x, y, 0, 0))

        self.image = Car.arr_img_srf[0]
        self.brezenhem = Brezenhem()
        self.is_moving = 0
        self.real_speed = 0
        self.real_direction = 0     # реальное напраывление объекта направление для спрайта
        self.rotate_direction = 0   # направление вращения 0 против часовой стрелки
        self.need_direction = 0     # куда крутимся

        self.message = message

        self.engine_power = 0               # выдается нейросетью, -100..100,
                                            # минус - задний ход, плюс - передний

        self.speed = 0.0                   # скороксть начальная
        self.max_speed = 300.0              # максимальная скорость пиксель в секунду

        self.total_S = 0                    # пробег авто за всю party

        self.CAR_LEN = 70                   # длинна машины, точнее расстояние между осями

        self.K_NN_engine_power = 100;
        # self.is_engine_on = 0
        # self.engine_acceleration_dv = 10.0  # разгон под двигателем

        self.is_braking_on = 0
        self.K_braking = 0.4


        self.K_air_friction = 0.005                 # коефициент торможения (об воздух :)       #

        self.course_nd2 = nd2_getMatrix((0.8, 0.0))  # матрица курса

        self.speering_angle_want = 0            # положение руля желаемое. (задается нейросетью)
        self.speering_angle = 0                 # положение руля фактическое


        self.speering_direction = 0         # -1 0 1 куда крутим руль
        self.MAX_SPEERING = grad2rad(30)    # максимальное отклонение руля
        self.SPEERING_DV = grad2rad(12)     # изменение угла на руле за 1 сек
        self.MIN_SPEERING = grad2rad(1)     # минимальное отклонение руля, если меньше него то ставим на ноль

        self.init_sensors()


        # Setting up network architecture
        # Each "Vision" has 3 distances it tracks: wall, apple and self
        # there are also one-hot encoded direction and one-hot encoded tail direction,
        # each of which have 4 possibilities.
        # num_inputs = SENSORS_COUNT



        # NN_structure = [NN_INPUTS_COUNT]
        # NN_structure.extend(Car.NN_HIDDEN_LAYERS_SIZE)
        # NN_structure.append(Car.NN_OUTPUTS_COUNT)
        # NN_structure имеет вид [20,10,5,2]
        # 20 - число входов, 2 число выходов, 10, 5 скрытые слои

        self.NN = FeedForwardNetwork(NN_STRUCTURE)


    def init_sensors(self):

        # углы положения сенсоров
        self.arr_sensors_angles = [
            grad2rad(-90),
            grad2rad(-45),
            grad2rad(0),
            grad2rad(45),
            grad2rad(90),
        ]

        # значения сенсоров - 0.0
        self.arr_sensors_value = np.zeros(shape=(CAR_SENSORS_COUNT, 1), dtype=float)

        # координаты относительно машины (константа), при курсе 0
        self.arr_sensors_car_pos = np.empty(shape=[CAR_SENSORS_COUNT], dtype=object, )

        # координаты относительно карты, с учетом курса
        self.arr_sensors_end_3mfdot = np.zeros(
                shape=(CAR_SENSORS_COUNT, nd2_getMatrixSize()),
                dtype=float
        )

        # координаты относительно окна
        self.arr_sensors_wnd_pos = np.empty(shape=[CAR_SENSORS_COUNT], dtype=list)

        # расчитаем координаты сенсоров , относительно машины
        # курс не учитываем
        for ai, v in np.ndenumerate(self.arr_sensors_angles):
            i = ai[0]
            # формируем вектор от центра машины на сенсор.
            self.arr_sensors_car_pos[i] = nd2_getScaleMatrix(Car.SENSOR_MAX_LEN) @ nd2_getRotateMatrix(v) @ nd2_getMatrix([1, 0])

        self.arr_sensors_value = np.full(shape=CAR_SENSORS_COUNT, dtype=float, fill_value=Car.SENSOR_MAX_LEN)


        self.setDirectionImage2()


    def setAcceleration(self, on):
        self.is_engine_on = on



    def setBreaking(self, on):
        self.is_braking_on = on



    def setSpeering(self, dir):
        # -1    налево
        # 1     направо
        self.speering_direction = dir



    def updateCamera(self, camera_rect):

        # положение автомобиля относительно окна
        self.wnd_rect.center = (self.map_rectpos.left - camera_rect.left, self.map_rectpos.top - camera_rect.top)

        # пересчитаем положение сенсоров относ  окна
        for i in range(CAR_SENSORS_COUNT):
            self.arr_sensors_wnd_pos[i] = (
                int(self.arr_sensors_end_3mfdot[i][0]) - camera_rect.left,
                int(self.arr_sensors_end_3mfdot[i][1]) - camera_rect.top
            )



    def setPos(self, new_rectpos):
        self.map_rectpos = new_rectpos



    def update(self, *args):

        if args[0] == 1:    # 1 - training
            self.update_movement()
            self.update_sensors()

        elif args[0] == 's':    # 2 - show
            pass



    def update_movement(self):

        # print('Car.update_movement')

        # формируем входные данне на нйеросеть
        # X = np.zeros(NN_INPUT_COUNTS)

        X = np.hstack((
                self.arr_sensors_value,    # сенсоры
                [self.speed],              # скорость
                [self.speering_angle],     # положение руля
        ))

        # в NN передаем X в формате именно (7,1) а не (7,)
        X = X.reshape(len(X), 1)

        (self.engine_power, self.speering_angle_want) = self.NN.feed_forward(X)

        self.engine_power *= self.K_NN_engine_power

        # self.engine_power = max(0, min(200, self.engine_power))

        self.speering_angle_want = (2 * self.speering_angle_want - 1) * self.MAX_SPEERING



        # PRINT
        self.printNNValues()


        # пересчитаем скорость
        dts = self.map.dt

        ###################


        # пересчитаем положение руля

        # разница между желаемым и реальным положением руля, с учетом знака
        delta_angle = self.speering_angle_want - self.speering_angle

        # на какой угол сколько можем повернуть руль за один кадр (без знака)
        speering_rotate_angle = self.SPEERING_DV * dts


        if abs(delta_angle) < speering_rotate_angle:
            # нужно довернуть на минимальный угол
            self.speering_angle = self.speering_angle_want

        else:
            self.speering_angle += speering_rotate_angle * np.sign(delta_angle)


        # ограничим диапазон вращения руля
        self.speering_angle = max(-self.MAX_SPEERING, min(self.speering_angle, self.MAX_SPEERING))



        # ускорения
        # вектор ускорения совпадает с направлением машины
        # engine_dv = self.engine_acceleration_dv if self.is_engine_on else 0
        engine_dv = self.engine_power

        abs_speed = abs(self.speed)

        abs_friction_dv = min(abs_speed, max(0.1, abs_speed ** 2 * self.K_air_friction))
        friction_dv = -abs_friction_dv if self.speed >= 0 else abs_friction_dv

        # тормоза пока нет
        # if self.is_braking_on:
        #     abs_braking_dv = abs_speed if (abs_speed < 0.9) else (abs_speed * self.K_braking)
        #     braking_dv = math.copysign(abs_braking_dv,-1 if self.speed >= 0 else 1)      # знак наоборот
        # else:
        #     braking_dv = 0

        # прирост скорости (скаляр)
        # dv = (engine_dv + braking_dv + friction_dv) * dts

        dv = (engine_dv + friction_dv) * dts

        # новая скорость (скаляр)
        self.speed = max(-self.max_speed, min(self.max_speed, self.speed + dv))




        if abs(self.speering_angle) > 0.001:
            # движение по дуге

            # радиус поворота, скаляр
            # берем положительное значение тк скаляр
            R_turn = self.CAR_LEN / math.tan(abs(self.speering_angle))

            # положение заднего колеса (оно идет по дуге поворота)
            back_wheel_nd2 = nd2_getScaleMatrix(self.CAR_LEN/2) @ (nd2_getRotateMatrix180() @ self.course_nd2)

            # вектор от заднего колеса на центр дуги , по которй едет машина
            # вектор перпендикулярен курсу машины
            if self.speering_angle > 0:
                R_turn_back_nd2 =  nd2_getScaleMatrix(R_turn) @ (nd2_getRotateMatrixRight90() @ self.course_nd2)
            else:
                R_turn_back_nd2 =  nd2_getScaleMatrix(R_turn) @ (nd2_getRotateMatrixLeft90() @ self.course_nd2)


            # центр дуги , по которй едет машина
            centr_turn_nd2 = back_wheel_nd2 + R_turn_back_nd2


            # угловой пробег (скаляр). (угол из центра вращения (centr_turn_nd2) на машину в начале и конце шага
            d_alfa = math.copysign((self.speed * dts) / R_turn, self.speering_angle)

            # матрица поворота
            rotateMatrix_nd2 = nd2_getRotateMatrix(d_alfa)
            self.map_pos_nd2 = self.map_pos_nd2 + centr_turn_nd2 + rotateMatrix_nd2 @ nd2_getRotateMatrix180() @ centr_turn_nd2

            # пересчитаем курс
            self.course_nd2 = nd2_normalize(rotateMatrix_nd2 @ self.course_nd2)

        else:
            # движение по прямой
            self.map_pos_nd2 = self.map_pos_nd2 + (self.speed * dts) * self.course_nd2

        self.total_S += self.speed * dts


        self.setDirectionImage2()

        # новое положение
        self.map_rectpos.topleft = (int(self.map_pos_nd2[0]), int(self.map_pos_nd2[1]))



    def setDirectionImage2(self):
        angle = nd2_getAngle(self.course_nd2)
        rumb_angle = PI / 16        # = 2 * PI / 32
        direction  = (int((angle + rumb_angle / 2) / rumb_angle)) & 0x1F
        self.image = Car.arr_img_srf[direction]

    #
    # расчет фитнесс функции
    #
    def getFitness(self):
        # self.map_pos_nd2      TRAINING_UPDATE_GTIME_FPS
        cur_dist = 1e6
        cur_i = None
        for i, point in enumerate(self.map.arr_roadsections_axial_2idot):
            dist = d2_caclDistance2Points(self.map_pos_nd2, point)
            if dist < cur_dist:
                cur_dist = dist
                cur_i = i

        return getFrames() + self.total_S * 100 + cur_i**2 * 100;


    def getMediumSpeed(self):
        return self.total_S * TRAINING_UPDATE_GTIME_FPS / getFrames()


    #
    #
    #
    def update_sensors(self):

        rotate_nd2 = nd2_getRotateMatrix(nd2_getAngle(self.course_nd2))
        for ai, sensor_car_pos in np.ndenumerate(self.arr_sensors_car_pos):
            i = ai[0]

            # повернем сенсор по курсу машины и разместим на карте
            self.arr_sensors_end_3mfdot[i] = rotate_nd2 @ sensor_car_pos + self.map_pos_nd2




        ############################################################
        #
        # определим прямоугольник (его края парралелны карте) в который попадают все сенcоры
        # (сенсор - это отрезок, имеющий конкретную длинну


        arr_x = self.arr_sensors_end_3mfdot[..., 0]
        arr_y = self.arr_sensors_end_3mfdot[..., 1]

        x1 = np.amin(arr_x)
        x2 = np.amax(arr_x)
        y1 = np.amin(arr_y)
        y2 = np.amax(arr_y)

        # arr_sensors_irect -
        # rect закрывающий ВСЕ сенсоры-отрезки разом
        # УВЕЛИЧИМ НА 2 ПИКСЕЛЯ ВО ВСЕ СТОРОНЫ чтобы убрать краевые эффекты
        # было до увеличения arr_sensors_irect = pg.Rect(x1,y1,x2-x1+1,y2-y1+1)
        arr_sensors_irect = pg.Rect(x1 - 2, y1 - 2, x2 - x1 + 3, y2 - y1 + 3)




        ######################################################

        # составим список спрайтов краев дороги, которые попадают (втч частично) в arr_sensors_irect
        # с этими спрайтами в дальнейшем будем искать пересечения
        #
        lst_curbs_4_all_sensors = []

        for sprite_curb in self.map.arr_sprites_curbs:
            if arr_sensors_irect.colliderect(sprite_curb.map_rect):
                lst_curbs_4_all_sensors.append(sprite_curb)



        # для каждого сенсора найдем все sprite_curb у которого rect Пересекается с rect которые возможно пересекаются с сенсором
        # пересечение ищем по rect-rect
        # этим мы минимизируем число спрайтов c котороыми


        # инициируем массив пустыми листами
        arr_sensors_lst_curbs = np.empty(shape=[CAR_SENSORS_COUNT], dtype=list)
        for i in range(arr_sensors_lst_curbs.size):
            arr_sensors_lst_curbs[i] = np.array([])

        test = np.full(shape=[CAR_SENSORS_COUNT], fill_value=0, dtype=int)

        # общее начало отрезков-сенсоров
        car_irectpos = pg.Rect(
            nd2_getPoint(self.map_pos_nd2),
            (1, 1)
        )

        sensor_start_point_3mf = self.map_pos_nd2

        # длинна сенсора текущая, на данный момент обхода
        # после обхода всех перечений сенсора здесь будет самое короткое значение
        arr_sensor_len_f = np.full(shape=[CAR_SENSORS_COUNT], dtype=float, fill_value=float(Car.SENSOR_MAX_LEN))




        for sensor_i in range(CAR_SENSORS_COUNT):

            # rect сенсора
            # объеденим точку начала сенсоров (внутри авто) и тотчку конца сенсора в одном рект
            sensor_irect = car_irectpos.union(
                pg.Rect(
                    nd2_getPoint(self.arr_sensors_end_3mfdot[sensor_i]),
                    (1, 1)
                )
            )

            # увеличим рект для сенсора, иначе возникают краевые эффекты
            sensor_irect.move_ip(-2, -2)
            sensor_irect.w += 4
            sensor_irect.h += 4

            sensor_leABC = None
            sensor_end_point_f2 = self.arr_sensors_end_3mfdot[sensor_i]

            # пересекем rect текущего сенсора и rect текущего curb

            for sprite_curb in lst_curbs_4_all_sensors:

                # для избежания кравеых эффектов увеличим рект спрайта во всех направлениях на 2
                curb_wrapper_irect = sprite_curb.map_rect.move(-2, -2)
                curb_wrapper_irect.w += 4
                curb_wrapper_irect.h += 4



                if not sensor_irect.colliderect(curb_wrapper_irect):
                    continue

                # пересекаются sensor_irect с curbs rect
                # пока не факт что пересекаюся сами отрезки

                curb_start_2fdot = sprite_curb.start_2fdot
                curb_end_2fdot = sprite_curb.end_2fdot




                # проверим сенсор и curb на коллинеарность

                vl = nd2_getVectorLen4VectorsMult(
                    (d2_minus(curb_start_2fdot, curb_end_2fdot)),                              # отрезок curb
                    (d2_minus(sensor_start_point_3mf, sensor_end_point_f2))   # отрезок
                )

                # если vl = 0 то сенсор и curb на коллинеарны, считаем что это
                # CASTLE ну ввобще совпадение надо проверять отдельно , но пока этот код не написан
                if abs(vl) < 1e-6:
                    continue


                # прмяые содеражащие сенсор и curb непарралельны, несовпадают и следовательно где то пересекаются
                # но это прямяые, насчет отрезков пока неясно

                # получим Общее Уравнение Прямой для обоих прямых
                # curb_leABC = nd2_convert_2Points_2_LineEquationABC(curb_start_2fdot,curb_end_2fdot)


                if sensor_leABC is None:
                    sensor_leABC = nd2_convert_2Points_2_LineEquationABC(sensor_start_point_3mf,sensor_end_point_f2)

                # найдем пересечение прямых, содержащих отрезки
                # нам известно, что прямые точно пересекаются
                # но пока не известно, пересекаются ли сами отрезки
                intersect_point_2f = nd2_getLinesIntersectPoint(
                    # curb_leABC[0],curb_leABC[1],curb_leABC[2],          # коеффиценты A B C, общего уравнения прямой Ax+Bx+C=0 для curb
                    sprite_curb.arr_lineEqualABC[0], sprite_curb.arr_lineEqualABC[1], sprite_curb.arr_lineEqualABC[2],

                    # коеффиценты A B C, общего уравнения прямой Ax+Bx+C=0 для curb
                    sensor_leABC[0], sensor_leABC[1], sensor_leABC[2],  # коеффиценты A B C, для сенсора
                )

                s1 = signFloat(intersect_point_2f[0] - curb_start_2fdot[0])
                s2 = signFloat(intersect_point_2f[0] - curb_end_2fdot[0])
                s3 = signFloat(intersect_point_2f[1] - curb_start_2fdot[1])
                s4 = signFloat(intersect_point_2f[1] - curb_end_2fdot[1])

                s5 = signFloat(intersect_point_2f[0] - sensor_start_point_3mf[0])
                s6 = signFloat(intersect_point_2f[0] - sensor_end_point_f2[0])
                s7 = signFloat(intersect_point_2f[1] - sensor_start_point_3mf[1])
                s8 = signFloat(intersect_point_2f[1] - sensor_end_point_f2[1])

                if (
                    not (
                        (abs(s1 + s2) < 2 ) and      #пары s1 s2 должны быть или с разынм занком (-1 1) или (0 0) или (1 0) или (-1 0)
                        (abs(s3 + s4) < 2 ) and      #если пари s1 s2 имееет вид (-1 -1) или (1 1) занчит отрезки не пересекаются
                        (abs(s5 + s6) < 2 ) and      # для прверки abs(s1 + s2) < 2
                        (abs(s7 + s8) < 2 )
                    )
                ):
                    # отрезки не пересекаются
                    continue

                # установлен факт пересечения сенсора с curb
                test[sensor_i] += 1

                # измерим расстояние от машины до точки пересечения
                intersect_len = d2_caclDistance2Points(intersect_point_2f,sensor_start_point_3mf)

                # если найденная точка пересечения ближе
                if intersect_len < arr_sensor_len_f[sensor_i]:
                    arr_sensor_len_f[sensor_i] = intersect_len
                    self.arr_sensors_end_3mfdot[sensor_i] = intersect_point_2f


            self.arr_sensors_value[sensor_i] = arr_sensor_len_f[sensor_i]

        # end for sensor_i ....


    def printValues(self):
        out = {}
        out['sensors'] = '{:4.0f} {:4.0f} {:4.0f} {:4.0f} {:4.0f}'.format(
            self.arr_sensors_value[0],
            self.arr_sensors_value[1],
            self.arr_sensors_value[2],
            self.arr_sensors_value[3],
            self.arr_sensors_value[4],
        )

        out['speed'] = '{:4.1f}'.format(self.speed)
        out['speering'] = '{:5.3f}'.format(self.speering_angle)


        self.message.sendMessage("WM_SET_PARAM_1", out )

    def printNNValues(self):
        self.message.sendMessage("WM_SET_NN_OUT", {
            'engine_power' : self.engine_power,
            'speering_want': self.speering_angle_want,
        });


    def draw_sensors(self):
        # print('draw_sensors')
        for ai, sensor_wnd_pos in np.ndenumerate(self.arr_sensors_wnd_pos):
            i = ai[0]  # индекс

            if sensor_wnd_pos is not None:
                pg.draw.line(
                    self.map.surface,
                    (255, 0, 128, 128),
                    self.wnd_rect.center,
                    sensor_wnd_pos,
                    1,
                )



    def setTarget(self, target_rect):
        # задает цель для движения

        self.target_rect = target_rect
        self.is_moving = 1

        # координатат конца отрезка относитльно его начала
        self.brezenhem.start(self.map_rectpos.center, self.target_rect.topleft)

        # определим желаемое направление движения
        self.need_direction = self.brezenhem.getSpriteDirection32()

        if self.need_direction != self.real_direction:
            if self.need_direction > self.real_direction:
                if self.need_direction - self.real_direction <= 16:
                    self.rotate_direction = 1
                else:
                    self.rotate_direction = -1
            else:
                if self.real_direction - self.need_direction <= 16:
                    self.rotate_direction = -1
                else:
                    self.rotate_direction = 1

        self.real_speed = 0
        self.rotate_msector_s = 0          #1000

