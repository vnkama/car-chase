import math
import numpy as np
from fw.functions import *

# class Vector2d:
#     def __init__(self, x=0, y=0):
#         self.x, self.y = x, y
#
#
#     def summ_v(self,vector_b):
#         pass
#
#     def scalar_mult(self,vector_b):
#         pass
#
#     #угол между векторами
#     def angle(self,vb):
#         retrun (self.x * vb.x + self.y * vb.y) / (sqrt(self.x ** 2 + self.y ** 2) * sqrt(vb.x ** 2 + vb.y ** 2))
#
#     def len(self):
#         return sqrt(self.x ** 2 + self.y ** 2)


#
# префикс vector_ означает что операци веждутся над координатами вида [x,y]
# это НЕ pygame.Rect !!

#преобразует вектор к радиус-вектору
def vector_getRadiusVector(begin,end):
    return [end[0]-begin[0],end[1]-begin[1]]




#угол между векторами
def vector2_calcAngle(a,b):
    return (a[0] * b[0] + a[1] * b[1]) / (math.sqrt(a[0] ** 2 + a[1] ** 2) * math.sqrt(b[0] ** 2 + b[1] ** 2))

###########################################

#w=1 координата
#w=0 направление
def nd2_getMatrix(pos,w=0):
    return np.array(
        [
            pos[0],
            pos[1],
            w,
        ],
        float)


#матрица масштабирвания 2D
def nd2_getScaleMatrix(k):
    return np.array(
        [
            [k, 0, 0],
            [0, k, 0],
            [0, 0, 1],
        ],
        float)

#матрица поворот
def nd2_getRotateMatrix(alfa_rad):
    cos_alfa = math.cos(alfa_rad)
    sin_alfa = math.sin(alfa_rad)
    return np.array(
        [
            [cos_alfa,     -sin_alfa,     0],
            [sin_alfa,     cos_alfa,      0],
            [0,     0,      1],
        ],
        float)

#матрица поворот 180
def nd2_getRotateMatrix180():
    return np.array(
        [
            [-1,     0,     0],
            [0,     -1,      0],
            [0,     0,      1],
        ],
        float)



#поворотная матрица поворот на 90 по часовой стрелки (ось Y на экране вниз)
def nd2_getRotateMatrixRight90():
    return np.array(
        [
            [0,     -1,     0],
            [1,     0,      0],
            [0,     0,      1],
        ],
        float)


#поворотная матрица поворот на 90 против часовой стрелки (ось Y на экране вниз)
def nd2_getRotateMatrixLeft90():
    return np.array(
        [
            [0,     1,      0],
            [-1,    0,      0],
            [0,     0,      1],
        ],
        float)


#детерминант матрицы
def np2_detD2(a):
    return a[0, 0] * a[1, 1] - a[0, 1] * a[1, 0]

def np_vector2_len(a):
    return math.sqrt(a[0] ** 2 + a[1] ** 2)

#Нормализовать вектор
def np2_normalize(a):
    len = math.sqrt(a[0] ** 2 + a[1] ** 2)
    a[0] = a[0] / len
    a[1] = a[1] / len
    return a


#
# угол поворта вектора относительно оси X
# дает только положительные значения
#
def np2_getAngle(a):
    if (abs(a[0]) < 0.0000001):
        #x=0
        return (PI_d2) if a[1] > 0 else -(PI_d2)
    else:
        if (a[0] >= 0):
            if (a[1] >= 0):
                return math.atan(a[1] / a[0])
            else:
                #(a[1] < 0):
                return PI_m2 + math.atan(a[1] / a[0])
        else:
            if (a[1] >= 0):
                return PI  + math.atan(a[1] / a[0])
            else:
                #(a[1] < 0):
                return PI  + math.atan(a[1] / a[0])


#=========================================================
def np_d2_getLinesIntersectPoint(a1,b1,c1,a2,b2,c2):
    #ищет точку пересечения двух прямых
    # a1, b1, c1 -уравнение прямой в общем виде

    #print(a1,b1,c1,a2,b2,c2)

    matrix_D = np.array([
        [a1, b1],
        [a2, b2],
    ])

    matrix_Dx = np.array([
        [-c1, b1],
        [-c2, b2],
    ])

    matrix_Dy = np.array([
        [a1, -c1],
        [a2, -c2],
    ])

    D = np2_detD2(matrix_D)
    Dx = np2_detD2(matrix_Dx)
    Dy = np2_detD2(matrix_Dy)
    
    return [Dx / D, Dy / D ,1]







