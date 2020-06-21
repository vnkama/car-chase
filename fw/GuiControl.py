#import pygame as pg
from config import *
from fw.functions import *
from fw.fwWindow import fwWindow


#
#
#
class GuiControl(fwWindow):

    def __init__(self,params):

        super().__init__(params)

        self.value = 0
        self.is_focus = 0
        self.background_color_hover = params.get('background_color_hover',self.background_color)


    # def __del__(self):
    #     pass


    def isFocus(self):
        return self.is_focus

    def setFocus(self,focus):
        self.is_focus = focus

    def getValue(self):
        return self.value

    def setValue(self,value):
        self.value = value

    def handle_MOUSEBUTTONDOWN(self,event):
        pass

    def handle_MOUSEBUTTONUP(self,event):
        pass

    def handle_MOUSEMOTION(self,event):
        #
        # обработчик перемещения мыши
        # координаты приходят абсолютные, относительно окна приложения
        #
        self.mouse_hover_flag = self.isPointInWindow(event.pos)
