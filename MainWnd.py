#import pygame as pg
from fw.functions import *
from fw.fwMainWnd import fwMainWnd

from ControlWnd import ControlWnd
from MapWnd import MapWnd


#
#
#
class MainWnd(fwMainWnd):

    def __init__(self):
        fwMainWnd.__init__(self)


        self.control_wnd = ControlWnd({
            'parent_obj':self
        })
        self.createChild(self.control_wnd)

        self.map_wnd = MapWnd({
            'parent_obj':self,
            'control_wnd':self.control_wnd
        })
        self.createChild(self.map_wnd)


    def update(self):
        super().update()

        dt = self.main_timer.get_time()
        self.control_wnd.sendMessage("WM_SET_TICKS",dt)
        self.map_wnd.dt = dt


    def newGame(self):
        self.map_wnd.newGame()
