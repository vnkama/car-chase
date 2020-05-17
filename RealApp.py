import pygame as pg
from fw.functions import *
from fw.game import Game

from ControlWnd import ControlWnd
from MapWnd import MapWnd


#
#
#
class RealApp(Game):

    def __init__(self):
        Game.__init__(self)

        # укахатель на главное окно приложения
        setMainWnd(self)

        self.control_wnd = ControlWnd({'parent_obj':self})
        self.createChild(self.control_wnd)
        self.createChild(MapWnd({
            'parent_obj':self,
            'control_wnd':self.control_wnd
        }))


    def update(self):
        super().update()
        t = self.main_timer.get_time()
        self.control_wnd.sendMessage("WM_SET_TICKS",t)
