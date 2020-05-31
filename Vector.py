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

#
# просто возвращает констанцу, размер массива
#
def nd2_getMatrixSize():
    return 3

def nd2_getPoint(nd2):
    return [nd2[0],nd2[1]]

def nd2_getPointInt(nd2):
    return [int(nd2[0]),int(nd2[1])]


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




def nd2_vector_len(a):
    return math.sqrt(a[0] ** 2 + a[1] ** 2)

#Нормализовать вектор
def nd2_normalize(a):
    len = math.sqrt(a[0] ** 2 + a[1] ** 2)
    a[0] = a[0] / len
    a[1] = a[1] / len
    return a


#
# угол поворта вектора относительно оси X
# дает только положительные значения
#
def nd2_getAngle(a):
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


#вектор минус вектор
def nd2_minus(v1,v2):
    return [
        v1[0]-v2[0],
        v1[1]-v2[1],
        v1[2]-v2[2]]


def nd2_getLinesIntersectPoint(a1,b1,c1,a2,b2,c2):
    #ищет точку пересечения двух прямых
    # a1, b1, c1 -общее уравение прямой

    #ВНИМАНИЕ. Если прямые парралельны то мы получим деление на ноль !!!!!
    # прверяем заранее
    #


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

    D = d2_deterD2(matrix_D)
    Dx = d2_deterD2(matrix_Dx)
    Dy = d2_deterD2(matrix_Dy)
    
    return np.array((Dx / D, Dy / D ,1))


#
# проверяет что два вектора коллинеарны
# считаем модуль произведения векторов
#
def nd2_getVectorLen4VectorsMult(v1,v2):
    # print(type(v1), v1)
    # print(type(v2), v2)
    # quit()
    return v1[0] * v2[1] - v1[1] * v2[0]


#
# конвертируем две точки прямой в коефыфиценты прямой ABC (общее уранвение прямой)
#
def nd2_convert_2Points_2_LineEquationABC(p1,p2):
    # 1я точка прямой -p1 соотвтетствует [x1,y1]
    # 2я точка прямой -p2 соотвтетствует [x2,y2]

    A = p2[1] - p1[1]       # y2-y1
    B = p1[0] - p2[0]       # x1-x2
    C = p1[0]*(p1[1]-p2[1]) + p1[1]*(p2[0]-p1[0])   #x1(y1-y2) + y1(x2-x1)

    return (A,B,C)



def isLinesIntersect(start1, end1, start2, end2):
    vector1 = (end2[0] - start2[0]) * (start1[1] - start2[1]) - (end2[1] - start2[1]) * (start1[0] - start2[0])
    vector2 = (end2[0] - start2[0]) * (end1[1] - start2[1]) - (end2[1] - start2[1]) * (end1[0] - start2[0])
    vector3 = (end1[0] - start1[0]) * (start2[1] - start1[1]) - (end1[1] - start1[1]) * (start2[0] - start1[0])
    vector4 = (end1[0] - start1[0]) * (end2[1] - start1[1]) - (end1[1] - start1[1]) * (end2[0] - start1[0])
    return (vector1 * vector2 <= 0) and (vector3 * vector4 <= 0)

####################################################


def d2_plus(p1,p2):
    return [p1[0]+p2[0],p1[1]+p2[1]]


def d2_minus(p1,p2):
    return [p1[0]-p2[0],p1[1]-p2[1]]

def d2_minusAndInc(p1,p2):
    return [p1[0]-p2[0]+1,p1[1]-p2[1]+1]




def d2_getInt(p1):
    return [int(p1[0]),int(p1[1])]

def d2_zero():
    return [0,0]

def d2_one():
    return [1,1]


#детерминант матрицы
def d2_deterD2(a):
    return a[0, 0] * a[1, 1] - a[0, 1] * a[1, 0]

def signFloat(f):
    return (1 if (f > 1e-6) else (-1 if (f < -1e-6) else 0))


#расстояние между двумя точками

def d2_caclDistance2Points(p1,p2):
    return math.sqrt(((p1[0]-p2[0]) ** 2) + ((p1[1]-p2[1]) ** 2))


