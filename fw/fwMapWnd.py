# import pygame as pg
# import numpy as np
from config import *
# from fw.functions import *

from fw.fwWindow import fwWindow


#
# класс пока пустой
#
class fwMapWnd(fwWindow):

    def __init__(self, params):
        super().__init__(params)        # parent - fwWindow

        # номер шага обучения (1-based)
        # когда трайнинг не идет переменная тоже стоит
        # при инициации начального положения training_step = 0
        # в начале расчета 1го перемещения training_step ставится в  1
        self.training_update_step = None
        self.training_update_gtime_ms_f = None
        self.training_update_dt_gtime_ms_f = None


    def newGame(self):
        self.training_update_step = 0
        # self.training_step = 60 соответствует self.training_update_gtime_ms_f = 1000.0
        # применяется для расчета втч физики

        # время ticks последнего или текущего вызова update, считается с 0
        # 0 - начало игры, 60 сек - внутриигровая минута.
        # время хоккейное, при паузах стоит,
        self.training_update_gtime_ms_f = 0
        self.training_update_dt_gtime_ms_f = TRAINING_UPDATE_DT_GTAME_MS_F


    def sendMessage(self, msg, param1=None, param2=None):
        # fwWindow.sendMessage - не олпределен

        if msg == 'WM_NEW_GAME':
            self.newGame()

        elif msg == 'WM_QUIT':
            pass

        elif msg == 'WM_UPDATE_TRAINING':
            self.training_update();

        elif msg == 'WM_UPDATE_SHOW':
            pass

        else:
            # если не обработали здесь то вызываем fwWindow.sendMessage
            super().sendMessage(msg, param1, param2)

