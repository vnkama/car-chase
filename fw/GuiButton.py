#import pygame as pg
from config import *
from fw.functions import *
from fw.GuiControl import GuiControl


#
#
#
class GuiButton(GuiControl):

    def __init__(self,params):

        params['background_color'] = params.get('background_color',THEME_BUTTON_BACKGROUND)
        params['background_color_hover'] = params.get('background_color_hover',THEME_BUTTON_BACKGROUND_HOVER)
        params['border_color'] = params.get('border_color',THEME_BUTTON_BORDER_COLOR)
        params['border_width'] = params.get('border_width',1)

        super().__init__(params)

        getAppWnd().registerHandler_MOUSEMOTION(self)
        getAppWnd().registerHandler_MOUSEBUTTONDOWN(self)

        self.on_button_func =  params.get('on_button_func', None)



    def handle_MOUSEBUTTONDOWN(self,event):
        if (self.enabled):

            if (event.button == 1):
                # нажата левая кнопка

                if (self.isPointInWindow(event.pos) and self.on_button_func is not None):
                    #кнопка нажата в зоне кнопки
                    self.on_button_func()



    def drawThis(self):

        if (not self.mouse_hover_flag or not self.enabled):
            self.drawBackground()
        else:
            self.drawBackground(self.background_color_hover)

        self.drawBorder()

        f = getAppWnd().getFont('arial_16')
        color = CONTROL_WND_FONT_COLOR if (self.enabled) else CONTROL_WND_FONT_DISABLED_COLOR;
        text1_srf = f.render(self.text, 1, HRGB(color))




        but_rect = self.surface.get_rect()
        text_rect = text1_srf.get_rect()

        self.surface.blit(text1_srf,((but_rect.width - text_rect.width) / 2,(but_rect.height -  text_rect.height) / 2))



















