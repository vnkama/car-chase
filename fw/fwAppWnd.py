import pygame as pg
from config import *
from fw.functions import *
from fw.FwError import FwError

#import h5py
import traceback
from fw.fwWindow import fwWindow





#
#
#
class fwAppWnd(fwWindow):




    # pygame инициализируем как статический, т.к. CellWeed
    # грузит спрайты как статические, один набор спрайтов на все Weed
    # а статические переменные расчитываются раньше чем запускается до __init__

    pg.init()
    pg.display.set_caption(MAIN_WND_TITLE)

    if (MAIN_WND_FULLSCREEN):
        #вариант для FULLSCREEN
        main_srf = pg.display.set_mode(
            #(1600, 900),
            (MAIN_WND_WIDTH, MAIN_WND_HEIGHT),
            pg.FULLSCREEN
        )

    else:
        # вариант для запуска в окне
        main_srf = pg.display.set_mode(
            (MAIN_WND_WIDTH, MAIN_WND_HEIGHT)
        )


    #
    #
    #
    def __init__(self):

        # укахатель на главное окно приложения
        setMainWnd(self)
        print(CONSOLE_CLR_ERROR + "AppWnd.__init__" + CONSOLE_CLR_RESET)

        (w,h) = fwAppWnd.main_srf.get_size()

        super().__init__({
            'name': 'fwAppWnd class',
            'parent_wnd': None,                     # родительского окна нет
            'rect': pg.Rect(0,0,w,h),
            'background_color':   MAIN_WND_BACKGROUND,
            'surface': fwAppWnd.main_srf             #т.к. родительского окна у fwAppWnd нет
                                                 # subsurface вызывать не откуда, то передаем главную повехность для него как surface
        })

        self.main_timer = pg.time.Clock()
        self.is_mainloop_run = True

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

    # # определить в классе наследнике
    # def initMainWindows(self):
    #     pass



    #
    #
    #
    def __del__(self):
        pg.quit()


    def sendMessage(self, code,param1=None,param2=None):
        #super().sendMessage(self, code, param1, param2)    #fwWindow.sendMessage - пустой метод, вызывать ненужно

        if (code == "WM_QUIT_APP"):
            self.quitApp()

        elif (code == "WM_NEW_GAME"):
            self.newGame()


    #
    #основной цикл приложения
    #
    def run(self):

        try:

            while self.is_mainloop_run:
                self.main_timer.tick(FPS_RATE)

                self.handleEvents()
                self.update()
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



    def newGame(self):
        print(CONSOLE_CLR_GREEN + "AppWnd.newApp" + CONSOLE_CLR_RESET)
        self.state = 'APP_STATE_NEW'

        self.sendMessageToChilds("WM_NEW_GAME")





    #
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
                for wnd in self.arr_handlers_MOUSEBUTTONDOWN:
                    wnd.handle_MOUSEBUTTONDOWN(event)

            elif event.type == pg.KEYDOWN:
                # перебираем все зарегистрированные окна обработчики KEYDOWN
                for wnd in self.arr_handlers_KEYDOWN:
                    wnd.handle_KEYDOWN(event)

            elif event.type == pg.KEYUP:
                # перебираем все зарегистрированные окна обработчики KEYDOWN
                for wnd in self.arr_handlers_KEYUP:
                    wnd.handle_KEYUP(event)



    # def update(self):
    #     pass

    # def draw(self):
    #     super().draw()      #fwWindow


    # добавим обработчик перемещения мыши
    def registerHandler_MOUSEMOTION(self,wnd):
        self.arr_handlers_MOUSEMOTION.append(wnd)

    def unregHandler_MOUSEMOTION(self,wnd):
        self.arr_handlers_MOUSEMOTION.remove(wnd)



    def registerHandler_MOUSEBUTTONDOWN(self,wnd):
        self.arr_handlers_MOUSEBUTTONDOWN.append(wnd)

    def unregHandler_MOUSEBUTTONDOWN(self,wnd):
        self.arr_handlers_MOUSEBUTTONDOWN.remove(wnd)



    def registerHandler_KEYDOWN(self,wnd):
        self.arr_handlers_KEYDOWN.append(wnd)

    def unregHandler_KEYDOWN(self,wnd):
        self.arr_handlers_KEYDOWN.remove(wnd)



    def registerHandler_KEYUP(self,wnd):
        self.arr_handlers_KEYUP.append(wnd)

    def unregHandler_KEYUP(self,wnd):
        self.arr_handlers_KEYUP.remove(wnd)



    #
    #
    #
    def getFont(self, name):
        # global g_arr_fonts;
        # return g_arr_fonts.get(name.lower(), g_arr_fonts['tahoma_20'])
        return self.arr_fonts.get(name.lower(), self.arr_fonts['tahoma_20'])

    #
    #
    #
    def setFonts(self,arr_fonts):
        self.arr_fonts = arr_fonts
