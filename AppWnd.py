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

    #
    #
    #
    def __init__(self):


        # время последнего вызова функции draw. Переменная одна для всех режимов(play - pause - training - show итд) не
        # независымый учет для разных режимов не имеет смысла, тк.к физически одновременно может рисоваться на экране только один
        self.draw_last_call_rtime_ms_f = None

        # self.draw_next_call_rtime_ms_f = None
        self.draw_dt_rtime_ms_f = None


        # время последнего вызова training_update
        self.update_last_call_rtime_ms = None

        # интервал времени между текущим и предыдущим вызовами функции
        # задаетсмя настроками программы
        self.update_dt_rtime_ms_f = None




        # указатель на главное окно приложения
        setMainWnd(self)
        print(CONSOLE_CLR_ERROR + "AppWnd.__init__" + CONSOLE_CLR_RESET)

        (w, h) = g_main_srf.get_size()

        super().__init__({
            'name': 'fwAppWnd class',
            'parent_wnd': None,                     # родительского окна нет
            'rect': pg.Rect(0, 0, w, h),
            'background_color':   MAIN_WND_BACKGROUND,
            'surface': g_main_srf             #т.к. родительского окна у fwAppWnd нет
                                                 # subsurface вызывать не откуда, то передаем главную повехность для него как surface
        })

        # self.main_timer = pg.time.Clock()

        self.is_mainloop_run = True
        self.tool_wnd = None
        self.map_wnd = None


        pg.font.init()

        self.arr_fonts = {}

        # уставноим шрифты
        self.setFonts({
             # индекс строго в нижнем регистре
             'arial_16': pg.font.SysFont('Arial', 16),
             'arial_20': pg.font.SysFont('Arial', 20),
             'tahoma_20': pg.font.SysFont('Tahoma', 20),
        })




        # mousemotion окна-обработчики перемещения мыши
        self.arr_handlers_MOUSEMOTION = []

        # окна-обработчики нажатия кнопок мыши
        self.arr_handlers_MOUSEBUTTONDOWN = []

        # окна-обработчики нажатия кнопок клавиатуры
        self.arr_handlers_KEYDOWN = []

        # окна-обработчики окончания нажатия кнопок клавиатуры
        self.arr_handlers_KEYUP = []

        self.initMainWindows()

        # rtime - реальное время. используется для например для синхронизации FPS или опрса клавиатуры
        # gtime - это внутриигровое время, по сюжету игра может длится хоть 10 часов, а на компьютере прошло 5 минут
        # dt - временной интервал
        # постфиксы
        # _ms     милисекунды,
        # _sec    секунды
        # _f      флоат, фремя с плавающей точкой


        self.initTiming()


        self.state = None
        self.newGame()

    #
    # инициализируем основные окна,
    # это надо делать в AppWnd а не в  fwAppWnd, тк fwAppWnd не знает классов не из фреймворков типа ToolWnd итп
    #
    def initMainWindows(self):
        self.tool_wnd = ToolWnd({
            'parent_wnd': self
        })
        self.addChildWnd(self.tool_wnd)

        self.map_wnd = MapWnd({
            'parent_wnd': self,
            'tool_wnd': self.tool_wnd,
        })
        self.addChildWnd(self.map_wnd)


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

        elif msg == "WM_NEW_GAME":
            self.newGame()

        elif msg == "WM_PLAY":
            self.play()

        elif msg == "WM_PAUSE":
            self.pause()


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

                if self.state == 'APP_STATE_TRAINING_NEW' \
                        or self.state == 'APP_STATE_SHOW_PAUSE' \
                        or self.state == 'APP_STATE_TRAINING_PAUSE':


                    delay_ms = self.draw_last_call_rtime_ms_f - pg.time.get_ticks() + self.draw_dt_rtime_ms_f

                    if delay_ms > 0:
                        pg.time.wait(math.ceil(delay_ms))

                    #self.draw_last_call_rtime_ms_f = pg.time.get_ticks()    # += PAUSE_DRAW_DT


                    self.handleEvents()
                    self.draw()

                    pg.display.update()



                elif self.state == 'APP_STATE_TRAINING_PLAY':

                    cur_ms = pg.time.get_ticks()

                    update_delay_ms = update_next_ms - cur_ms
                    draw_delay_ms = draw_next_ms - cur_ms
                    handle_events_delay_ms = handle_events_next_ms - cur_ms

                    delay_ms = min(update_delay_ms, draw_delay_ms, handle_events_delay_ms)

                    if delay_ms > 0:
                        pg.time.wait(delay_ms)

                    now_ms = pg.time.get_ticks()

                    update_delay_ms = update_next_ms - now_ms
                    draw_delay_ms = draw_next_ms - now_ms
                    handle_events_delay_ms = draw_next_ms - now_ms

                    if handle_events_delay_ms <= 0:
                        self.handleEvents()
                        handle_events_next_ms = pg.time.get_ticks() + STATE_TRAINING_PLAY__HANDLE_EVENTS_INTERVAL_MS


                    if draw_delay_ms <= 0:
                        self.draw()
                        pg.display.update()
                        draw_next_ms = pg.time.get_ticks() + STATE_TRAINING_PLAY__UPDATE_INTERVAL_MS


                    if update_delay_ms <= 0:
                        self.update_training()



                elif self.state == 'APP_STATE_SHOW_PLAY':
                    # это не готово !
                    self.handleEvents()
                    self.update_4_show()
                    self.draw()
                    pg.display.update()

                else:
                    pass




                #self.main_timer.tick(DRAW_FPS)

                # self.handleEvents()
                # self.update()
                # self.draw()
                #
                # pg.display.update()

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


    def newGame(self):
        print(CONSOLE_CLR_GREEN + "AppWnd.newApp" + CONSOLE_CLR_RESET)

        self.state = 'APP_STATE_TRAINING_NEW'


        self.draw_last_call_rtime_ms_f = 0
        # self.draw_next_call_rtime_ms_f = 0

        self.draw_dt_rtime_ms_f = 1000 / TRAINING_PAUSE_DRAW_FPS

        # self.update_interval_ms = 16
        self.training_update_step = 0
        self.training_update_gtime_ms_f = 0.0






        self.sendMessageToChilds('WM_NEW_GAME')


    def play(self):
        if (
            self.state == 'APP_STATE_TRAINING_NEW' or
            self.state == 'APP_STATE_TRAINING_PAUSE'
        ):

            self.state = 'APP_STATE_TRAINING_PLAY'
            print("AppWnd.play")

            self.draw_dt_rtime_ms_f = 1000 / self.tool_wnd.selectTrainingDrawSpeed.getValue()


            # res['res']['update_fps'] - 1 : 1x обычная скороть расчет в реальном времени, 2 : 2x двойная
            # res['res']['update_fps'] * TRAINING_UPDATE_FPS    :   1x  :  60 расчетов в секунду
            # период перерасчета в реалаьном времени
            # запросим настройки по скорости обновления из tool_wnd
            res = {}
            self.update_last_call_rtime_ms = 0
            self.tool_wnd.sendMessage('WM_GET_TRAINING_PROPS', res)
            self.update_dt_rtime_ms_f = 1000 / (res['res']['update_fps'] * TRAINING_UPDATE_FPS)

            self.sendMessageToChilds('WM_PLAY')

        elif self.state == 'APP_STATE_SHOW_PAUSE':
            pass


    def pause(self):
        print("AppWnd.pause")
        if self.state == 'APP_STATE_TRAINING_PLAY':

            self.state = 'APP_STATE_TRAINING_PAUSE'
            self.sendMessageToChilds('WM_PAUSE')



    #
    #
    def handleEvents(self):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.is_mainloop_run = False

            elif event.type == pg.MOUSEMOTION:
                # перебираем все зарегистрированные окна обработчики MOUSEMOTION
                for wnd in self.arr_handlers_MOUSEMOTION:
                    wnd.handle_MOUSEMOTION(event)

            elif event.type == pg.MOUSEBUTTONDOWN:
                # перебираем все зарегистрированные окна обработчики MOUSEBUTTONDOWN

                # проверим есть ли контрол в фокусе
                if self.tool_wnd.focus_owner_wnd is not None:
                    # есть контрол в фокусе обрабатываем первым его его


                    if self.tool_wnd.focus_owner_wnd.handle_MOUSEBUTTONDOWN(event):

                        # контрол в фокусе обрабтали , обработаем все остальные
                        for wnd in self.arr_handlers_MOUSEBUTTONDOWN:
                            if wnd != self.tool_wnd.focus_owner_wnd:
                                if not wnd.handle_MOUSEBUTTONDOWN(event):
                                    break

                else:
                    for wnd in self.arr_handlers_MOUSEBUTTONDOWN:
                        if not wnd.handle_MOUSEBUTTONDOWN(event):
                            break

            elif event.type == pg.KEYDOWN:
                # перебираем все зарегистрированные окна обработчики KEYDOWN
                for wnd in self.arr_handlers_KEYDOWN:
                    wnd.handle_KEYDOWN(event)

            elif event.type == pg.KEYUP:
                # перебираем все зарегистрированные окна обработчики KEYDOWN
                for wnd in self.arr_handlers_KEYUP:
                    wnd.handle_KEYUP(event)


    #
    #
    #
    # def update(self):
    #     # super().update()  # fwWindow.update() пустой
    #
    #     cur_ms = pg.time.get_ticks()
    #     self.update_dt_ms = cur_ms - self.update_last_call_ms
    #     self.update_last_call_ms = cur_ms
    #
    #     self.sendMessageToChilds("WM_UPDATE")
    #
    #     # вывод времени . прошедшем с предыдущего вызова dt
    #     self.tool_wnd.sendMessage("WM_SET_TICKS", self.update_dt_ms)
    #     self.map_wnd.dt = self.update_dt_ms


    #
    # перерасчет всех объектов при обучении сети
    #
    def update_training(self):
        self.update_last_call_rtime_ms = pg.time.get_ticks()

        print(f'appWnd.update_training {self.update_last_call_rtime_ms}')

        # self.trainingupdate_next_ms = pg.time.get_ticks() + STATE_TRAINING_PLAY__DRAW_INTERVAL_MS

        self.sendMessageToChilds("WM_UPDATE_TRAINING")


    def update_show(self):
        # подкачка очередного кадра всех объектов из файла в режиме show
        self.update_last_call_rtime_ms = pg.time.get_ticks()
        print(f'appWnd.update_show {self.update_last_call_rtime_ms}')

        self.sendMessageToChilds("WM_UPDATE_SHOW")


    def draw(self):
        # super().draw()      #fwWindow
        self.draw_last_call_rtime_ms_f = pg.time.get_ticks()

        self.sendMessageToChilds('WM_DRAW')





    # добавим обработчик перемещения мыши
    def registerHandler_MOUSEMOTION(self,wnd):
        self.arr_handlers_MOUSEMOTION.append(wnd)

    def unregHandler_MOUSEMOTION(self,wnd):
        self.arr_handlers_MOUSEMOTION.remove(wnd)



    def registerHandler_MOUSEBUTTONDOWN(self, wnd):
        self.arr_handlers_MOUSEBUTTONDOWN.append(wnd)

    def unregHandler_MOUSEBUTTONDOWN(self, wnd):
        self.arr_handlers_MOUSEBUTTONDOWN.remove(wnd)



    def registerHandler_KEYDOWN(self, wnd):
        self.arr_handlers_KEYDOWN.append(wnd)

    def unregHandler_KEYDOWN(self, wnd):
        self.arr_handlers_KEYDOWN.remove(wnd)



    def registerHandler_KEYUP(self, wnd):
        self.arr_handlers_KEYUP.append(wnd)

    def unregHandler_KEYUP(self, wnd):
        self.arr_handlers_KEYUP.remove(wnd)
        #
        #
        #

    def getFont(self, name):
        return self.arr_fonts.get(name.lower(), self.arr_fonts['tahoma_20'])

    #
    #
    #
    def setFonts(self, arr_fonts):
        self.arr_fonts = arr_fonts
