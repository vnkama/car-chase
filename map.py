import numpy as np
from tkinter import messagebox as mb2


MAP_X_SIZE_PIX = 800
MAP_Y_SIZE_PIX = 600

MAP_X_SIZE_MINIMAP = 80
MAP_Y_SIZE_MINIMAP = 60



class cMap:

    def __init__(self,params=[]):
        self.initO2()

    def initO2(self):
        self.o2_map = np.zeros((MAP_X_SIZE_MINIMAP,MAP_Y_SIZE_MINIMAP),dtype=np.int32)

        with np.nditer(self.o2_map, op_flags=['readwrite'],flags=['multi_index']) as its_o2_map:
            for x in its_o2_map:
                o2 = 100 - its_o2_map.multi_index[1] * 2
                x = o2 if o2 >= 0 else 0

    def drawO2(self):




