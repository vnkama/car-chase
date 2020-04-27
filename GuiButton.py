import pygame as pg
from GuiWindow import GuiWindow

from config import *
from functions import *

class GuiButton(GuiWindow):
    def __init__(self,params):
        super().__init__(params)

        self.bg_color_hover = params.get('bg_hover_color',self.bg_color)

        getMainWnd().registerHandler_MOUSEMOTION(self)
        getMainWnd().registerHandler_MOUSEBUTTONDOWN(self)


    def __del__(self):
        getMainWnd().unregHandler_MOUSEMOTION(self)
        getMainWnd().unregHandler_MOUSEBUTTONDOWN(self)



    def handle_MOUSEMOTION(self,event):
        #
        # обработчик перемещения мыши
        # координаты приходят абсолютные, относительно окна приложения
        #
        self.mouse_hover_flag = self.isPointInWindow(event.pos)


    def handle_MOUSEBUTTONDOWN(self,event):
        if (event.button == 1):
            # нажата левая кнопка

            if (self.isPointInWindow(event.pos)):
                #кнопка нажата в зоне кнопки
                print("START !!!!")



    def draw_this(self):
        if (not self.mouse_hover_flag):
            self.drawBackground()
        else:
            self.drawBackground(self.bg_color_hover)

        self.drawBorder()

        global getFont
        f = getFont('arial_16')
        text1_srf = f.render('Start', 1, HRGB(CONTROL_WND_FONT_COLOR))


        but_rect = self.surface.get_rect()
        text_rect = text1_srf.get_rect()

        self.surface.blit(text1_srf,((but_rect.width - text_rect.width) / 2,(but_rect.height -  text_rect.height) / 2))















