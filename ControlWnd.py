import pygame
from config import *


from GuiWindow import GuiWindow
from GuiButton import GuiButton

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
            'text': 'Start',
            'parent_obj':self,
            'rect': pygame.Rect(70,430,120,32),
            'bg_color': CONTROL_WND_BACKGROUND,
            'bg_hover_color': THEME_BACKGROUND_HOVER_COLOR,
            'border_color': THEME_BORDER_COLOR_HIGH,
            'border_width': 1,
            'font': 'arial_20',
        }))


    def update(self):
        pass






