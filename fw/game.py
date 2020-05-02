import pygame as pg
from config import *
from fw.GuiWindow import GuiWindow

from fw.functions import *


class Game(GuiWindow):

    # pygame инициализируем как статический, т.к. CellWeed
    # грузит спрайты как статические, один набор спрайтов на все Weed
    # а статические переменные расчитываются раньше чем конструктора

    pg.init()
    pg.display.set_caption(MAIN_WND_TITLE)
    main_srf = pg.display.set_mode((MAIN_WND_WIDTH, MAIN_WND_HEIGHT))

    def __init__(self):
        (w,h) = Game.main_srf.get_size()


        super().__init__({
            'name': 'Game class',
            'parent_obj': None,                     # родительского окна нет
            'rect': pg.Rect(0,0,w,h),
            'bg_color':   MAIN_WND_BACKGROUND,
            'surface': Game.main_srf             #т.к. родительского окна у Game нет
                                                 # subsurface вызывать не откуда, то передаем главную повехность для него как surface
        })

        self.main_timer = pg.time.Clock()
        self.is_mainloop_run = True

        pg.font.init()
        #self.main_font = pygame.font.SysFont('Tahoma', CONTROL_WND_FONT_SIZE)

        #уставноим шрифты
        setFonts({
             #индекс строго в нижнем регистре
             'arial_16': pg.font.SysFont('Arial', 16),
             'arial_20': pg.font.SysFont('Arial', 20),
             'tahoma_20': pg.font.SysFont('Tahoma', 20),
        })


        #mousemotion окна-обработчики перемещения мыши
        self.arr_handlers_MOUSEMOTION = []

        #окна-обработчики нажатия кнопок мыши
        self.arr_handlers_MOUSEBUTTONDOWN = []

        #окна-обработчики нажатия кнопок клавиатуры
        self.arr_handlers_KEYDOWN = []

        #окна-обработчики окончания нажатия кнопок клавиатуры
        self.arr_handlers_KEYUP = []


    def __del__(self):
        pg.quit()


    #основной цикл приложения
    def run(self):
        while self.is_mainloop_run:
            self.main_timer.tick(FPS_RATE)

            self.handleEvents()
            self.update()
            self.draw()

            pg.display.update()




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



    #def update(self):
        #цикл по всем графическим объектам


    def draw(self):
        super().draw()      #GuiWindow


    def registerHandler_MOUSEMOTION(self,wnd):
        #добавим обработчик перемещения мыши
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
