#import pygame as pg
from config import *
from fw.functions import *
from fw.FwError import FwError

from fw.fwWindow import fwWindow
from fw.GuiSelectList import GuiSelectList


#
#
#
class fwToolWnd(fwWindow):

    def __init__(self, params):

        params['rect'] = CONTROL_WND_RECT
        params['background_color'] = THEME_WINDOW_BACKGROUND
        params['name'] = 'ControlWnd'

        super().__init__(params)        # parent - fwWindow

        self.tmp_child_wnd = None   # временное окно для всплывашек открытого комбобокса итд


    def sendMessage(self, msg, param1=None, param2=None):

        if msg == 'WM_CREATE_TMP_CHILD':
            self.createTmpChildWnd(param1, param2)

        elif msg == 'WM_CLOSE_TMP_CHILD':
            self.closeTmpChild(param1)

        elif msg == 'WM_NEW_GAME':
            self.newGame()

        elif msg == 'WM_PLAY':
            self.play()

        elif msg == 'WM_PAUSE':
            self.pause()

        elif msg == 'WM_UPDATE':
            pass




    #
    #
    #
    def createTmpChildWnd(self,params,params_new_wnd):

        if (self.tmp_child_wnd is not None ):
            # создание второо временного окна пока не закрыто первое запрещено
            return

        self.tmp_child_wnd_params = params

        if (self.tmp_child_wnd_params['tmp_class_name']  == "GuiSelectList"):
            params_new_wnd['parent_wnd'] = self
            self.tmp_child_wnd = GuiSelectList(params_new_wnd)



    #
    # закрыть дочернее окно
    #
    def closeTmpChild(self,value):
        #value - возвращенное значение

        if (self.tmp_child_wnd is None ):
            raise FwError

        self.tmp_child_wnd.desctructor()
        del self.tmp_child_wnd
        self.tmp_child_wnd = None

        if (value is not None):
            self.tmp_child_wnd_params['creator_wnd'].setValue(value)


    #
    #
    #
    def drawChildWnds(self):
        super().drawChildWnds()

        # рисуем временное окно если есть
        if (self.tmp_child_wnd is not None):
            self.tmp_child_wnd.draw()


    def quit_onButton(self):
        getAppWnd().sendMessage('WM_QUIT_APP')

    def new_onButton(self):
        getAppWnd().sendMessage('WM_NEW_GAME')


    def play_onButton(self):
        getAppWnd().sendMessage('WM_PLAY')

    def pause_onButton(self):
        getAppWnd().sendMessage('WM_PAUSE')


    def newGame(self):
        self.btnNew.disable()
        self.btnPause.disable()

    def play(self):
        self.btnNew.disable()
        self.btnPlay.disable()
        self.btnPause.enable()
        self.semaphorRun.setColor('green')

    def pause(self):
        self.btnNew.enable()
        self.btnPlay.enable()
        self.btnPause.disable()
        self.semaphorRun.setColor('red')
