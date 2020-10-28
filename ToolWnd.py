import pygame as pg
from config import *
from fw.functions import *
# from fw.FwError import FwError

from fw.fwToolWnd import fwToolWnd
# from fw.GuiButton import GuiButton
from fw.GuiSelect import GuiSelect
from fw.GuiLabel import GuiLabel


#
# окно с органами управления игрой (форма)
#
class ToolWnd(fwToolWnd):

    def __init__(self, params):

        # params['rect'] = TOOL_WND_RECT
        # params['background_color'] = CONTROL_WND_BACKGROUND
        # params['name'] = 'ControlWnd'

        super().__init__(params)        # parent - fwWindow




        ############################################



        ############################################

        # self.addChildWnd(GuiSelect({
        #     'name': 'combo-test',
        #     'text': ["one", "two", "three", "four"],
        #     'value': "two",
        #     'parent_wnd': self,
        #     'rect': pg.Rect(60, 180, 80, 22),
        #     # 'on_button_func': self.quit_onButton
        # }))

        ############################################

        self.addChildWnd(GuiLabel({
            'parent_wnd': self,
            'rect': pg.Rect(0, 300, 60, 32),
            'text': 'Param 1:',
        }))



        self.lbl_speed = GuiLabel({
            'parent_wnd': self,
            'rect': pg.Rect(61, 300, 200, 32),
            'text': '0',
        })
        self.addChildWnd(self.lbl_speed)

        ############################################

        self.addChildWnd(GuiLabel({
            'parent_wnd': self,
            'rect': pg.Rect(0, 332, 100, 32),
            'text': 'ticks:',
        }))


        self.lbl_ticks = GuiLabel({
            'parent_wnd': self,
            'rect': pg.Rect(80, 332, 100, 32),
            'text': '0',
        })
        self.addChildWnd(self.lbl_ticks)

    ############################################

    def sendMessage(self, msg, param1=None, param2=None):
        if msg == 'WM_SET_PARAM_1':
            self.lbl_speed.setText(param1)

        elif msg == 'WM_SET_TICKS':
            self.lbl_ticks.setText(param1)

        else:
            # если не обработали здесь то отправляем наверх
            super().sendMessage(msg, param1, param2)

