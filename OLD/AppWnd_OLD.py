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
    #     self.tool_wnd = ToolWnd({
    #         'parent_wnd': self
    #     })
    #     self.addChildWnd(self.tool_wnd)
    #
    #
    #     self.map_wnd = MapWnd({
    #         'parent_wnd': self,
    #         'tool_wnd': self.tool_wnd,
    #     })
    #     self.addChildWnd(self.map_wnd)


    # def update(self):
    #     # вывод времени . прошедшем с предыдущего вызова dt
    #     super().update()
    #
    #     self.tool_wnd.sendMessage("WM_SET_TICKS", self.update_dt_ms)
    #     self.map_wnd.dt = self.update_dt_ms




