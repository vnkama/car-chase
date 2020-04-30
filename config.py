import pygame

FPS_RATE=30                             #частота кадров в сек       60
MAIN_WND_TITLE      ='Car chase'  #имя главного окна
MAIN_WND_HEIGHT     = 768   # размер определен спрайтом зелени 128 * 6 = 768
MAIN_WND_WIDTH      = 1400  #


MAIN_WND_BACKGROUND = 0x682828      #debug


THEME_BORDER_COLOR_LOW          = 0x4f4f4f
THEME_BORDER_COLOR_HIGH         = 0xe7e7e7
THEME_BACKGROUND_COLOR          = 0x282828
THEME_BACKGROUND_HOVER_COLOR    = 0x1A1A1A


CONTROL_WND_WIDTH       = 300
CONTROL_WND_RECT        = pygame.Rect(MAIN_WND_WIDTH-CONTROL_WND_WIDTH,0,CONTROL_WND_WIDTH,MAIN_WND_HEIGHT)   #left top w h
CONTROL_WND_BACKGROUND          = 0x282828
#CONTROL_WND_BACKGROUND_HOVER    = 0x242424
CONTROL_WND_FONT_SIZE   = 20
CONTROL_WND_FONT_COLOR  = 0xe7e7e7


MAP_WND_RECT            = pygame.Rect(0,0,MAIN_WND_WIDTH - CONTROL_WND_WIDTH,MAIN_WND_HEIGHT) #left top w h
MAP_WND_BACKGROUND      = 0x682848






