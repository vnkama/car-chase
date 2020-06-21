import pygame as pg
from config import *

from fw.functions import *
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

        self.createChild(GuiButton({
            'name': 'button-start',
            'text': 'New',
            'parent_obj':self,
            'rect': pg.Rect(20,380,120,32),
            'font': 'arial_20',
            'on_button_func': self.start_onButton
        }))


        self.createChild(GuiButton({
            'name': 'button-quit',
            'text': 'Quit',
            'parent_obj':self,
            'rect': pg.Rect(20,430,120,32),
            'font': 'arial_20',
            'on_button_func': self.quit_onButton
        }))

        self.createChild(GuiCombobox({
            'name': 'combo-test',
            'text': 'combo',
            'parent_obj':self,
            'rect': pg.Rect(20,480,120,22),
            'font': 'arial_20',
            #'on_button_func': self.quit_onButton
        }))

        ############################################
        #
        self.createChild(GuiLabel({
            'parent_obj':self,
            'rect': pg.Rect(0,100,60,32),
            'text': 'Param 1:',
            'font': 'arial_20',
        }))


        #
        self.lbl_speed = GuiLabel({
            'parent_obj': self,
            'rect': pg.Rect(61, 100, 200, 32),
            'text': '0',
            'font': 'arial_20',
        })
        self.createChild(self.lbl_speed)

        ############################################
        #
        self.createChild(GuiLabel({
            'parent_obj':self,
            'rect': pg.Rect(0,140,100,32),
            'text': 'ticks:',
            'font': 'arial_20',
        }))


        #
        self.lbl_ticks = GuiLabel({
            'parent_obj': self,
            'rect': pg.Rect(80, 140, 100, 32),
            'text': '0',
            'font': 'arial_20',
        })
        self.createChild(self.lbl_ticks)



    def sendMessage(self,code,param1,param2=0):
        if (code == "WM_SET_PARAM_1"):
            self.lbl_speed.setText(param1)

        elif (code == "WM_SET_TICKS"):
            self.lbl_ticks.setText(param1)


    def quit_onButton(self):
        getMainWnd().is_mainloop_run = False

    def start_onButton(self):
        getMainWnd().newGame()
