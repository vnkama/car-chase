import pygame
from config import *
from GuiWindow import GuiWindow


class Game(GuiWindow):

    # pygame инициализируем как статический, т.к. CellWeed
    # грузит спрайты как статические, один набор спрайтов на все Weed
    # а статические переменные расчитываются раньше чем конструктора

    pygame.init()
    pygame.display.set_caption(MAIN_WND_TITLE)
    main_srf = pygame.display.set_mode((MAIN_WND_WIDTH, MAIN_WND_HEIGHT))

    def __init__(self):

        (w,h) = Game.main_srf.get_size()


        super().__init__({
            'name': 'Game class',
            'parent_obj': None,                     # родительского окна нет
            'rect': pygame.Rect(0,0,w,h),
            'bg_color':   MAIN_WND_BACKGROUND,
            'surface': Game.main_srf             #т.к. родительского окна у Game нет
                                                  # subsurface вызывать не откуда, то передаем главную повехность для него как surface
        })

        self.main_timer = pygame.time.Clock()
        self.is_mainloop_run = True

        pygame.font.init()
        #self.main_font = pygame.font.SysFont('Tahoma', CONTROL_WND_FONT_SIZE)

        #mousemotion окна-обработчики перемещения мыши
        self.arr_handlers_MOUSEMOTION = []


        #mousemotion окна-обработчики нажатия
        self.arr_handlers_MOUSEBUTTONDOWN = []


    def __del__(self):
        pygame.quit()


    #основной цикл приложения
    def run(self):
        while self.is_mainloop_run:
            self.main_timer.tick(FPS_RATE)

            self.handleEvents()
            self.update()
            self.draw()

            pygame.display.update()




    def handleEvents(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.is_mainloop_run = False

            elif event.type == pygame.MOUSEMOTION:
                # перебираем все зарегистрированные окна обработчики MOUSEMOTION
                for wnd in self.arr_handlers_MOUSEMOTION:
                    wnd.handle_MOUSEMOTION(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # перебираем все зарегистрированные окна обработчики MOUSEBUTTONDOWN
                for wnd in self.arr_handlers_MOUSEBUTTONDOWN:
                    wnd.handle_MOUSEBUTTONDOWN(event)


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
