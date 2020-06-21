import pygame as pg


#
#
#
class fwWindow:

    def __init__(self,params):
        self.parent_obj = params['parent_obj']

        self.child_objects = []

        if self.parent_obj is not None:
            #есть родительское
            self.surface = self.parent_obj.getSurface().subsurface(params['rect'])


        else:
            # нет родительсокго окна (например, это галвное окно приложения)
            # в таком случеа поверхность должна была быть передана при вызове
            self.surface = params['surface']

        #-------

        self.background_color = params.get('background_color',None)


        self.border_color = params.get('border_color',None)
        self.border_width = params.get('border_width',None)


        self.text = params.get('text',None)
        self.name = params.get('name',None)



    def draw(self):
        self.draw_this()
        self.draw_child()


    def draw_child(self):
        #вызовем draw очерних окон
        if len(self.child_objects):
            for wnd in self.child_objects:
                wnd.draw()

    def draw_this(self):
        #как правило эту функцию следует переопределить

        #свой фон (если есть)
        self.drawBackground()


    def update(self):
        self.update_child()

    def update_child(self):
        for child_object in self.child_objects:
            child_object.update()



    def drawBackground(self,color = None):
        if (color is not None):
            self.surface.fill(color)
        elif (self.background_color is not None):
            self.surface.fill(self.background_color)


    def drawBorder(self):
        #свою рамку, если есть
        if self.border_width is not None and self.border_color is not None :
            if self.border_width > 0:
                surface_rect = self.surface.get_rect()

                pg.draw.rect(
                    self.surface,
                    self.border_color,
                    surface_rect,
                    self.border_width)


    #
    # проверяем попадает ли координата внутрь данного окна
    #
    def isPointInWindow(self,point):
        return pg.Rect(self.surface.get_abs_offset(),self.surface.get_size()).collidepoint(point)



    #
    #
    #
    def setText(self,new_text):
        self.text = new_text

    def getSurface(self):
        return self.surface

    def createChild(self,new_child):
        self.child_objects.append(new_child)

    # def draw(self):
    #     self.draw_this()   #-метод пустой, но его переопределим в классах наследниках
    #
    #     # вызовем draw очерних окон
    #     for wnd in self.child_objects:
    #         wnd.draw()

