import pygame as pg
from config import *
# from fw.functions import *
from fw.FwError import FwError



class fwWindow:
    #
    # базовый класс окна.
    # класс абстрактный, напрямую  объект от него не создаетсмя
    #

    def __init__(self, params):
        # parent_wnd используется parent_send_message
        self.parent_wnd = params['parent_wnd']

        # сохранеям указатель на родительский  surface, если своего surface нет
        # нужен чтобы давать его чайлдам данного объекта
        self.parent_surface = None

        self.surface = None

        self.enabled = True
        self.child_objects = []

        self.main_rect = None
        self.old_rect = None




        if params['type'] == 'main':
            # это главное окно приложения
            # родительсокго окна - нет
            # surface у него - главная поверхность pygame, она должна была быть передана при вызове через params['surface']

            #  params['surface']
            self.parent_wnd = None
            self.surface = params['surface']
            self.main_rect = params['rect']



        elif params['type'] == 'normal':
            # обычное окно
            self.parent_wnd = params['parent_wnd']

            if self.parent_wnd.surface is not None:
                # у родительскокго окна есть surface, создадм свою subsurface от него
                self.surface = self.parent_wnd.surface.subsurface(params['rect'])
            else:
                # у родительскокго окна нет surface, но он должен хранить parent_surface создадм свою subsurface от него
                self.surface = self.parent_wnd.parent_surface.subsurface(params['rect'])

            self.main_rect = params['rect']


        elif params['type'] == 'no_surface':
            # мы создаем не окно а объект у которого нет surface,
            # но может update, sendMessage
            self.parent_wnd = params['parent_wnd']
            self.surface = None
            self.parent_surface = params['parent_surface']

        else:
            raise FwError()


        self.background_color = params.get('background_color', None)
        self.background_disabled_color = params.get('background_color', self.background_color)


        self.border_color = params.get('border_color', None)
        self.border_width = params.get('border_width', None)


        self.text = params.get('text',None)
        self.name = params.get('name',None)



    #
    # как правило эту функцию следует переопределить
    #
    def draw(self):
        self.drawThis()
        self.sendMessageToChilds('WM_DRAW')


    #
    # как правило эту функцию следует переопределить
    # закрасит свой фон (если есть)
    #
    def drawThis(self):
        self.drawBackground()



    #
    #
    #
    def drawBackground(self, color = None):
        if color is not None:
            self.surface.fill(color)

        elif self.background_color is not None:
            self.surface.fill(self.background_color)



    #
    #
    #
    def drawBorder(self):
        # рисуем свою рамку, если есть
        if self.border_width is not None and self.border_color is not None:

            color = self.border_color if self.enabled else THEME_BUTTON_BORDER_DISABLED_CLR

            if self.border_width > 0:
                surface_rect = self.surface.get_rect()

                pg.draw.rect(
                    self.surface,
                    color,
                    surface_rect,
                    self.border_width)



    #
    # проверяем попадает ли координата внутрь данного окна
    # point - координата относительно окна приложения -> (x,y)
    #
    def isPointInWindow(self, point):

        return pg.Rect(
                self.surface.get_abs_offset(),
                self.surface.get_size()
        ).collidepoint(point)



    #
    # point - координата относительно окна приложения
    # возвращает коорднаты точки point относительно даннго окна -> (x,y)
    #
    def getOffsetInWindow(self, point):

        offs = self.surface.get_abs_offset() #координаты данного окна относительно приложения
        return (
            point[0] - offs[0],
            point[1] - offs[1],
        )



    def setText(self, new_text):
        self.text = new_text

    def getSurface(self):
        return self.surface

    def addChildWnd(self, new_child):
        self.child_objects.append(new_child)
        return new_child


    def sendMessage(self, msg, param1=None, param2=None):
        #
        #   return True если сообщение обработано
        #   False если сообщение не обработано
        #

        if msg == 'WM_DRAW':
            self.draw()

        elif msg == 'WM_UPDATE':
            self.update()

        else:
            return False


    def sendMessageToChilds(self, msg, param1=None, param2=None):
        for child_wnd in self.child_objects:
            child_wnd.sendMessage(msg, param1, param2)


    def drawAllChilds(self):
        for child_wnd in self.child_objects:
            child_wnd.draw()


    # def update(self):
    #     pass





    # абстарнктные обработчики событий клавиатуры и мыши
    # реальные нужно определять в классах наследниках, там где необходимы
    def handle_MouseMotion(self, event):        pass
    def handle_MouseButtonDown(self, event):    return True       # return True - значит можно продолжать обработку дальше
    def handle_KeyDown(self, event):            pass
    def handle_KeyUp(self, event):              pass


    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def isEnable(self):
        return self.enabled


    def resize(self, new_rect):
        # resize работает только если есть parent_wnd
        if self.parent_wnd is not None:
            old_offset = self.surface.get_offset()
            old_rectsize = self.surface.get_rect()
            self.old_rect = pg.Rect(old_offset, old_rectsize.size)

            # удаляем старую оверхность
            del self.surface

            # создаем новую поверхность
            self.surface = self.parent_wnd.surface.subsurface(new_rect)

    def resetOldSize(self):
            self.resize(self.old_rect)

