import pygame as pg
from functions import *


class GameObject:
    # GameObject по сути surface-object
    #

    def __init__(self,params):
        self.parent_obj = params['parent_obj']

        self.child_objects = []

        if self.parent_obj is not None:
            #есть родительское
            self.surface = self.parent_obj.getSurface().subsurface(params['rect'])

            #регистрируемся в списке родителя
            #self.parent_obj.addChildWindow(self)

        else:
            # нет родительсокго окна (например, это галвное окно приложения)
            # в таком случеа поверхность должна была быть передана при вызове
            self.surface = params['surface']

    def getSurface(self):
        return self.surface

    def createChild(self,new_child):
        self.child_objects.append(new_child)

    def addChildWindow(self,new_window):
        self.child_objects.append(new_window)


    def draw(self):
        self.draw_this()   #-метод пустой, но переопредtkbnm в классах наследниках

        # вызовем draw очерних окон
        for wnd in self.child_objects:
            wnd.draw()

    def draw_this(self):
        pass


    def update(self):
        #if len(self.child_objects):

        for child_object in self.child_objects:
            child_object.update()

