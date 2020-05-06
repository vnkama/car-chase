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
            Tree(700, 200, arr_groups)
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

        for section in self.arr_roadsections_corners:

            polygon_points = []
            for point in section:
                polygon_points.append((int(point[0]),int(point[1])))

            pg.draw.polygon(
                    self.background_srf,
                    (20, 20, 220),
                    polygon_points
                )

        getMainWnd().registerHandler_MOUSEBUTTONDOWN(self)
        getMainWnd().registerHandler_KEYDOWN(self)
        getMainWnd().registerHandler_KEYUP(self)



    def init_road(self):

        self.arr_roadsections_axial_points =  np.array(
            [
                [0, 200],
                [100, 100],
                [150, 100],
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
                140,
                140,
                140,
            ],
            int
        )


        road_len = len(self.arr_roadsections_axial_points)



        #вектора-координаты 2d [x y 1] на повороты осевая линия дороги
        #индексы 0..road_len
        arr_roadsections_axial_turn_coords = np.zeros((road_len,3),int)
        for i in range(road_len): #
            arr_roadsections_axial_turn_coords[i] = np_d2_getMatrix(self.arr_roadsections_axial_points[i])


        #секция дороги в прмяоугольном виде. 4 угла
        arr_P = np.zeros((road_len-1,4,3),float)


        #нормальные вектора левого-правого краев дороги

        arr_N_left = np.zeros((road_len-1,3),float)
        arr_A_left = np.zeros((road_len-1),float)
        arr_B_left = np.zeros((road_len-1),float)
        arr_C_left = np.zeros((road_len-1),float)

        arr_N_right = np.zeros((road_len-1,3),float)
        arr_A_right = np.zeros((road_len-1),float)
        arr_B_right = np.zeros((road_len-1),float)
        arr_C_right = np.zeros((road_len-1),float)



        # матрицы поворота
        matrix_rotate_left = np_d2_getRotateMatrixLeft90()
        matrix_rotate_right = np_d2_getRotateMatrixRight90()

        self.arr_roadsections_corners = np.zeros((road_len-1,4,3),float)

                            #вектора-направляения [x y 0], это направления участков дороги.
                            #направления из точки [road_len] нет - некуда направлять
                            #arr_roadsections_direction = np.zeros((road_len-1,3),float)
        for i in range(road_len-1):
            # вектора-направляения [x y 0], направления участков дороги, считается вдоль осевой.
            roadsectin_axis_vector = arr_roadsections_axial_turn_coords[i+1] - arr_roadsections_axial_turn_coords[i]

            #коеффициент масштабирования
            #ширина дороги в начале и конце секции разная
            k_width_begin = arr_roadsections_width[i] / (2 * np_vector2_len(roadsectin_axis_vector))
            k_width_end = arr_roadsections_width[i+1] / (2 * np_vector2_len(roadsectin_axis_vector))

            #матрица масштабирования начала и конца секции
            matrix_scaling_begin = np_d2_getScaleMatrix(k_width_begin)
            matrix_scaling_end = np_d2_getScaleMatrix(k_width_end)

            #масшиабируем вектор направления до нужной длины
            roadsection_direction_begin = matrix_scaling_begin @ roadsectin_axis_vector
            roadsection_direction_end = matrix_scaling_end @ roadsectin_axis_vector

            #arr_P координаты 4х углов секции. прямоугольный формат секции
            #0 - начало секции левый
            #1 - конец секции левый
            #2 - конец секции правый
            #3 - начало секции правый

            #self - убрать TODO
            # углы
            arr_P[i][0] = arr_roadsections_axial_turn_coords[i] + matrix_rotate_left @ roadsection_direction_begin
            arr_P[i][1] = arr_roadsections_axial_turn_coords[i+1] + matrix_rotate_left @ roadsection_direction_end
            arr_P[i][2] = arr_roadsections_axial_turn_coords[i+1] + matrix_rotate_right @ roadsection_direction_end
            arr_P[i][3] = arr_roadsections_axial_turn_coords[i] + matrix_rotate_right @ roadsection_direction_begin

            #нормальные вектора левого-правого краев дороги
            # края дороги могут быть непаррадедльны осевой
            N_left = matrix_rotate_left @ (arr_P[i][1] - arr_P[i][0])
            N_right = matrix_rotate_right @ (arr_P[i][2] - arr_P[i][3])

            #считаем общее уравнение прямой для левого-правого краев дороги
            #общее уравнение прямой для края дороги
            # a*x1 + b*y1 + c1 = 0
            # a = Nx, берем из нормального вектора
            # b = Ny, берем из нормального вектора
            # c = -(a x1  + b y1)       x1 y1 - любая точка через которую проходит прямая

            # print(i,arr_N_left[i])
            # a = arr_N_left[i][0]
            # arr_A_left[i]=a

            arr_A_left[i] = N_left[0]
            arr_B_left[i] = N_left[1]
            arr_C_left[i] = -(arr_A_left[i] * arr_P[i][0][0] +  arr_B_left[i] * arr_P[i][0][1])

            arr_A_right[i] = N_right[0]
            arr_B_right[i] = N_right[1]
            arr_C_right[i] = -(arr_A_right[i] * arr_P[i][3][0] +  arr_B_right[i] * arr_P[i][3][1])

        self.arr_roadsections_corners = arr_P

        #просчитаем все реальные углы
        #в последней секции не просчитываем
        for i in range(road_len - 1):
        #     #print(self.arr_roadsections_corners)
        #
            if (i == 0):
                # в 0й сейкции, реальные 0й и 3й углы совпадают с прямоугольными, тк. "минус первой" секции не сущесвует
                self.arr_roadsections_corners[i][0] = arr_P[i][0]
                self.arr_roadsections_corners[i][3] = arr_P[i][3]
            else:
                #все секции кроме нулевой, копируют 0й 3й углы с предыдущей секции, т.к. они совпадают
                self.arr_roadsections_corners[i][0] = self.arr_roadsections_corners[i-1][1]
                self.arr_roadsections_corners[i][3] = self.arr_roadsections_corners[i-1][2]

            if (i == (road_len - 2)):
                # в последней сейкции, реальные 1й и 2й углы совпадают с прямоугольными, тк. "после последней " секции не сущесвует
                self.arr_roadsections_corners[road_len - 2][1] = arr_P[road_len - 2][1]
                self.arr_roadsections_corners[road_len - 2][2] = arr_P[road_len - 2][2]
            else:
                #pass
                #считаем реальные 1й 2й углы секции
                # self.arr_roadsections_corners[i][1] = arr_P[i][1]
                # self.arr_roadsections_corners[i][2] = arr_P[i][2]
                # continue
                # 1й угол

                 self.arr_roadsections_corners[i][1] = np_d2_getLinesIntersectPoint(
                     arr_A_left[i], arr_B_left[i], arr_C_left[i],
                     arr_A_left[i+1], arr_B_left[i+1], arr_C_left[i+1]
                 )

                 self.arr_roadsections_corners[i][2] = np_d2_getLinesIntersectPoint(
                     arr_A_right[i], arr_B_right[i], arr_C_right[i],arr_A_right[i+1], arr_B_right[i+1], arr_C_right[i+1]
                 )

        print(self.arr_roadsections_corners)








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

        # prev_pos = None
        # for i,point_desc in enumerate(self.arr_roadsections_axial_points):
        #     cur_pos = point_desc
        #
        #     if (i != 0 ):
        #         pg.draw.line(
        #             self.surface,
        #             (180,80,80),             #цивет
        #             prev_pos,
        #             cur_pos,
        #             2
        #         )
        #     prev_pos = cur_pos
        #
        # for roadsection_corners in self.arr_roadsection_corners:
        #
        #     points = (
        #         (int(roadsection_corners[0][0]),int(roadsection_corners[0][1])),
        #         (int(roadsection_corners[1][0]),int(roadsection_corners[1][1])),
        #         (int(roadsection_corners[2][0]),int(roadsection_corners[2][1])),
        #         (int(roadsection_corners[3][0]),int(roadsection_corners[3][1])),
        #     )
        #
        #
        #     pg.draw.polygon(
        #         self.surface,
        #         (20, 20, 220),
        #         points
        #     )
        #
        #     for corner in range(4):
        #         pg.draw.circle(
        #             self.surface,
        #             (80, 80, 180),
        #             (int(roadsection_corners[corner][0]),int(roadsection_corners[corner][1])),
        #             2
        #         )





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
