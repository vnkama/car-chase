import pygame as pg
# from config import *
# from fw.functions import *
# from fw.FwError import FwError


#
# базовый класс окна.
# класс абстрактный, напрямую  объект от него не создаетсмя
#
class fwWindow:

    def __init__(self,params):
        self.parent_wnd = params['parent_wnd']

        self.child_objects = []

        if self.parent_wnd is not None:
            #есть родительское
            self.surface = self.parent_wnd.surface.subsurface(params['rect'])


        else:
            # нет родительсокго окна
            # пример, это главное окно приложения
            # в таком случеа поверхность должна была быть передана при вызове
            self.surface = params['surface']

        #-------

        self.background_color = params.get('background_color',None)


        self.border_color = params.get('border_color',None)
        self.border_width = params.get('border_width',None)


        self.text = params.get('text',None)
        self.name = params.get('name',None)



    def draw(self):
        self.drawThis()
        self.drawChildWnds()



    def drawThis(self):
        #как правило эту функцию следует переопределить

        #закрасит свой фон (если есть)
        self.drawBackground()



    def drawChildWnds(self):
        #вызовем draw очерних окон
        if len(self.child_objects):
            for wnd in self.child_objects:
                wnd.draw()



    def update(self):
        self.updateChildWnds()

    def updateChildWnds(self):
        for child_object in self.child_objects:
            child_object.update()



    def drawBackground(self, color = None):
        if (color is not None):
            self.surface.fill(color)
        elif (self.background_color is not None):
            self.surface.fill(self.background_color)



    def drawBorder(self):
        #рисуем свою рамку, если есть
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
        return pg.Rect(
            self.surface.get_abs_offset(),
            self.surface.get_size()
        ).collidepoint(point)



    #
    #
    #
    def setText(self,new_text):
        self.text = new_text

    def getSurface(self):
        return self.surface

    def addChildWnd(self,new_child):
        self.child_objects.append(new_child)

    # def handleMessageToChilds_handler(self, client_wnd, msg, param1, param2):
    #     self.sendMessageToChilds(self, client_wnd, msg, param1, param2)

    def sendMessageToChilds(self, client_wnd, msg, param1=None, param2=None):
        for child_object in self.child_objects:
            child_object.sendMessage(client_wnd, msg, param1, param2)


    #
    # функция пустая, переопределять
    #   return True если сообщение обработано
    #   False если сообщение не обработано
    #
    def sendMessage(self,client_wnd, msg, param1=None, param2=None):
        return False


    # абстарнктные обработчики событий клавиатуры и мыши
    # реальные нужно определять в классах наследниках, там где необходимы
    def handle_MOUSEMOTION(self, event):        pass
    def handle_MOUSEBUTTONDOWN(self, event):    pass
    def handle_KEYDOWN(self, event):            pass
    def handle_KEYUP(self, event):              pass

