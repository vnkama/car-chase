#import pygame as pg
from fw.functions import *
from fw.game import Game

from ControlWnd import ControlWnd
from MapWnd import MapWnd


class RealApp(Game):

    def __init__(self):
        Game.__init__(self)

        # укахатель на главное окно приложения
        setMainWnd(self)

        self.createChild(ControlWnd({'parent_obj':self}))
        self.createChild(MapWnd({'parent_obj':self}))
