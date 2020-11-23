#import pygame as pg
from config import *
from fw.functions import *
from fw.GuiControl import GuiControl

#
#
#
class GuiLabel(GuiControl):

    def drawThis(self):
        text1_srf = getAppWnd().getFont(self.font_name).render(str(self.text), 1, HRGB(THEME_FONT_CLR))

        but_rect = self.surface.get_rect()
        text_rect = text1_srf.get_rect()

        self.surface.blit(
            text1_srf,
            (2, (but_rect.height -  text_rect.height) / 2)
        )
