import pygame as pg     #использован pg.Rect


FPS_RATE=60                             #частота кадров в сек 60
MAIN_WND_TITLE      ='Car chase'        #имя главного окна
MAIN_WND_HEIGHT     = 896               #768(в окне win)   # размер определен спрайтом зелени 128 * 6 = 768
MAIN_WND_WIDTH      = 1600              #1400(в окне win)
MAIN_WND_BACKGROUND = 0x682828          #debug

#размер игровой карты (НЕ экрана)
MAP_SIZE_X = 2560
MAP_SIZE_Y = 896
MAP_SIZE_XY = (MAP_SIZE_X,MAP_SIZE_Y)
MAP_SIZE_RECT = pg.Rect(0,0,MAP_SIZE_X,MAP_SIZE_Y)

MAP_TAIL_SIZE_X   = 20          # 20 * 128 = 2560
MAP_TAIL_SIZE_Y    = 7          # 6 * 128 = 768 (в окне win),        7 * 128 = 960

THEME_BORDER_COLOR_LOW          = 0x4f4f4f
THEME_BORDER_COLOR_HIGH         = 0xe7e7e7
THEME_BACKGROUND_COLOR          = 0x282828
THEME_BACKGROUND_HOVER_COLOR    = 0x1A1A1A


CONTROL_WND_WIDTH       = 300
CONTROL_WND_RECT        = pg.Rect(MAIN_WND_WIDTH-CONTROL_WND_WIDTH,0,CONTROL_WND_WIDTH,MAIN_WND_HEIGHT)   #left top w h
CONTROL_WND_BACKGROUND  = 0x282828
CONTROL_WND_FONT_SIZE   = 20
CONTROL_WND_FONT_COLOR  = 0xe7e7e7


MAP_WND_RECT            = pg.Rect(0,0,MAIN_WND_WIDTH - CONTROL_WND_WIDTH,MAIN_WND_HEIGHT) #left top w h
MAP_WND_BACKGROUND      = 0x682848


ERROR_CONSOLE_COLOR = "\033[35m\033[1m"



