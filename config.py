import pygame as pg     # использован pg.Rect

# party         один запуск авто от начала движения до кончины авто
# generation    одно поколение, состоит из нескольких Party, в конце поколения пересчитываются нейросети
# Series        несколько поколений

# training      режим обучения, машинка едет под управлением нейросети
# show          показ процесса обучения в записи

# =================================================================================


# rtime - реальное время. используется для например для синхронизации FPS или опрса клавиатуры
# gtime - это внутриигровое время, по сюжету игра может длится хоть 10 часов, а на компьютере прошло 5 минут
# dt - временной интервал
# постфиксы
# _ms     милисекунды,
# _sec    секунды
# _f      флоат, аремя с плавающей точкой


#srf        surface



# =================================================================================
# количесвто особей в поколении
#GAME_GENE_SIZE  = 100

# максимальное количесвто поколений
#GAME_GENE_COUNT_MAX = 500

###################################
# размер популяции (колво партий)
POPULATION_SIZE = 30

# размер популяции переходящий в следующее поколение
INDIVIDS_ALIVE_COUNT = int(POPULATION_SIZE / 2)
INDIVIDS_CHILD_COUNT = POPULATION_SIZE - INDIVIDS_ALIVE_COUNT

# максимальное кол-во поколений в серии
GENE_MAX_COUNT = 50

# начальное значение генератора случайных чисел
RND_START_VALUE = 1000

# =================================================================================

CAR_START_X = 0
CAR_START_Y = 400

# =================================================================================

# на паузе update - не вызывается, handel_events вызывается вместе с draw
TRAINING_PAUSE_HANDLE_EVENTS_FPS = 60
TRAINING_PAUSE_UPDATE_FPS = 1000            # update на данный момент не вызывается на паузе
TRAINING_PAUSE_DRAW_FPS = 60

TRAINING_PLAY_HANDLE_EVENTS_FPS = 60
# TRAINING_PLAY_UPDATE_FPS = 60             #
# TRAINING_PLAY_DRAW_FPS = 60               # fps берется с select

SHOW_PAUSE_HANDLE_EVENTS_FPS = 60
SHOW_PAUSE_UPDATE_FPS = 1000
SHOW_PAUSE_DRAW_FPS = 60

SHOW_PLAY_HANDLE_EVENTS_FPS = 30
SHOW_PLAY_UPDATE_FPS = 60                   # base
SHOW_PLAY_DRAW_FPS = 60                     # base



#########




#интервал пересчета UPDATE, внутриигровое время (механика)


TRAINING_UPDATE_GTIME_FPS         = 60




CAR_SENSORS_COUNT = 7

# скорость машины - 1
# текущее положение руля - 1
# сенсоры - SENSORS_COUNT = 5
# итого входов : 7
NN_INPUTS_COUNT = CAR_SENSORS_COUNT + 2
NN_HIDDEN_LAYERS_SIZE = [7, 5]
NN_OUTPUTS_COUNT = 2

# NN_structure имеет вид [20,10,5,2]
# 20 - число входов, 2 число выходов, 10, 5 скрытые слои
NN_STRUCTURE = [NN_INPUTS_COUNT] + NN_HIDDEN_LAYERS_SIZE + [NN_OUTPUTS_COUNT]





SBX_eta = 100




MAIN_WND_TITLE = 'Car chase'  # имя главного окна
MAIN_WND_FULLSCREEN = 0
MAIN_WND_BACKGROUND = 0x682828  # debug

if MAIN_WND_FULLSCREEN:
    MAIN_WND_HEIGHT     = 900             # для фулл скрин
    MAIN_WND_WIDTH      = 1600
else:
    MAIN_WND_HEIGHT     = 768               #768(в окне win)   # размер определен спрайтом зелени 128 * 6 = 768
    MAIN_WND_WIDTH      = 1400              #1400(в окне win)



# размер игровой карты (НЕ экрана)
MAP_SIZE_X = 2560
MAP_SIZE_Y = 896
MAP_SIZE_XY = (MAP_SIZE_X, MAP_SIZE_Y)
MAP_SIZE_RECT = pg.Rect(0, 0, MAP_SIZE_X, MAP_SIZE_Y)

MAP_TAIL_SIZE_X   = 20          # 20 * 128 = 2560
MAP_TAIL_SIZE_Y    = 7          # 6 * 128 = 768 (в окне win),        7 * 128 = 960

THEME_RED_CLR                   = 0xFB0D1C
THEME_GREEN_CLR                 = 0x2AC325
THEME_BLUE_CLR                  = 0x426DF9
THEME_DARK_GREY_CLR             = 0x282828
THEME_MED_GREY_CLR              = 0x606060
THEME_LIGHT_GREY_CLR            = 0xe7e7e7

THEME_BORDER_CLR_LOW            = THEME_MED_GREY_CLR
THEME_BORDER_CLR_HIGH           = THEME_LIGHT_GREY_CLR
THEME_BACKGROUND_CLR            = THEME_DARK_GREY_CLR
THEME_BACKGROUND_HOVER_CLR      = 0x1A1A1A
THEME_FONT_CLR                  = THEME_LIGHT_GREY_CLR
THEME_FONT_DISABLED_CLR         = THEME_MED_GREY_CLR
THEME_FONT                      = "arial_20"
THEME_FONT_CONTROL              = "arial_14"

THEME_BUTTON_BACKGROUND         = THEME_BACKGROUND_CLR
THEME_BUTTON_BACKGROUND_HOVER   = THEME_BACKGROUND_HOVER_CLR
THEME_BUTTON_BORDER_CLR         = THEME_BORDER_CLR_HIGH
THEME_BUTTON_BORDER_DISABLED_CLR = THEME_BORDER_CLR_LOW

THEME_SEMAPHOR_GREY             = THEME_DARK_GREY_CLR
THEME_SEMAPHOR_GREEN            = 0x10F010
THEME_SEMAPHOR_RED              = 0xE01010


THEME_SELECT_BACKGROUND_CLR         = THEME_BACKGROUND_CLR
THEME_SELECT_BACKGROUND_HOVER_CLR   = THEME_BACKGROUND_HOVER_CLR
THEME_SELECT_BORDER_CLR         = THEME_BORDER_CLR_HIGH
THEME_SELECT_STRING_HEIGHT      = 22


# THEME_WINDOW_BACKGROUND     = THEME_DARK_GREY_CLR



TOOL_WND_WIDTH       = 300
TOOL_WND_RECT        = pg.Rect(MAIN_WND_WIDTH-TOOL_WND_WIDTH, 0, TOOL_WND_WIDTH, MAIN_WND_HEIGHT)   #left top w h
# CONTROL_WND_BACKGROUND  = THEME_DARK_GREY_CLR
TOOL_WND_FONT_SIZE   = 20
# THEME_FONT_CLR  = 0xe7e7e7              # цвет шрифта на контролах
# CONTROL_WND_FONT_DISABLED_COLOR  = THEME_BUTTON_BORDER_DISABLED_CLR


MAP_WND_RECT            = pg.Rect(0,0,MAIN_WND_WIDTH - TOOL_WND_WIDTH,MAIN_WND_HEIGHT) #left top w h
MAP_WND_BACKGROUND      = 0x682848


CONSOLE_CLR_ERROR   = "\033[35m\033[1m"
CONSOLE_CLR_RED     = "\033[31m\033[1m"
CONSOLE_CLR_GREEN   = "\033[32m\033[1m"
CONSOLE_CLR_RESET   = "\033[0m"

#=================================================================================