import pygame as pg

# порядок загрзки pygame
# 1. импортируем InitPygame, где вызывается pg.init(),
# 2. подключаем разные модули, использующие pygame
# 3. при подключении модулей во многих из них обрабатываются статические переменные, втч использующие pygame для загрузки изображений
# 4. только после этого обрабатываются __init__
from InitPygame import *

from config import *
from fw.functions import *
from fw.FwError import FwError

#import h5py
import math
import traceback
from fw.fwWindow import fwWindow

from Series import Series
from ToolWnd import ToolWnd
from MapWnd import MapWnd



#
#
#
class AppWnd(fwWindow):
    """
    Класс AppWnd - главное окно всего приложения.
    """

    def __init__(self):
        print(CONSOLE_CLR_ERROR + "AppWnd.__init__" + CONSOLE_CLR_RESET)


        # время последнего вызова функции draw. Переменная одна для всех режимов(play - pause - training - show итд)
        # независымый учет для разных режимов не имеет смысла, тк.к физически одновременно может рисоваться на экране только один режим
        self.draw_last_call_rtime_ms_f = None

        # заданный нами интервал между вызовами draw
        # фактический интервал может быть больше, если программа тормозит
        self.draw_dt_rtime_ms_f = None

        # момент времени последнего вызова update
        self.update_last_call_rtime_ms_f = None

        # предварительо заданный интервал времени между текущим и предыдущим вызовами функции
        # задается настройками программы
        # фактический интервал может быть больше, если программа тормозит
        self.update_dt_rtime_ms_f = None

        self.handleEvents_last_call_rtime_ms_f = None
        self.handleEvents_dt_rtime_ms_f = None


        # установим указатель на главное окно приложения
        setMainWnd(self)

        # (w, h) = g_main_srf.get_size()

        super().__init__({
            'name': 'fwAppWnd class',
            'type' : 'main',                        # главное окно приложения
            'parent_wnd': None,                     # родительского окна у главного нет
            # 'rect': pg.Rect(0, 0, w, h),
            'rect': pg.Rect((0, 0), g_main_srf.get_size()),
            'background_color':   MAIN_WND_BACKGROUND,
            'surface': g_main_srf,                  #родительского окна у fwAppWnd нет для главного окна используетя глобальная поверхность pygame
        })

        self.is_mainloop_run = True
        self.Tool_wnd = None
        self.Map_wnd = None
        self.Series = None


        # уставноим шрифты
        self.arr_fonts = {}

        self.setFonts({
             # индекс строго в нижнем регистре
            'arial_14': pg.font.SysFont('Arial', 14),
            'arial_16': pg.font.SysFont('Arial', 16),
             'arial_20': pg.font.SysFont('Arial', 20),
             'tahoma_20': pg.font.SysFont('Tahoma', 20),
        })


        # обработчики перемещения событий мыши и клавиатуры
        # класс обработчик должен наследоваться от fwWindow
        self.Mousemotion_handlers_arr = []
        self.MouseButtonDown_handlers_arr = []
        self.KeyDown_handlers_arr = []
        self.KeyUp_handlers_arr = []



        self.Tool_wnd = ToolWnd({
            'type': 'normal',  # обычное окно
            'parent_wnd': self,
        })
        self.addChildWnd(self.Tool_wnd)



        self.Series = Series({
            'type' : 'no_surface',      # у Series нет графики
            'parent_wnd': self,
            'Tool_wnd': self.Tool_wnd,
            'parent_surface': self.surface,
        })
        self.addChildWnd(self.Series)




        self.initTiming()


        self.state = None
        self.newSeries()




    #
    #
    #
    def __del__(self):
        pg.quit()


    def initTiming(self):
        #############################
        # УДАЛИТЬ

        self.update_last_call_ms = 0
        self.update_dt_ms = 0

        # self.training_draw_call_rtime_ms = None
        # self.training_draw_dt_rtime_ms_f = None


        # self.draw_last_call_ms = 0
        # self.draw_interval_ms = 16
        #############################



    def sendMessage(self, msg, param1=None, param2=None):

        #super().sendMessage(self, code, param1, param2)    # fwWindow.sendMessage - пустой метод, вызывать нет смысла

        if msg == "WM_QUIT_APP":
            self.quitApp()

        elif msg == "WM_NEW_SERIES":
            self.resetSeries()

        elif msg == "WM_PLAY":
            self.play()

        elif msg == "WM_PAUSE":
            self.pause()

        elif msg == 'WM_END_SERIES':
            self.endSeries()



    #
    # основной цикл приложения
    #

    def run(self):

        update_next_ms = 0
        draw_next_ms = 0
        handle_events_next_ms = 0


        try:

            # необходимо , т.к. иначе при первом показе не просчитаны некоторые параметры (например координаты сенсоров)
            self.update()

            while self.is_mainloop_run:




                now = pg.time.get_ticks()

                handle_events_next_call = self.handleEvents_last_call_rtime_ms_f + self.handleEvents_dt_rtime_ms_f
                update_next_call = self.update_last_call_rtime_ms_f + self.update_dt_rtime_ms_f
                draw_next_call = self.draw_last_call_rtime_ms_f + self.draw_dt_rtime_ms_f

                if handle_events_next_call <= min(update_next_call, draw_next_call):
                    delay_ms = int(handle_events_next_call - now)
                    if delay_ms > 0:
                        pg.time.wait(delay_ms)
                    self.handleEvents_last_call_rtime_ms_f = pg.time.get_ticks()


                    self.handleEvents()

                elif update_next_call <= min(handle_events_next_call, draw_next_call):
                    delay_ms = int(update_next_call - now)
                    if delay_ms > 0:
                        pg.time.wait(delay_ms)
                    self.update_last_call_rtime_ms_f = pg.time.get_ticks()
                    self.update()

                else:
                    delay_ms = int(draw_next_call - now)
                    if delay_ms > 0:
                        pg.time.wait(delay_ms)
                    self.draw_last_call_rtime_ms_f = pg.time.get_ticks()
                    self.draw()

                pg.display.update()



        except FwError as e:
            print("\033[35m\033[1mgame.py except FwError")
            e.out()
            traceback.print_exc()

    #
    #
    #
    def quitApp(self):
        self.is_mainloop_run = False
        print(CONSOLE_CLR_RED + "AppWnd.quitApp" + CONSOLE_CLR_RESET)


    #
    # обрабатывае нажатие кнопки NEW
    # принудительно уничтожить
    #
    def resetSeries(self):
        self.Series.destroySeries()
        self.newSeries()



    def newSeries(self):
        print(CONSOLE_CLR_GREEN + "AppWnd.newApp" + CONSOLE_CLR_RESET)

        self.state = 'APP_STATE_TRAINING_NEW'


        ######

        now = pg.time.get_ticks()

        self.handleEvents_last_call_rtime_ms_f = now
        self.handleEvents_dt_rtime_ms_f = 1000 / TRAINING_PAUSE_HANDLE_EVENTS_FPS

        self.update_last_call_rtime_ms_f = now
        self.update_dt_rtime_ms_f = 1000 / TRAINING_PAUSE_UPDATE_FPS

        self.draw_last_call_rtime_ms_f = now
        self.draw_dt_rtime_ms_f = 1000 / TRAINING_PAUSE_DRAW_FPS


        self.Tool_wnd.newSeries()
        self.Series.newSeries()




    def endSeries(self):
        self.state = 'APP_STATE_TRAINING_END'
        print("AppWnd.endSeries endSeries")

        self.Tool_wnd.endSeries()

        self.handleEvents_dt_rtime_ms_f = 1000 / TRAINING_PAUSE_HANDLE_EVENTS_FPS
        self.update_dt_rtime_ms_f = 1000 / TRAINING_PAUSE_UPDATE_FPS
        self.draw_dt_rtime_ms_f = 1000 / TRAINING_PAUSE_DRAW_FPS



    def play(self):
        if (
            self.state == 'APP_STATE_TRAINING_NEW' or
            self.state == 'APP_STATE_TRAINING_PAUSE'
        ):

            print("AppWnd.training play")
            self.state = 'APP_STATE_TRAINING_PLAY'

            # res['res']['update_fps'] - 1 : 1x обычная скороть расчет в реальном времени, 2 : 2x двойная
            # res['res']['update_fps'] * TRAINING_UPDATE_FPS : 1x  :  60 расчетов в секунду
            # период перерасчета в реалаьном времени
            # запросим настройки по скорости обновления из Tool_wnd
            res = {}
            self.Tool_wnd.sendMessage('WM_GET_TRAINING_PROPS', res)

            self.handleEvents_dt_rtime_ms_f = 1000 / TRAINING_PLAY_HANDLE_EVENTS_FPS
            self.update_dt_rtime_ms_f = 1000 / res['res']['update_fps']
            self.draw_dt_rtime_ms_f = 1000 / res['res']['draw_fps']

            self.Tool_wnd.play()


        elif self.state == 'APP_STATE_SHOW_PAUSE':
            self.state = 'APP_STATE_SHOW_PLAY'




    def pause(self):
        if self.state == 'APP_STATE_TRAINING_PLAY':
            print("AppWnd.training pause")
            self.state = 'APP_STATE_TRAINING_PAUSE'

            self.handleEvents_dt_rtime_ms_f = 1000 / TRAINING_PAUSE_HANDLE_EVENTS_FPS
            self.update_dt_rtime_ms_f = 1000 / TRAINING_PAUSE_UPDATE_FPS
            self.draw_dt_rtime_ms_f = 1000 / TRAINING_PAUSE_DRAW_FPS

            self.Tool_wnd.pause()


        elif self.state == 'APP_STATE_SHOW_PLAY':
            print("AppWnd.training pause")
            self.state = 'APP_STATE_SHOW_PAUSE'



    def handleEvents(self):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.is_mainloop_run = False

            elif event.type == pg.MOUSEMOTION:
                # перебираем все зарегистрированные окна обработчики MOUSEMOTION
                for wnd in self.Mousemotion_handlers_arr:
                    wnd.handle_MouseMotion(event)

            elif event.type == pg.MOUSEBUTTONDOWN:
                # перебираем все зарегистрированные окна обработчики MOUSEBUTTONDOWN

                # проверим есть ли контрол в фокусе
                if self.Tool_wnd.focus_owner_wnd is not None:
                    # есть контрол в фокусе обрабатываем первым его его


                    if self.Tool_wnd.focus_owner_wnd.handle_MouseButtonDown(event):

                        # контрол в фокусе обрабтали , обработаем все остальные
                        for wnd in self.MouseButtonDown_handlers_arr:
                            if wnd != self.Tool_wnd.focus_owner_wnd:
                                if not wnd.handle_MouseButtonDown(event):
                                    break

                else:
                    for wnd in self.MouseButtonDown_handlers_arr:
                        if not wnd.handle_MouseButtonDown(event):
                            break

            elif event.type == pg.KEYDOWN:
                # перебираем все зарегистрированные окна обработчики KEYDOWN
                for wnd in self.KeyDown_handlers_arr:
                    wnd.handle_KeyDown(event)

            elif event.type == pg.KEYUP:
                # перебираем все зарегистрированные окна обработчики KEYDOWN
                for wnd in self.KeyUp_handlers_arr:
                    wnd.handle_KeyUp(event)


    def update(self):
        if self.state == 'APP_STATE_TRAINING_PLAY':
            self.Series.updateTraining()

        elif self.state == 'APP_STATE_SHOW_PLAY':
            self.Series.updateShow()





    def draw(self):
        # super().draw()      #fwWindow

        # у AppWnd нет собственной графики, рисоавть нечего
        # вызовем
        self.Tool_wnd.draw()
        self.Series.draw()





    # добавим обработчик перемещения мыши
    def registerHandler_MOUSEMOTION(self,wnd):
        self.Mousemotion_handlers_arr.append(wnd)

    def unregHandler_MOUSEMOTION(self,wnd):
        self.Mousemotion_handlers_arr.remove(wnd)



    def registerHandler_MOUSEBUTTONDOWN(self, wnd):
        self.MouseButtonDown_handlers_arr.append(wnd)

    def unregHandler_MOUSEBUTTONDOWN(self, wnd):
        self.MouseButtonDown_handlers_arr.remove(wnd)



    def registerHandler_KEYDOWN(self, wnd):
        self.KeyDown_handlers_arr.append(wnd)

    def unregHandler_KEYDOWN(self, wnd):
        self.KeyDown_handlers_arr.remove(wnd)



    def registerHandler_KEYUP(self, wnd):
        self.KeyUp_handlers_arr.append(wnd)

    def unregHandler_KEYUP(self, wnd):
        self.KeyUp_handlers_arr.remove(wnd)
        #
        #
        #

    def getFont(self, name):
        return self.arr_fonts.get(name.lower(), self.arr_fonts['tahoma_20'])


    def setFonts(self, arr_fonts):
        self.arr_fonts = arr_fonts
