import pygame as pg
from config import *
from fw.functions import *
from fw.FwError import FwError

import math
from fw.GuiControl import GuiControl


#
#
#
class GuiSelect(GuiControl):

    # load image of archer
    archer_srf = pg.image.load("./images/gui/combobox_archer.png").convert()

    def __init__(self, params):

        params['background_color'] = params.get('background_color', THEME_SELECT_BACKGROUND_CLR)
        params['background_color_hover'] = params.get('background_color_hover', THEME_SELECT_BACKGROUND_HOVER_CLR)
        params['border_color'] = params.get('border_color', THEME_SELECT_BORDER_CLR)
        params['border_width'] = params.get('border_width', 1)

        super().__init__(params)

        # self.arr_text =  params['text']
        self.value_arr = params['value']
        self.selected_item_i = 0;



        # проверим кол--во слов в Combobox
        if len(self.value_arr) < 2 or len(self.value_arr) > 10:
            raise FwError

        getAppWnd().registerHandler_MOUSEMOTION(self)
        getAppWnd().registerHandler_MOUSEBUTTONDOWN(self)

        # обычный размер не в фокусе
        # может применятся если размер контрола меняется
        self.closed_rectsize = self.getSurface().get_rect()    # ex rect(0, 0, 56, 32)


    def setItem(self, item):
        # можно дописать функцию так чтобы передавать стринг,
        # и она будет искать подходящее занчение в списке
        if type(item) is int:
            self.selected_item_i = item

    def getValue(self):
        return self.value_arr[self.selected_item_i][1]

    def drawThis(self):

        # фон будет отрисован во весть размер поверхности
        # селект можкт быть открыт и меть больший размер
        if self.mouse_hover_flag and not self.is_focus:
            self.drawBackground(self.background_color_hover)

        else:
            # обычный фон
            self.drawBackground()

        # при открытом селекте бордер рисуется на максимум, на весь открытый селект
        self.drawBorder()

        #self_rectsize = self.surface.get_rect()




        X = self.closed_rectsize.w - 14
        Y = (self.closed_rectsize.h - 5) // 2
        Y = Y if Y // 2 else Y + 1


        archer_rect = pg.Rect(X, Y, 9, 5)  # 9,5 - size of archer

        # copy archer to control
        self.surface.blit(
            GuiSelect.archer_srf,
            archer_rect
        )

        # выведем текст
        txt = self.value_arr[self.selected_item_i][0]
        text_srf = getAppWnd().getFont('arial_16').render(txt, 1, HRGB(THEME_FONT_CLR))
        self.surface.blit(
            text_srf,
            (5, 1),
        )

        if self.is_focus:
            # линия разделяющая основной прямоугольник селекта и выпадающий спсиок
            # рисуется когда спсиок открыт
            pg.draw.line(
                self.surface,
                self.border_color,
                (0, self.closed_rectsize.bottom - 1),
                (self.closed_rectsize.right, self.closed_rectsize.bottom - 1),
            )

            # выведем строки в выпадающем спсике
            for i, value in enumerate(self.value_arr):
                text_srf = getAppWnd().getFont('arial_16').render(value[0], 1, HRGB(THEME_FONT_CLR))
                self.surface.blit(
                    text_srf,
                    (5, self.closed_rectsize.h + 1 + i * THEME_SELECT_STRING_HEIGHT)
                )

            pass




    def handleClickInFocus(self, event):
        # координата клика Y отвносительно открытого селекта
        Y = self.getOffsetInWindow(event.pos)[1]


        # координата клика Y отвносительно всплывающего спсика селекта
        Y = Y - self.closed_rectsize.h

        if Y < 0:
            # клик был в основной (верхней) части селекта
            # закрываем селект без изменений
            self.parent_wnd.sendMessage('WM_REQUEST_FREE_FOCUS', self)

        else:
            # клик был в нижней части селекта - выпадающем списке
            # устанвливаем новое значение селекта
            new_item_i = math.floor(Y / THEME_SELECT_STRING_HEIGHT)
            self.setItem(new_item_i)
            self.parent_wnd.sendMessage('WM_REQUEST_FREE_FOCUS', self)


        return False


    def setFocus(self):
        # функцию нельзя вызывать из данного класса, иначе может получится два контрола с фокусом одновременно
        # запрашивайте у родительского окна self.parent_wnd.sendMessage('WM_REQUEST_FOCUS')
        # оттуда вызывать setFocus

        self.is_focus = True

        self_offs = self.surface.get_offset()
        #self_rectsize = self.surface.get_rect()

        # местоположение вспомогательного окна (спсиок значений для выборов)
        # окна физически не существует
        # child_rect = pg.Rect(
        #     self_offs[0],
        #     self_offs[1] + self_rectsize.h + 1,
        #     self_rectsize.w,
        #     len(self.arr_text) * 22 + 2  # размер вспомогательного окна определяется числом слов
        # )

        # увеличим Surface
        # размер вспомогательного окна определяется числом слов + 1 пиксель на нижний бордер.
        new_rect = pg.Rect(
            self_offs[0],
            self_offs[1],
            self.closed_rectsize.w,
            self.closed_rectsize.h + len(self.value_arr) * THEME_SELECT_STRING_HEIGHT + 1
        )

        self.resize(new_rect)


        # params1 = {
        #     'tmp_class_name': "GuiSelectList",
        #     'creator_wnd': self,
        # }
        #
        # params2 = {
        #     'rect': child_rect,
        #     'text': self.arr_text,
        #     'value': self.value,
        # }


    def clearFocus(self):
        # функцию нельзя вызывать из данного класса,
        # запрашивайте у родительского окна self.parent_wnd.sendMessage('WM_REQUEST_FREE_FOCUS')
        # оттуда вызывать clearFocus

        self.resize(self.main_rect)
        self.is_focus = False

