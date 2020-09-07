import pygame as pg
from config import *
from fw.functions import *
#from fw.FwError import FwError

from fw.fwControlWnd import fwControlWnd
from fw.GuiButton import GuiButton
from fw.GuiCombobox import GuiCombobox
from fw.GuiLabel import GuiLabel


#
# окно с органами управления игрой (форма)
#
class ControlWnd(fwControlWnd):

    def __init__(self,params):

        # params['rect'] = CONTROL_WND_RECT
        # params['background_color'] = CONTROL_WND_BACKGROUND
        # params['name'] = 'ControlWnd'

        super().__init__(params)        # parent - fwWindow

        ############################################

        self.addChildWnd(GuiButton({
            'name': 'button-start',
            'text': 'New',
            'parent_wnd':self,
            'rect': pg.Rect(20,380,120,32),
            'on_button_func': self.start_onButton
        }))


        self.addChildWnd(GuiButton({
            'name': 'button-quit',
            'text': 'Quit',
            'parent_wnd':self,
            'rect': pg.Rect(20,430,120,32),
            'on_button_func': self.quit_onButton
        }))

        self.addChildWnd(GuiCombobox({
            'name': 'combo-test',
            'text': ["one","two","three","four"],
            'value' : "two",
            'parent_wnd':self,
            'rect': pg.Rect(20,480,120,22),
            #'on_button_func': self.quit_onButton
        }))

        ############################################

        self.addChildWnd(GuiLabel({
            'parent_wnd':self,
            'rect': pg.Rect(0,100,60,32),
            'text': 'Param 1:',
        }))



        self.lbl_speed = GuiLabel({
            'parent_wnd': self,
            'rect': pg.Rect(61, 100, 200, 32),
            'text': '0',
        })
        self.addChildWnd(self.lbl_speed)

        ############################################

        self.addChildWnd(GuiLabel({
            'parent_wnd':self,
            'rect': pg.Rect(0,140,100,32),
            'text': 'ticks:',
        }))


        self.lbl_ticks = GuiLabel({
            'parent_wnd': self,
            'rect': pg.Rect(80, 140, 100, 32),
            'text': '0',
        })
        self.addChildWnd(self.lbl_ticks)



    def sendMessage(self,code,param1=None,param2=None):
        if (code == "WM_SET_PARAM_1"):
            self.lbl_speed.setText(param1)

        elif (code == "WM_SET_TICKS"):
            self.lbl_ticks.setText(param1)

        else:
            #если не обработали здесь то отправляем наверх
            super().sendMessage(code,param1,param2)





    def quit_onButton(self):
        getMainWnd().is_mainloop_run = False

    def start_onButton(self):
        getMainWnd().newGame()



