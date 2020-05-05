import pygame as pg
import numpy as np
from config import *
from fw.functions import *
from Vector import *

from fw.GuiWindow import GuiWindow
# from CellWeed import *
# from CellOvalis import *
from Tile import *
from Car import *
from Camera import *

import random




#
# окно с органами управления игрой
#
class MapWnd(GuiWindow):

    def __init__(self,params):

        params['rect'] = MAP_WND_RECT
        params['bg_color'] = MAP_WND_BACKGROUND
        params['name'] = 'MapWnd'


        super().__init__(params)        # parent - GuiWindow

        self.background_srf = pg.Surface(MAP_SIZE_XY)
        self.Camera = Camera(MAIN_WND_WIDTH,MAIN_WND_HEIGHT,MAP_SIZE_X,MAP_SIZE_Y)


        #группы спрайтов
        self.arr_sprites_update_camera = pg.sprite.Group()  # для взывова draw, карта отдельно копируемся
        self.arr_sprites_draw = pg.sprite.Group()           # для взывова draw, карта отдельно копируемся
        self.arr_sprites_update = pg.sprite.Group()         # то что двигаетсмя
        self.arr_sprites_collide = pg.sprite.Group()        # прверяиьт на столкновения с автомобилем


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
        arr_groups = (self.arr_sprites_update_camera, self.arr_sprites_draw, self.arr_sprites_collide)

        self.arr_trees.append(
            Tree(0, 0, arr_groups)
        )

        self.arr_trees.append(
            Tree(200, 200, arr_groups)
        )

        self.arr_trees.append(
            Tree(2045, 614, arr_groups)
        )

        self.arr_oils = []

        self.arr_oils.append(
            Oil(400, 400, (self.arr_sprites_update_camera, self.arr_sprites_draw))
        )

        self.arr_rocks = []
        self.arr_rocks.append(
            Rock(600, 400, (self.arr_sprites_update_camera,self.arr_sprites_update, self.arr_sprites_draw))
        )

        self.arr_cars = []
        self.arr_cars.append(
            Car(400, 200, (self.arr_sprites_update_camera,self.arr_sprites_update, self.arr_sprites_draw))
        )


        #формирует дорогу
        self.init_road()


        getMainWnd().registerHandler_MOUSEBUTTONDOWN(self)
        getMainWnd().registerHandler_KEYDOWN(self)
        getMainWnd().registerHandler_KEYUP(self)



    def init_road(self):

        arr_road_point = [[] * 3]

        # осевая лигния дороги
        # self.arr_road_centrum_pos = [
        #     ((0, 200), 100),
        #     ((100, 100), 100),
        #     ((200, 200), 100),
        #     ((300, 300), 100),
        #     ((350, 400), 100),
        #     ((450, 430), 100),
        #     ((550, 430), 100),
        #     ((650, 420), 100),
        #     ((680, 360), 50),
        #     ((690, 260), 50),
        # ]

        self.arr_roadsections_axial_points =  np.array(
            [
                [0, 200],
                [100, 100],
                [200, 200],
                [300, 300],
                [350, 400],

                [450, 430],
                [550, 430],
                [650, 420],
                [680, 360],
                [690, 260],
            ],
            int
        )

        arr_roadsections_width =  np.array(
            [
                100,
                100,
                100,
                100,
                100,

                100,
                100,
                100,
                100,
                100,
            ],
            int
        )


        # инициируем массив дороги
        # self.arr_road_pos - содержит по две точки , левую и правую, на каждом повороте дороги
        road_len = len(self.arr_roadsections_axial_points)



        #вектора 2d [x y 1] дорога-осевая линия-повороты
        #indexes 0..road_len
        arr_roadsections_axial_turn_coords = np.zeros((road_len,3),int)
        for i in range(road_len): #
            arr_roadsections_axial_turn_coords[i] = np_d2_getMatrix(self.arr_roadsections_axial_points[i])

            # arr_roadsections_axial_turn_coords[i][0] = self.arr_roadsections_axial_points[i][0]
            # arr_roadsections_axial_turn_coords[i][1] = self.arr_roadsections_axial_points[i][1]
            # arr_roadsections_axial_turn_coords[i][2] = 1



        #4 угла секции дороги. секция в прмяоугольном виде
        self.arr_roadsection_corners = np.zeros((road_len-1,4,3),float)



        #вектора-направляения [x y 0], это направления участков дороги.
        #направления в точке [road_len] нет - некуда направлять
        arr_roadsections_direction = np.zeros((road_len-1,3),float)
        for i in range(road_len-1):
            arr_roadsections_direction[i] = arr_roadsections_axial_turn_coords[i+1] - arr_roadsections_axial_turn_coords[i]

            #масштабируем вектор направления
            #ширина дороги в начале и конце секции разная
            k_width_begin = arr_roadsections_width[i] / (2 * np_vector2_len(arr_roadsections_direction[i]))
            k_width_end = arr_roadsections_width[i+1] / (2 * np_vector2_len(arr_roadsections_direction[i]))

            #матрица масштабирования начала и конца секции
            matrix_scaling_begin = np_d2_getScaleMatrix(k_width_begin)
            matrix_scaling_end = np_d2_getScaleMatrix(k_width_end)

            #матрицы поворота
            matrix_rotate_left = np_d2_getRotateMatrixLeft90()
            matrix_rotate_right = np_d2_getRotateMatrixRight90()

            #масшиабируем вектор направления
            roadsections_direction_begin = matrix_scaling_begin @ arr_roadsections_direction[i]
            roadsections_direction_end = matrix_scaling_end @ arr_roadsections_direction[i]



            #вектора углов секции. прямоугольный формат
            #0 - начало секции левый
            #1 - конец секции левый
            #2 - конец секции правый
            #3 - начало секции правый

            # print(matrix_rotate_left)
            # print(roadsections_direction_begin)
            # a =  matrix_rotate_left @ roadsections_direction_begin


            self.arr_roadsection_corners[i][0] = arr_roadsections_axial_turn_coords[i]   + matrix_rotate_left    @ roadsections_direction_begin
            self.arr_roadsection_corners[i][1] = arr_roadsections_axial_turn_coords[i+1] + matrix_rotate_left    @ roadsections_direction_end
            self.arr_roadsection_corners[i][2] = arr_roadsections_axial_turn_coords[i+1]   + matrix_rotate_right   @ roadsections_direction_end
            self.arr_roadsection_corners[i][3] = arr_roadsections_axial_turn_coords[i] + matrix_rotate_right   @ roadsections_direction_begin


            # print(i,k_width)
            # print(arr_roadsections_direction[i])
            # print(arr_roadsections_direction[i],"\r\n")



        #координаты углов дорожных секций




            # пустой массив
        # 1й индекс порядковый номер поворота от начала дороги, этот индекс ссответствует индексу в self.arr_road_centrum_pos
        # 2й индекс, 0-левая сторна дороги, 1-правая сторона дороги
        # 3й индекс, 0-x, 1-y, собственно координаты точки
        #self.arr_road_pos = np.zeros((road_len, 2, 2), int)




        # вектора по оси дороги
        arr_roadsection_vector = np.zeros((road_len, 2), int)
        arr_central_angle = np.zeros((road_len, 2), float)

        # радиус векторы идут по оси дороги, 0й вектор из 0й точки
        # из последней точки радиус-вектора нет (т.к. некуда вести)
        # for i in range(road_len - 1):
        #     arr_roadsection_vector[i] = vector_getRadiusVector(self.arr_road_centrum_pos[i][0],
        #                                                        self.arr_road_centrum_pos[i + 1][0])

            # if (i != 0):
            #     arr_central_angle[i-1] = vector_calcAngle(arr_central_vector[i],arr_central_vector[i-1])
            #     print(i,arr_central_angle[i])

        # углы поворота дороги, на сколько поворачивается дорга на каждом повороте





    def update(self):
        self.Camera.update()



    def draw_this(self):
        #копируем карту тайлов
        #self.drawBackground()       #оригинальная родная заливка фона -

        #координаты окна показываемые камерой относительно карты
        camera_position_rect = self.Camera.getPositionRect()

        #копируем фон(тайловая карта)
        self.surface.blit(          # копируем в окно MapWnd
            self.background_srf,    # копируем из карты
            pg.Rect(0,0,0,0),       # копируем на все окно MapWnd
            camera_position_rect)   # из карты берем то что показывает камера

        #пересчитываем координаты в спрайтах с учетом камеры
        for sprite in self.arr_sprites_update_camera:
            sprite.update_camera(camera_position_rect)

        self.arr_sprites_update.update()

        sprite_lst = pg.sprite.spritecollide(
            self.arr_cars[0],           #машину сталикиваем
            self.arr_sprites_collide,    #
            False,
            pg.sprite.collide_mask
        )

        prev_pos = None
        for i,point_desc in enumerate(self.arr_roadsections_axial_points):
            cur_pos = point_desc

            if (i != 0 ):
                pg.draw.line(
                    self.surface,
                    (180,80,80),             #цивет
                    prev_pos,
                    cur_pos,
                    2
                )
            prev_pos = cur_pos

        for roadsection_corners in self.arr_roadsection_corners:

            points = (
                (int(roadsection_corners[0][0]),int(roadsection_corners[0][1])),
                (int(roadsection_corners[1][0]),int(roadsection_corners[1][1])),
                (int(roadsection_corners[2][0]),int(roadsection_corners[2][1])),
                (int(roadsection_corners[3][0]),int(roadsection_corners[3][1])),
            )


            pg.draw.polygon(
                self.surface,
                (20, 20, 220),
                points
            )

            for corner in range(4):
                pg.draw.circle(
                    self.surface,
                    (80, 80, 180),
                    (int(roadsection_corners[corner][0]),int(roadsection_corners[corner][1])),
                    2
                )





        # prev = None
        # for point_desc in self.arr_road_centrum_line:
        #     pos = point_desc[0]
        #     if (prev != None ):
        #         pg.draw.line(
        #             self.surface,
        #             (80,80,80),             #цивет
        #             (prev[0],prev[1]),
        #             (pos[0],pos[1]),
        #             1
        #         )
        #     prev = point




        # if (sprite_lst):
        #     sprite_lst[0].kill()
        #     print("TOUCH !!")

        self.arr_sprites_draw.draw(self.surface)


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

                self.arr_cars[0].setTarget(click_map_rect)


    def handle_KEYDOWN(self,event):
        if (event.key == pg.K_LEFT):
            self.Camera.moveLeft()



        elif (event.key == pg.K_RIGHT):
            self.Camera.moveRight()



    def handle_KEYUP(self,event):
        if (event.key == pg.K_LEFT):
            self.Camera.moveStop()

        elif (event.key == pg.K_RIGHT):
            self.Camera.moveStop()
