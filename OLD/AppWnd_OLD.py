#import pygame as pg
# from fw.functions import *
# from fw.fwAppWnd import fwAppWnd
#
# from ToolWnd import ToolWnd
# from MapWnd import MapWnd



#
#
#
# class AppWnd(fwAppWnd):
#
#
#     #
#     def __init__(self):
#         super().__init__()


    # #
    # # инициализируем основные окна,
    # # это надо делать в AppWnd а не в  fwAppWnd, тк fwAppWnd не знает классов не из фреймворков типа ToolWnd итп
    # #
    # def initMainWindows(self):
    #     self.Tool_wnd = ToolWnd({
    #         'parent_wnd': self
    #     })
    #     self.addChildWnd(self.Tool_wnd)
    #
    #
    #     self.Map_wnd = MapWnd({
    #         'parent_wnd': self,
    #         'Tool_wnd': self.Tool_wnd,
    #     })
    #     self.addChildWnd(self.Map_wnd)


    # def update(self):
    #     # вывод времени . прошедшем с предыдущего вызова dt
    #     super().update()
    #
    #     self.Tool_wnd.sendMessage("WM_SET_TICKS", self.update_dt_ms)
    #     self.Map_wnd.dt = self.update_dt_ms




