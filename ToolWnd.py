import pygame as pg
from config import *
from fw.functions import *
#from fw.FwError import FwError

from fw.fwToolWnd import fwToolWnd
from fw.GuiButton import GuiButton
from fw.GuiCombobox import GuiCombobox
from fw.GuiLabel import GuiLabel


#
# окно с органами управления игрой (форма)
#
class ToolWnd(fwToolWnd):

    def __init__(self,params):

        # params['rect'] = CONTROL_WND_RECT
        # params['background_color'] = CONTROL_WND_BACKGROUND
        # params['name'] = 'ControlWnd'

        super().__init__(params)        # parent - fwWindow

        ############################################

        self.addChildWnd(GuiButton({
            'name': 'button-quit',
            'text': 'Quit',
            'parent_wnd':self,
            'rect': pg.Rect(220,20,56,32),
            'on_button_func': self.quit_onButton
        }))

        ############################################

        self.addChildWnd(GuiButton({
            'name': 'button-start',
            'text': 'New',
            'parent_wnd':self,
            'rect': pg.Rect(10,60,60,32),
            'on_button_func': self.new_onButton
        }))


        self.addChildWnd(GuiButton({
            'name': 'button-play',
            'text': 'Play',
            'parent_wnd':self,
            'rect': pg.Rect(74,60,60,32),
            'on_button_func': self.play_onButton
        }))

        btnPause = self.addChildWnd(GuiButton({
            'name': 'button-pause',
            'text': 'Pause',
            'parent_wnd':self,
            'rect': pg.Rect(138,60,60,32),
            'on_button_func': self.play_onButton
        }))

        btnPause.disable()


        ############################################

        self.addChildWnd(GuiCombobox({
            'name': 'combo-test',
            'text': ["one","two","three","four"],
            'value' : "two",
            'parent_wnd':self,
            'rect': pg.Rect(10,120,120,22),
            #'on_button_func': self.quit_onButton
        }))

        ############################################

        self.addChildWnd(GuiLabel({
            'parent_wnd':self,
            'rect': pg.Rect(0,200,60,32),
            'text': 'Param 1:',
        }))



        self.lbl_speed = GuiLabel({
            'parent_wnd': self,
            'rect': pg.Rect(61, 200, 200, 32),
            'text': '0',
        })
        self.addChildWnd(self.lbl_speed)

        ############################################

        self.addChildWnd(GuiLabel({
            'parent_wnd':self,
            'rect': pg.Rect(0,232,100,32),
            'text': 'ticks:',
        }))


        self.lbl_ticks = GuiLabel({
            'parent_wnd': self,
            'rect': pg.Rect(80, 232, 100, 32),
            'text': '0',
        })
        self.addChildWnd(self.lbl_ticks)

    ############################################

    def sendMessage(self, client_wnd, msg, param1=None,param2=None):
        if (msg == "WM_SET_PARAM_1"):
            self.lbl_speed.setText(param1)

        elif (msg == "WM_SET_TICKS"):
            self.lbl_ticks.setText(param1)

        elif (msg == 'WM_NEW_GAME'):
            self.newGame()

        else:
            #если не обработали здесь то отправляем наверх
            super().sendMessage(None, msg, param1, param2)

    def newGame(self):
        pass



    def quit_onButton(self):
        getAppWnd().sendMessage(None, 'WM_QUIT_APP')

    def new_onButton(self):
        getAppWnd().sendMessage(None, 'WM_NEW_APP')


    def play_onButton(self):
        pass
