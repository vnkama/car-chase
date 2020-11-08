#import pygame as pg
from config import *
from fw.functions import *
#from fw.FwError import FwError

from fw.fwWindow import fwWindow


#
#
#
class GuiControl(fwWindow):

    def __init__(self,params):

        params['font'] = params.get('font', THEME_FONT)
        params['type'] = 'normal'

        super().__init__(params)

        self.value = 0
        self.is_focus = False
        self.background_color_hover = params.get('background_color_hover', self.background_color)

        self.mouse_hover_flag =0






    # def __del__(self):
    #     pass


    def isFocus(self):
        return self.is_focus

    def setFocus(self):
        self.is_focus = True

    def clearFocus(self):
        self.is_focus = False

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value





    def handle_MOUSEBUTTONUP(self, event):
        pass

    def handle_MOUSEMOTION(self, event):
        #
        # обработчик перемещения мыши
        # координаты приходят абсолютные, относительно окна приложения
        #
        self.mouse_hover_flag = self.isPointInWindow(event.pos)


    def draw(self):
        self.drawThis()
        # drawChilds не вызывается потомучто у контролов нет чайлдов
        # а если у кого и есть пусть переопределят draw

    def handleClickInFocus(self, event):
        pass

    def handle_MouseButtonDown(self, event):
        if event.button == 1:
            # mouse LB have pressed

            if self.isPointInWindow(event.pos):
                # MLB нажата в пределах контрола

                if not self.isFocus():
                    # не в фокусе, запрашиваем фокус,
                    self.parent_wnd.sendMessage('WM_REQUEST_FOCUS', self)

                else:
                    # контрол в фокусе
                    # обработаем контрол
                    return self.handleClickInFocus(event)



            else:
                # MLB  нажата вне контрола
                # сбросим фокус
                if self.is_focus:
                    self.parent_wnd.sendMessage('WM_REQUEST_FREE_FOCUS', self)

        return True
