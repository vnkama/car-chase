import math
import sys


def HRGB(hex):    #hex_rgb
    return [(hex & 0xFF0000) >> 16, (hex & 0xFF00) >> 8 ,hex & 0xFF]

def grad2rad(grad):
    return grad * 0.0174532922

def rad2grad(grad):
    return grad * 57.29578049

# def f2i(f):
#     return int(round(f))

PI=3.1415926535
PI_m2 = PI*2
PI_d2 = PI/2

# D2_0 = [0,0]
# D2_1 = [1,1]




g_main_game = None
# g_conrol_wnd = None


########################################
def getAppWnd():
    global g_main_game
    return g_main_game

def setMainWnd(main_wnd):
    global g_main_game
    g_main_game = main_wnd

# def getFrames():
#     return getAppWnd().Series.frames

########################################
# def getControlWnd():
#     global g_conrol_wnd
#     return g_conrol_wnd
#
# def setControlWnd(conrol_wnd):
#     global g_conrol_wnd
#     g_conrol_wnd = conrol_wnd




def calcAbsToOffset(base_point_xy,point_xy):
    # base_point_xy координаты опорной точки
    # point_abs координаты точки
    # получим координатфы точки относилььно опорной
    return (point_xy[0] - base_point_xy[0],point_xy[1] - base_point_xy[1])

def calcPointMinusPoint(p1_xy,p2_xy):
    return (p1_xy[0] - p2_xy[0],p1_xy[1] - p2_xy[1])




def offsetPoint(point_xy,offset_xy):
    return (point_xy[0]+offset_xy[0],point_xy[1]+offset_xy[1])



def getPointDistanse_Float(point_xy):
    #дистанция до точки от 0,0
    return math.sqrt(point_xy[0] * point_xy[0] + point_xy[1] * point_xy[1])



def quit(text=''):
    print("\033[31mcalled by QUIT() *********************************************")
    if (len(text)):
        print(f"\033[31m{text}\033[0m")

    sys.exit()