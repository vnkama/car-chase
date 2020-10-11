import pygame as pg
import numpy as np
from config import *
from fw.functions import *
from Vector import *

from fw.fwMapWnd import fwMapWnd
from Tile import *
from Car import *
from Camera import *

import random





#
# окно с картой
#
class MapWnd(fwMapWnd):

    def __init__(self,params):


        params['rect'] = MAP_WND_RECT
        params['background_color'] = MAP_WND_BACKGROUND
        params['name'] = 'MapWnd'

        super().__init__(params)        # parent - fwWindow

        self.control_wnd = params['control_wnd']    #для вывода ссобщений

        self.background_srf = pg.Surface(MAP_SIZE_XY)
        self.Camera = Camera(MAP_WND_RECT.width,MAP_WND_RECT.height,MAP_SIZE_X,MAP_SIZE_Y)
        self.dt = 0


        #группы спрайтов
        self.arr_sprites_update_camera = pg.sprite.Group()
        self.arr_sprites_draw = pg.sprite.Group()           # для взывова draw, карта отдельно копируемся
        self.arr_sprites_update = pg.sprite.Group()         # то что двигаетсмя
        self.arr_sprites_collide = pg.sprite.Group()        # прверяиьт на столкновения с автомобилем
        self.arr_sprites_curbs = pg.sprite.Group()


        #тайловая карта
        #тайлы двух видов, определяются случайно
        #тайлы спрайтами не являются, а копируеются один раз прямо на фон
        for x in range(MAP_TAIL_SIZE_X):
            for y in range(MAP_TAIL_SIZE_Y):
                #номер типа тайла случайно
                rand = random.randint(0, 1)
                dest_rect = pg.Rect(
                    Tile.SPRITE_SIZE_X * x,
                    Tile.SPRITE_SIZE_Y * y,
                    Tile.SPRITE_SIZE_X,
                    Tile.SPRITE_SIZE_Y)

                Tile.copyImg(self.background_srf, dest_rect, rand)



        #нарисуем деревья

        self.arr_trees = []
        groups = (self.arr_sprites_update_camera, self.arr_sprites_draw, self.arr_sprites_collide)

        self.arr_trees.append(
            Tree(100, 100, groups)
        )

        self.arr_trees.append(
            Tree(500, 600, groups)
        )

        self.arr_trees.append(
            Tree(1000, 150, groups)
        )

        self.arr_trees.append(
            Tree(1500, 180, groups)
        )


        self.arr_oils = []
        groups = (self.arr_sprites_update_camera, self.arr_sprites_draw)
        self.arr_oils.append(
            Oil(400, 400, groups)
        )

        self.arr_rocks = []
        groups = (self.arr_sprites_update_camera,self.arr_sprites_update, self.arr_sprites_draw)
        self.arr_rocks.append(
            Rock(600, 400, groups)
        )




        #формирует дорогу
        self.init_road()

        self.arr_cars = []
        self.newGame()

        getAppWnd().registerHandler_MOUSEBUTTONDOWN(self)
        getAppWnd().registerHandler_KEYDOWN(self)
        getAppWnd().registerHandler_KEYUP(self)



    def init_road(self):


        arr_roadsections_axial_2idot =  np.array(
            [
                [0, 300],
                [300, 300],
                [350, 280],
                [400, 200],
                [500, 130],

                [600, 100],
                [700, 100],
                [800, 130],
                [900, 200],
                [1000, 300],

                [1100, 320],
                [1200, 420],
                [1300, 490],
                [1400, 520],
                [1500, 520],

                [1600, 480],
                [1760, 300],
                [1840, 260],
                [2000, 240],
                [2100, 240],

                [2250, 270],
            ],
            int
        )

        arr_roadsections_width_i =  np.array(
            [
                150,
                150,
                150,
                150,
                150,

                150,
                150,
                150,
                150,
                150,

                150,
                150,
                150,
                120,
                100,

                100,
                100,
                120,
                150,
                150,

                150
            ],
            int
        )


        road_len = len(arr_roadsections_axial_2idot)
        #road_len = 7


        #вектора-координаты 2d [x y 1] на повороты осевая линия дороги
        #индексы 0..road_len

        arr_roadsections_axial_turn_3mfdot = np.zeros((road_len,3),float)
        for i in range(road_len): #
            arr_roadsections_axial_turn_3mfdot[i] = nd2_getMatrix(arr_roadsections_axial_2idot[i])


        #секция дороги в виде прямоугольника (НЕ полигона !). 4 угла
        arr_P = np.zeros((road_len-1,4,3),float)


        #нормальные вектора левого-правого краев дороги

        arr_A_left = np.zeros((road_len-1),float)
        arr_B_left = np.zeros((road_len-1),float)
        arr_C_left = np.zeros((road_len-1),float)

        arr_A_right = np.zeros((road_len-1),float)
        arr_B_right = np.zeros((road_len-1),float)
        arr_C_right = np.zeros((road_len-1),float)



        # матрицы поворота
        matrix_rotate_left = nd2_getRotateMatrixLeft90()
        matrix_rotate_right = nd2_getRotateMatrixRight90()


        arr_roadsections_corners_3mf = np.zeros((road_len-1,4,3),float)

                            #вектора-направляения [x y 0], это направления участков дороги.
                            #направления из точки [road_len] нет - некуда направлять
                            #arr_roadsections_direction = np.zeros((road_len-1,3),float)
        for i in range(road_len-1):
            # вектора-направляения [x y 0], направления участков дороги, считается вдоль осевой.
            roadsection_axis_3mf = arr_roadsections_axial_turn_3mfdot[i+1] - arr_roadsections_axial_turn_3mfdot[i]

            #коеффициент масштабирования
            #ширина дороги в начале и конце секции разная
            k_width_begin = arr_roadsections_width_i[i] / (2 * nd2_vector_len(roadsection_axis_3mf))
            k_width_end = arr_roadsections_width_i[i+1] / (2 * nd2_vector_len(roadsection_axis_3mf))

            #матрица масштабирования начала и конца секции
            matrix_scaling_begin = nd2_getScaleMatrix(k_width_begin)
            matrix_scaling_end = nd2_getScaleMatrix(k_width_end)

            #масшиабируем вектор направления до нужной длины
            roadsection_direction_begin = matrix_scaling_begin @ roadsection_axis_3mf
            roadsection_direction_end = matrix_scaling_end @ roadsection_axis_3mf

            #arr_P координаты 4х углов секции. прямоугольный формат секции
            #0 - начало секции левый
            #1 - конец секции левый
            #2 - конец секции правый
            #3 - начало секции правый

            # углы
            arr_P[i][0] = arr_roadsections_axial_turn_3mfdot[i] + matrix_rotate_left @ roadsection_direction_begin
            arr_P[i][1] = arr_roadsections_axial_turn_3mfdot[i+1] + matrix_rotate_left @ roadsection_direction_end
            arr_P[i][2] = arr_roadsections_axial_turn_3mfdot[i+1] + matrix_rotate_right @ roadsection_direction_end
            arr_P[i][3] = arr_roadsections_axial_turn_3mfdot[i] + matrix_rotate_right @ roadsection_direction_begin

            #нормальные вектора левого-правого краев дороги
            # края дороги могут быть непарралельны осевой
            N_left = matrix_rotate_left @ (arr_P[i][1] - arr_P[i][0])
            N_right = matrix_rotate_right @ (arr_P[i][2] - arr_P[i][3])

            #считаем общее уравнение прямой для левого-правого краев дороги
            #общее уравнение прямой для края дороги
            # a*x1 + b*y1 + c1 = 0
            # a = Nx, берем из нормального вектора
            # b = Ny, берем из нормального вектора
            # c = -(a x1  + b y1)       x1 y1 - любая точка через которую проходит прямая

            arr_A_left[i] = N_left[0]
            arr_B_left[i] = N_left[1]
            arr_C_left[i] = -(arr_A_left[i] * arr_P[i][0][0] +  arr_B_left[i] * arr_P[i][0][1])

            arr_A_right[i] = N_right[0]
            arr_B_right[i] = N_right[1]
            arr_C_right[i] = -(arr_A_right[i] * arr_P[i][3][0] +  arr_B_right[i] * arr_P[i][3][1])



        #просчитаем все реальные углы
        #в последней секции не просчитываем
        for i in range(road_len - 1):

            if (i == 0):
                # в 0й сейкции, реальные 0й и 3й углы совпадают с прямоугольными, тк. "минус первой" секции не сущесвует
                arr_roadsections_corners_3mf[i][0] = arr_P[i][0]
                arr_roadsections_corners_3mf[i][3] = arr_P[i][3]
            else:
                #все секции кроме нулевой, копируют 0й 3й углы с предыдущей секции, т.к. они совпадают
                arr_roadsections_corners_3mf[i][0] = arr_roadsections_corners_3mf[i-1][1]
                arr_roadsections_corners_3mf[i][3] = arr_roadsections_corners_3mf[i-1][2]

            if (i == (road_len - 2)):
                # в последней сейкции, реальные 1й и 2й углы совпадают с прямоугольными, тк. "после последней " секции не сущесвует
                arr_roadsections_corners_3mf[road_len - 2][1] = arr_P[road_len - 2][1]
                arr_roadsections_corners_3mf[road_len - 2][2] = arr_P[road_len - 2][2]

            else:
                #считаем реальные 1й 2й углы секции
                # continue
                # 1й угол

                arr_roadsections_corners_3mf[i][1] = nd2_getLinesIntersectPoint(
                    arr_A_left[i], arr_B_left[i], arr_C_left[i],
                    arr_A_left[i+1], arr_B_left[i+1], arr_C_left[i+1]
                )

                arr_roadsections_corners_3mf[i][2] = nd2_getLinesIntersectPoint(
                    arr_A_right[i], arr_B_right[i], arr_C_right[i],
                    arr_A_right[i+1], arr_B_right[i+1], arr_C_right[i+1]
                )




        self.arr_road_sprites = []

        #рисуем полигоны на дороге

        for i in range(road_len - 1):
            #for arr_roadsection in arr_roadsections_corners_3mf:
            arr_roadsection = arr_roadsections_corners_3mf[i]
            #цикл для каждого 4х угольного полигона дороги
            #arr_roadsection - содержит 4 угла полигона

            polygon_corners = []

            for corner_xy in arr_roadsection:
                polygon_corners.append((int(corner_xy[0]),int(corner_xy[1])))

            pg.draw.polygon(
                    self.background_srf,
                    (20, 20, 220),
                    polygon_corners
                )

            groups = (self.arr_sprites_update_camera, self.arr_sprites_draw,self.arr_sprites_curbs)


            #ставим спрайт на левую сторону дороги
            self.arr_road_sprites.append(
                Curb(
                    arr_roadsection[0],
                    arr_roadsection[1],
                    (arr_A_left[i], arr_B_left[i], arr_C_left[i]),
                    groups
                )
            )

            #ставим спрайт на правую сторону дороги
            self.arr_road_sprites.append(
                Curb(
                    arr_roadsection[2],
                    arr_roadsection[3],
                    (arr_A_right[i], arr_B_right[i], arr_C_right[i]),
                    groups
                )
            )

    #
    #
    #
    # def sendMessage(self, msg, param1=None, param2=None):
    #     if (msg == 'WM_NEW_GAME'):
    #         self.newGame

    #начало новой игры (нажата кнопка new)
    def newGame(self):

        if (len(self.arr_cars)):
            self.arr_cars[0].kill()
            del (self.arr_cars[0])

        groups = (self.arr_sprites_update_camera,self.arr_sprites_update, self.arr_sprites_draw)
        self.arr_cars.append(
            Car(self,0, 300, groups, self.control_wnd)
        )


    def update(self):
        # self.updateChildWnds()    #у карты нет чайлдов
        self.arr_sprites_update.update()
        self.update_camera()


    def update_camera(self):
        self.Camera.update(self.arr_cars[0].map_rectpos)

        # координаты окна показываемые камерой относительно карты
        camera_position_rect = self.Camera.getPositionRect()

        # пересчитываем координаты в спрайтах с учетом камеры
        for sprite in self.arr_sprites_update_camera:
            sprite.update_camera(camera_position_rect)


    def drawThis(self):

        #копируем карту тайлов
        #self.drawBackground()       #оригинальная родная заливка фона -

        #координаты окна показываемые камерой относительно карты
        camera_position_rect = self.Camera.getPositionRect()

        #копируем фон(тайловая карта)
        self.surface.blit(          # копируем в окно MapWnd
            self.background_srf,    # копируем из карты
            pg.Rect(0,0,0,0),       # копируем на все окно MapWnd
            camera_position_rect)   # из карты берем то что показывает камера


        self.arr_cars[0].draw_sensors()
        self.arr_sprites_draw.draw(self.surface)

        # столкновение машины с краем дороги
        sprite_lst = pg.sprite.spritecollide(
            self.arr_cars[0],           #машину сталикиваем
            self.arr_sprites_curbs,      #с краями дороги
            False,
            pg.sprite.collide_mask
        )

        if (sprite_lst):
            self.arr_oils[0].kill()
            #print("ROAD !!")

        sprite_lst = pg.sprite.spritecollide(
            self.arr_cars[0],           #машину сталикиваем
            self.arr_sprites_collide,    #
            False,
            pg.sprite.collide_mask
        )

        if (sprite_lst):
            sprite_lst[0].kill()
            print("TOUCH !!")


    def handle_MOUSEBUTTONDOWN(self,event):
        if (event.button == 1):
            # нажата левая кнопка

            if (self.isPointInWindow(event.pos)):
                #кнопка нажата в зоне карты


                #абсолютные координаты мыши -> в относительные в окне
                # event.pos - абсолютные кордингаты клика относительно онка приложения
                # click_mapwnd_rect - координаты относительна окна mapwnd
                click_mapwnd_rect = pg.Rect(
                    calcAbsToOffset(self.surface.get_abs_offset(),event.pos),
                    (0,0)
                )

                # координаты окна показываемые камерой относительно карты
                camera_position_rect = self.Camera.getPositionRect()

                #координаты клика относительно карты
                click_map_rect =  camera_position_rect.move(click_mapwnd_rect.topleft)

                #self.arr_cars[0].setTarget(click_map_rect)



    def handle_KEYDOWN(self,event):
        if (event.key == pg.K_LEFT):
            self.arr_cars[0].setSpeering(-1)

        elif (event.key == pg.K_RIGHT):
            self.arr_cars[0].setSpeering(1)

        elif (event.key == pg.K_UP):
            self.arr_cars[0].setAcceleration(1)

        elif (event.key == pg.K_DOWN):
            self.arr_cars[0].setBreaking(1)



    def handle_KEYUP(self,event):
        if (event.key == pg.K_LEFT):
            self.arr_cars[0].setSpeering(0)

        elif (event.key == pg.K_RIGHT):
            self.arr_cars[0].setSpeering(0)

        elif (event.key == pg.K_UP):
            self.arr_cars[0].setAcceleration(0)

        elif (event.key == pg.K_DOWN):
            self.arr_cars[0].setBreaking(0)


    #
    #
    #
    def sendMessage(self, msg, param1=None,param2=None):
        # if (msg == 'WM_NEW_GAME'):
        #     self.newGame()
        #
        # elif (msg == 'WM_QUIT'):
        #     pass
        #
        # elif (msg == 'WM_UPDATE'):
        #     pass
        #
        # else:
        #     # если не обработали здесь то отправляем наверх
        super().sendMessage(msg, param1, param2)

