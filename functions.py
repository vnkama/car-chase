import math

def HRGB(hex):    #hex_rgb
    return [(hex & 0xFF0000) >> 16, (hex & 0xFF00) >> 8 ,hex & 0xFF]


g_arr_fonts = {}
g_main_game = None

def setFonts(arr_fonts):
    global g_arr_fonts
    g_arr_fonts = arr_fonts

def getFont(name):
    global g_arr_fonts
    return g_arr_fonts.get(name.lower(), g_arr_fonts['tahoma_20'])

def getMainWnd():
    global g_main_game
    return g_main_game

def setMainWnd(main_wnd):
    global g_main_game
    g_main_game = main_wnd



def calcAbsToOffset(base_point_xy,point_xy):
    # base_point_xy координаты опорной точки
    # point_abs координаты точки
    # получим координатфы точки относилььно опорной
    return (point_xy[0] - base_point_xy[0],point_xy[1] - base_point_xy[1])


def offsetPoint(point_xy,offset_xy):
    return (point_xy[0]+offset_xy[0],point_xy[1]+offset_xy[1])



def getPointDistanse_Float(point_xy):
    #дистанция до точки от 0,0
    return math.sqrt(point_xy[0] * point_xy[0] + point_xy[1] * point_xy[1])



