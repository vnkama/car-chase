#import pygame as pg
from config import *
#from fw.functions import *
from fw.fwWindow import fwWindow


#
#
#
class fwControlWnd(fwWindow):

    def __init__(self,params):

        params['rect'] = CONTROL_WND_RECT
        params['background_color'] = THEME_WINDOW_BACKGROUND
        params['name'] = 'ControlWnd'

        super().__init__(params)        # parent - fwWindow