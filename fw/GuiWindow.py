import pygame
from fw.GameObject import *

class GuiWindow(GameObject):

    def __init__(self,params):
        super().__init__(params)  #он пустой


        self.bg_color = params.get('bg_color',None)


        self.border_color = params.get('border_color',None)
        self.border_width = params.get('border_width',None)


        self.text = params.get('text',None)
        self.name = params.get('name',None)



    def draw(self):
        super().draw()      #он пустой

        self.draw_this()

        #вызовем draw очерних окон
        if len(self.child_objects):
            for wnd in self.child_objects:
                wnd.draw()

    def draw_this(self):
        #как правило эту функцию следует переопределить

        #свой фон (если есть)
        self.drawBackground()

    # def update(self):
    #     pass


    def drawBackground(self,color = None):
        if (color is not None):
            self.surface.fill(color)
        elif (self.bg_color is not None):
            self.surface.fill(self.bg_color)


    def drawBorder(self):
        #свою рамку, если есть
        if self.border_width is not None and self.border_color is not None :
            if self.border_width > 0:
                surface_rect = self.surface.get_rect()

                pygame.draw.rect(
                    self.surface,
                    self.border_color,
                    surface_rect,
                    self.border_width)


    def isPointInWindow(self,point):
        #
        # проверяем попадает ли координата внутрь данного окна
        #

        return pg.Rect(self.surface.get_abs_offset(),self.surface.get_size()).collidepoint(point)

    #
    #
    #
    def setText(self,new_text):
        self.text = new_text