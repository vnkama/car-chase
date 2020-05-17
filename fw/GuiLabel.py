import pygame as pg
from config import *
from fw.functions import *
from fw.GuiWindow import GuiWindow

#
#
#
class GuiLabel(GuiWindow):

    def draw_this(self):
        global getFont
        text1_srf = getFont('arial_16').render(str(self.text), 1, HRGB(CONTROL_WND_FONT_COLOR))

        but_rect = self.surface.get_rect()
        text_rect = text1_srf.get_rect()

        self.surface.blit(
            text1_srf,
            (2, (but_rect.height -  text_rect.height) / 2)
        )
