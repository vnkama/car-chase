import pygame
from game import Game
from ControlWnd import ControlWnd
from MapWnd import MapWnd

from functions import *



class CarChase(Game):

    def __init__(self):
        Game.__init__(self)

        # укахатель на главное окно приложения
        setMainWnd(self)

        self.createChild(ControlWnd({'parent_obj':self}))
        self.createChild(MapWnd({'parent_obj':self}))




