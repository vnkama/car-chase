import pygame as pg
from config import *
from fw.functions import *
# from fw.FwError import FwError

from fw.fwWindow import fwWindow
from fw.GuiButton import GuiButton
from fw.GuiSemaphor import GuiSemaphor
from fw.GuiSelect import GuiSelect
from fw.GuiLabel import GuiLabel

#
#
#
class ToolWnd(fwWindow):

    def __init__(self, params):

        params['rect'] = TOOL_WND_RECT
        params['background_color'] = THEME_BACKGROUND_CLR
        params['name'] = 'ControlWnd'

        super().__init__(params)        # parent - fwWindow

        self.tmp_child_wnd = None   # временное окно для всплывашек открытого комбобокса итд

        self.tmp_child_wnd_params = None
        self.focus_owner_wnd = None
        ############################################

        self.addChildWnd(GuiButton({
            'name': 'button-quit',
            'text': 'Quit',
            'parent_wnd':self,
            'rect': pg.Rect(220,20,56,32),
            'on_button_func': self.quit_onButton
        }))

        ############################################

        self.btnNew = self.addChildWnd(GuiButton({
            'name': 'button-start',
            'text': 'New',
            'parent_wnd': self,
            'rect': pg.Rect(10, 60, 60, 32),
            'on_button_func': self.new_onButton
        }))

        self.btnPlay = self.addChildWnd(GuiButton({
            'name': 'button-play',
            'text': 'Play',
            'parent_wnd': self,
            'rect': pg.Rect(74, 60, 60, 32),
            'on_button_func': self.play_onButton
        }))

        self.btnPause = self.addChildWnd(GuiButton({
            'name': 'button-pause',
            'text': 'Pause',
            'parent_wnd': self,
            'rect': pg.Rect(138, 60, 60, 32),
            'on_button_func': self.pause_onButton
        }))

        self.semaphorRun = self.addChildWnd(GuiSemaphor({
            'parent_wnd': self,
            'rect': pg.Rect(200, 60, 40, 32),
            'radius': 8,
            # 'on_button_func': self.pause_onButton
        }))

        #-------------------------------------

        self.addChildWnd(GuiLabel({
            'parent_wnd': self,
            'rect': pg.Rect(10, 120, 64, 22),
            'text': 'Training:',
        }))

        self.addChildWnd(GuiLabel({
            'parent_wnd': self,
            'rect': pg.Rect(10, 150, 60, 22),
            'text': 'Update:',
        }))

        self.selectTrainingUpdateSpeed = self.addChildWnd(GuiSelect({
            'name': 'combo-test',
            'value': [
                ("x1", 60),
                ("x2", 120),
                ("x5", 300),
                ("x10", 600),
            ],
            'parent_wnd': self,
            'rect': pg.Rect(65, 150, 80, 22),
        }))

        self.selectTrainingUpdateSpeed.setSelectedItemByText('x10')

        ##########

        self.addChildWnd(GuiLabel({
            'parent_wnd': self,
            'rect': pg.Rect(160, 150, 60, 22),
            'text': 'Draw:',
        }))

        self.selectTrainingDrawSpeed = self.addChildWnd(GuiSelect({
            'name': 'combo-test',
            'value': [
                ("60 fps", 60),
                ("30 fps", 30),
                ("10 fps", 10),
                ("5 fps", 5),
                ("1 fps", 1),
            ],
            'parent_wnd': self,
            'rect': pg.Rect(200, 150, 80, 22),
        }))

        # -------------------------------------

        self.addChildWnd(GuiLabel({
            'parent_wnd': self,
            'rect': pg.Rect(10, 200, 60, 22),
            'text': 'Show:',
        }))

        ############################################

        self.addChildWnd(GuiLabel({
            'parent_wnd': self,
            'rect': pg.Rect(8, 300, 60, 32),
            'text': 'Param 1:',
        }))



        self.lbl_speed = GuiLabel({
            'parent_wnd': self,
            'rect': pg.Rect(80, 300, 200, 32),
            'text': '0',
        })
        self.addChildWnd(self.lbl_speed)

        ############################################

        self.addChildWnd(GuiLabel({
            'parent_wnd': self,
            'rect': pg.Rect(8, 332, 100, 32),
            'text': 'ticks:',
        }))


        self.lbl_ticks = GuiLabel({
            'parent_wnd': self,
            'rect': pg.Rect(80, 332, 100, 32),
            'text': '0',
        })
        self.addChildWnd(self.lbl_ticks)

        ############################################

        self.addChildWnd(GuiLabel({
            'parent_wnd': self,
            'rect': pg.Rect(8, 364, 100, 32),
            'text': 'Party:',
        }))

        self.lbl_party = GuiLabel({
            'parent_wnd': self,
            'rect': pg.Rect(80, 364, 100, 32),
            'text': '0',
        })
        self.addChildWnd(self.lbl_party)



    def sendMessage(self, msg, param1=None, param2=None):
        # fwWindow.sendMessage() - не определен

        if msg == 'WM_REQUEST_FOCUS':
            self.requestFocus(param1)

        elif msg == 'WM_REQUEST_FREE_FOCUS':
            self.onRequestFreeFocus(param1)

        elif msg == 'WM_GET_TRAINING_PROPS':
            self.getTrainingProps(param1)


        elif msg == 'WM_PAUSE':
            self.pause()

        elif msg == 'WM_SET_PARAM_1':
            self.lbl_speed.setText(param1)

        elif msg == 'WM_SET_TICKS':
            self.lbl_ticks.setText(param1)

        elif msg == 'WM_SET_PARTY':
            self.lbl_party.setText(param1)

        else:
            # если не обработали здесь то отправляем наверх
            super().sendMessage(msg, param1, param2)




    def getTrainingProps(self, param1):
        param1['res'] = {
            'update_fps': self.selectTrainingUpdateSpeed.getValue(),
            'draw_fps': self.selectTrainingDrawSpeed.getValue(),
        }


    def requestFocus(self, focus_new_owner_wnd):
        # кто то из чайлдов заправшивает фокус
        # сбросим всем остальным фокус

        if self.focus_owner_wnd:
            # уже есть держатель фокуса
            # отберем у него фокус
            self.focus_owner_wnd.clearFocus()
            self.focus_owner_wnd = None


        self.focus_owner_wnd = focus_new_owner_wnd
        self.focus_owner_wnd.setFocus()


    def onRequestFreeFocus(self, focus_owner_wnd):
        # пришел запрос на закрытие окна
        if self.focus_owner_wnd is not None and self.focus_owner_wnd == focus_owner_wnd:
            self.focus_owner_wnd.clearFocus()
            self.focus_owner_wnd = None


    def draw(self):
        self.drawThis()

        if self.focus_owner_wnd is None:
            # нет контролов в фокусе,
            self.sendMessageToChilds('WM_DRAW')

        else:
            # есть контрол в фокусе,
            for child_wnd in self.child_objects:
                if self.focus_owner_wnd != child_wnd:
                    child_wnd.sendMessage('WM_DRAW')

            # контрол под фокусом рисуем последним, чтобы он был верхним
            self.focus_owner_wnd.sendMessage('WM_DRAW')



    def quit_onButton(self):
        getAppWnd().sendMessage('WM_QUIT_APP')

    def new_onButton(self):
        getAppWnd().sendMessage('WM_NEW_SERIES')


    def play_onButton(self):
        getAppWnd().sendMessage('WM_PLAY')

    def pause_onButton(self):
        getAppWnd().sendMessage('WM_PAUSE')


    def newSeries(self):
        self.btnNew.disable()
        self.btnPause.disable()


    def play(self):
        self.btnNew.disable()
        self.btnPlay.disable()
        self.btnPause.enable()
        self.semaphorRun.setColor('green')

        self.selectTrainingUpdateSpeed.disable()
        self.selectTrainingDrawSpeed.disable()

    def pause(self):
        self.btnNew.enable()
        self.btnPlay.enable()
        self.btnPause.disable()
        self.semaphorRun.setColor('red')

        self.selectTrainingUpdateSpeed.enable()
        self.selectTrainingDrawSpeed.enable()

    def endSeries(self):
        self.btnNew.enable()
        self.btnPlay.disable()
        self.btnPause.disable()
        self.semaphorRun.setColor('red')

        self.selectTrainingUpdateSpeed.disable()
        self.selectTrainingDrawSpeed.disable()
