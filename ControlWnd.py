import pygame as pg
from config import *


from fw.GuiWindow import GuiWindow
from fw.GuiButton import GuiButton
from fw.GuiLabel import GuiLabel


#
# окно с органами управления игрой (форма)
#
class ControlWnd(GuiWindow):

    def __init__(self,params):

        params['rect'] = CONTROL_WND_RECT
        params['bg_color'] = CONTROL_WND_BACKGROUND
        params['name'] = 'ControlWnd'

        super().__init__(params)        # parent - GuiWindow

        self.createChild(GuiButton({
            'name': 'button-start',
            'text': 'quit',
            'parent_obj':self,
            'rect': pg.Rect(20,430,120,32),
            'bg_color': CONTROL_WND_BACKGROUND,
            'bg_hover_color': THEME_BACKGROUND_HOVER_COLOR,
            'border_color': THEME_BORDER_COLOR_HIGH,
            'border_width': 1,
            'font': 'arial_20',
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



    def update(self):
        pass


    def sendMessage(self,code,param1,param2=0):
        if (code == "WM_SET_PARAM_1"):
            self.lbl_speed.setText(param1)

        elif (code == "WM_SET_TICKS"):
            self.lbl_ticks.setText(param1)



