import pygame as pg     #использован pg.Rect

# =================================================================================
# количесвто особей в поколении
GAME_GENE_SIZE  = 100

# максимальное количесвто поколений
GAME_GENE_COUNT_MAX = 500



# =================================================================================


FPS_RATE=60                             # частота кадров в сек 60

#интервал пересчета UPDATE, внутриигровое время (механика)
# MECH_UPDATE_INTERVAL_MS        = 16
MECH_UPDATE_INTERVAL_MS_F    = 16.6666667



# интервал обработки HANDLE_EVENTS
STATE_TRAINING_PLAY__HANDLE_EVENTS_INTERVAL_MS = 16
STATE_TRAINING_PLAY__UPDATE_INTERVAL_MS = 16
STATE_TRAINING_PLAY__DRAW_INTERVAL_MS = 16



MAIN_WND_TITLE = 'Car chase'  # имя главного окна
MAIN_WND_FULLSCREEN = 0
MAIN_WND_BACKGROUND = 0x682828  # debug

if MAIN_WND_FULLSCREEN:
    MAIN_WND_HEIGHT     = 900             # для фулл скрин
    MAIN_WND_WIDTH      = 1600
else:
    MAIN_WND_HEIGHT     = 768               #768(в окне win)   # размер определен спрайтом зелени 128 * 6 = 768
    MAIN_WND_WIDTH      = 1400              #1400(в окне win)



#размер игровой карты (НЕ экрана)
MAP_SIZE_X = 2560
MAP_SIZE_Y = 896
MAP_SIZE_XY = (MAP_SIZE_X, MAP_SIZE_Y)
MAP_SIZE_RECT = pg.Rect(0, 0, MAP_SIZE_X, MAP_SIZE_Y)

MAP_TAIL_SIZE_X   = 20          # 20 * 128 = 2560
MAP_TAIL_SIZE_Y    = 7          # 6 * 128 = 768 (в окне win),        7 * 128 = 960

THEME_RED_CLR                   = 0xFB0D1C
THEME_GREEN_CLR                 = 0x2AC325
THEME_BLUE_CLR                  = 0x426DF9
THEME_GREY_CLR                  = 0x282828

THEME_BORDER_COLOR_LOW          = 0x4f4f4f
THEME_BORDER_COLOR_HIGH         = 0xe7e7e7
THEME_BACKGROUND_CLR            = THEME_GREY_CLR
THEME_BACKGROUND_HOVER_COLOR    = 0x1A1A1A
THEME_FONT_CLR                  = 0xe7e7e7
THEME_FONT_DISABLED_CLR         = 0x606060
THEME_FONT                      = "arial_20"

THEME_BUTTON_BACKGROUND         = THEME_GREY_CLR
THEME_BUTTON_BACKGROUND_HOVER   = 0x1A1A1A
THEME_BUTTON_BORDER_COLOR       = 0xe7e7e7
THEME_BUTTON_BORDER_DISABLED_COLOR = 0x606060

THEME_SEMAPHOR_GREY             = THEME_GREY_CLR
THEME_SEMAPHOR_GREEN            = 0x10F010
THEME_SEMAPHOR_RED              = 0xE01010


THEME_COMBOBOX_BACKGROUND       = 0x1C1C1C
THEME_COMBOBOX_BACKGROUND_HOVER = 0x101010
THEME_COMBOBOX_BORDER_COLOR     = THEME_GREY_CLR
THEME_COMBOBOX_STRING_HEIGHT    = 22


# THEME_WINDOW_BACKGROUND     = THEME_GREY_CLR



TOOL_WND_WIDTH       = 300
TOOL_WND_RECT        = pg.Rect(MAIN_WND_WIDTH-TOOL_WND_WIDTH, 0, TOOL_WND_WIDTH, MAIN_WND_HEIGHT)   #left top w h
# CONTROL_WND_BACKGROUND  = THEME_GREY_CLR
TOOL_WND_FONT_SIZE   = 20
# THEME_FONT_CLR  = 0xe7e7e7              # цвет шрифта на контролах
# CONTROL_WND_FONT_DISABLED_COLOR  = THEME_BUTTON_BORDER_DISABLED_COLOR


MAP_WND_RECT            = pg.Rect(0,0,MAIN_WND_WIDTH - TOOL_WND_WIDTH,MAIN_WND_HEIGHT) #left top w h
MAP_WND_BACKGROUND      = 0x682848


CONSOLE_CLR_ERROR   = "\033[35m\033[1m"
CONSOLE_CLR_RED     = "\033[31m\033[1m"
CONSOLE_CLR_GREEN   = "\033[32m\033[1m"
CONSOLE_CLR_RESET   = "\033[0m"

#=================================================================================