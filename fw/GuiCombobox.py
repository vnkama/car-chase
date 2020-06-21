import pygame as pg
from config import *
from fw.functions import *
from fw.GuiControl import GuiControl


#
#
#
class GuiCombobox(GuiControl):

    #load image of archer
    archer_srf = pg.image.load("./images/gui/combobox_archer.png").convert()

    def __init__(self,params):

        params['background_color'] = params.get('background_color',THEME_COMBOBOX_BACKGROUND)
        params['background_color_hover'] = params.get('background_color_hover',THEME_COMBOBOX_BACKGROUND_HOVER)
        params['border_color'] = params.get('border_color',THEME_COMBOBOX_BORDER_COLOR)
        params['border_width'] = params.get('border_width',1)

        super().__init__(params)

        getMainWnd().registerHandler_MOUSEMOTION(self)
        getMainWnd().registerHandler_MOUSEBUTTONDOWN(self)



    def draw_this(self):
        if (not self.mouse_hover_flag):
            self.drawBackground()
        else:
            self.drawBackground(self.background_color_hover)

        self.drawBorder()

        X = self.surface.get_rect().w-14
        Y = (self.surface.get_rect().h-5)//2
        Y = Y if Y//2 else Y+1

        #print("Y:",Y)


        archer_rect = pg.Rect(X,Y,9,5)      #9,5 - size of archer

        #copy archer to control
        self.surface.blit(
            GuiCombobox.archer_srf,
            archer_rect)



