import pygame
from game import Game
from ControlWnd import ControlWnd
from MapWnd import MapWnd

from functions import *



#from GuiWindow import GuiWindow

class LakeGame(Game):

    def __init__(self):
        Game.__init__(self)

        #уставноим шрифты
        setFonts({
            #индекс строго в нижнем регистре
            'arial_16': pygame.font.SysFont('Arial', 16),
            'arial_20': pygame.font.SysFont('Arial', 20),
            'tahoma_20': pygame.font.SysFont('Tahoma', 20),
        })

        # укахатель на главное окно приложения
        setMainWnd(self)

        self.createChild(ControlWnd({'parent_obj':self}))
        self.createChild(MapWnd({'parent_obj':self}))




