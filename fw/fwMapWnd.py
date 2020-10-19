# import pygame as pg
# import numpy as np
# from config import *
# from fw.functions import *

from fw.fwWindow import fwWindow


#
# класс пока пустой
#
class fwMapWnd(fwWindow):

    # def __init__(self):
        # pass


    def sendMessage(self, msg, param1=None, param2=None):
        # fwWindow.sendMessage - не олпределен

        if msg == 'WM_NEW_GAME':
            self.newGame()

        elif msg == 'WM_QUIT':
            pass

        else:
            # если не обработали здесь то вызываем fwWindow.sendMessage
            super().sendMessage(msg, param1, param2)
