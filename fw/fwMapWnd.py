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


    # def newGame(self):


    def sendMessage(self, msg, param1=None, param2=None):
        # fwWindow.sendMessage - не олпределен

        if msg == 'WM_NEW_SERIES':
            self.newGame()

        elif msg == 'WM_QUIT':
            pass

        elif msg == 'WM_UPDATE_TRAINING':
            self.updateTraining();

        elif msg == 'WM_UPDATE_SHOW':
            pass

        else:
            # если не обработали здесь то вызываем fwWindow.sendMessage
            super().sendMessage(msg, param1, param2)

