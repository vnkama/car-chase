import pygame as pg
from config import *
#from fw.functions import *
from fw.GuiControl import GuiControl

import math
#
#
#
from src.config import THEME_RED_CLR, THEME_GREEN_CLR, THEME_GREY_CLR


class GuiSemaphor(GuiControl):

    def __init__(self, params):
        # имя по умолчанию
        params['name'] = params.get('name', 'GuiSemaphor')
        self.radius = params.get('radius', 4)

        self.lamp_color = THEME_SEMAPHOR_RED
        params['background_color'] = params.get('background_color', THEME_BUTTON_BACKGROUND)
        #self.images = params['images']

        super().__init__(params)

    def drawThis(self):
        #text1_srf = getAppWnd().getFont('arial_16').render(str(self.text), 1, HRGB(CONTROL_WND_FONT_COLOR))

        rect = self.surface.get_rect()

        pg.draw.circle(
            self.surface,
            self.lamp_color,
            (math.floor(rect.w/2), math.floor(rect.h/2)),
            self.radius,
            0,  # 0- fill
        )
        #text_rect = text1_srf.get_rect()

        # self.surface.blit(
        #     text1_srf,
        #     (2, (but_rect.height -  text_rect.height) / 2)
        # )

    def setColor(self, color):
        if color == 'red':
            self.lamp_color = THEME_RED_CLR
        elif color == 'green':
            self.lamp_color = THEME_GREEN_CLR
        elif color == 'grey':
            self.lamp_color = THEME_GREY_CLR
