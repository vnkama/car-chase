import math
import numpy as np

class Vector2d:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y


    def summ_v(self,vector_b):
        pass

    def scalar_mult(self,vector_b):
        pass

    #угол между векторами
    def angle(self,vb):
        retrun (self.x * vb.x + self.y * vb.y) / (sqrt(self.x ** 2 + self.y ** 2) * sqrt(vb.x ** 2 + vb.y ** 2))

    def len(self):
        return sqrt(self.x ** 2 + self.y ** 2)


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

def np_d2_getMatrix(pos,w=0):
    return np.array(
        [
            pos[0],
            pos[1],
            w,
        ],
        float)


#матрица масштабирвания 2D
def np_d2_getScaleMatrix(k):
    return np.array(
        [
            [k, 0, 0],
            [0, k, 0],
            [0, 0, 1],
        ],
        float)


#поворотная матрица поворот на 90 по часовой стрелки (ось Y на экране вниз)
def np_d2_getRotateMatrixRight90():
    return np.array(
        [
            [0,     -1,     0],
            [1,     0,      0],
            [0,     0,      1],
        ],
        float)


#поворотная матрица поворот на 90 против часовой стрелки (ось Y на экране вниз)
def np_d2_getRotateMatrixLeft90():
    return np.array(
        [
            [0,     1,      0],
            [-1,    0,      0],
            [0,     0,      1],
        ],
        float)


def np_vector2_len(a):
    return math.sqrt(a[0] ** 2 + a[1] ** 2)




