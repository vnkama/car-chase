#import pygame as pg
from fw.functions import *
from fw.fwAppWnd import fwAppWnd

from ToolWnd import ToolWnd
from MapWnd import MapWnd


#
#
#
class AppWnd(fwAppWnd):

    #
    #
    #
    def __init__(self):
        #fwAppWnd.__init__(self)
        super().__init__()

        #

        self.newGame()


    #
    # инициализируем основные окна,
    # это надо делать в AppWnd а не в  fwAppWnd, тк fwAppWnd не знает классов не из фреймворков типа ToolWnd итп
    #
    def initMainWindows(self):
        self.control_wnd = ToolWnd({
            'parent_wnd': self
        })
        self.addChildWnd(self.control_wnd)

        self.map_wnd = MapWnd({
            'parent_wnd': self,
            'control_wnd': self.control_wnd,
        })
        self.addChildWnd(self.map_wnd)


    #
    #
    #
    def update(self):
        super().update()

        dt = self.main_timer.get_time()
        self.control_wnd.sendMessage(None, "WM_SET_TICKS",dt)
        self.map_wnd.dt = dt




