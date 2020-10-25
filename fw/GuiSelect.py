import pygame as pg
from config import *
from fw.functions import *
from fw.FwError import FwError

from fw.GuiControl import GuiControl


#
#
#
class GuiSelect(GuiControl):

    #load image of archer
    archer_srf = pg.image.load("./images/gui/combobox_archer.png").convert()

    def __init__(self,params):

        params['background_color'] = params.get('background_color',THEME_COMBOBOX_BACKGROUND)
        params['background_color_hover'] = params.get('background_color_hover',THEME_COMBOBOX_BACKGROUND_HOVER)
        params['border_color'] = params.get('border_color',THEME_COMBOBOX_BORDER_COLOR)
        params['border_width'] = params.get('border_width',1)

        super().__init__(params)

        self.arr_text =  params['text']
        self.value = params['value']

        #проверим кол--во слов в Combobox
        if len(self.arr_text) < 2 or len(self.arr_text) > 10:
            raise FwError

        getAppWnd().registerHandler_MOUSEMOTION(self)
        getAppWnd().registerHandler_MOUSEBUTTONDOWN(self)



    def drawThis(self):
        if not self.mouse_hover_flag:
            self.drawBackground()
        else:
            self.drawBackground(self.background_color_hover)

        self.drawBorder()

        X = self.surface.get_rect().w-14
        Y = (self.surface.get_rect().h-5)//2
        Y = Y if Y//2 else Y+1

        archer_rect = pg.Rect(X,Y,9,5)      #9,5 - size of archer

        #copy archer to control
        self.surface.blit(
            GuiSelect.archer_srf,
            archer_rect)

        # output textvalue
        text_srf = getAppWnd().getFont('arial_16').render(self.value, 1, HRGB(THEME_FONT_CLR))
        self.surface.blit(
            text_srf,
            (5, 1)
        )



    def handle_MOUSEBUTTONDOWN(self, event):
        if event.button == 1:
            #LB have pressed

            if self.isPointInWindow(event.pos):
                #print("LB in rect")

                # LB have pressed in area of combo

                if not self.isFocus():
                    # не в фокусе, берем фокус будем открываться
                    #get focus
                    #self.setFocus(1)
                    self.open()

                else:
                    #LB have clicked in opened combo
                    #end focus
                    pass
                    #self.setFocus(0)



            else:
                # LB have pressed out of area of combo
                # reset focus
                if self.isFocus():
                    self.setFocus(0)

    def open(self):
        #открываем селект
        self.is_focus = 1

        self_rectsize = self.surface.get_rect()

        # местоположение вспомогательного окна (спсиок значений для выборов)
        # окна физически не существует
        # child_rect = pg.Rect(
        #     self_offs[0],
        #     self_offs[1] + self_rectsize.h + 1,
        #     self_rectsize.w,
        #     len(self.arr_text) * 22 + 2  # размер вспомогательного окна определяется числом слов
        # )

        # увеличим поверхность
        new_rect = pg.Rect(
            self_offs[0],
            self_offs[1],
            self_rectsize.w,
            self_rectsize.h + len(self.arr_text) * 22 + 2  # размер вспомогательного окна определяется числом слов
        )


        params1 = {
            'tmp_class_name': "GuiSelectList",
            'creator_wnd': self,
        }

        params2 = {
            'rect': child_rect,
            'text': self.arr_text,
            'value': self.value,
        }


        self.parent_wnd.sendMessage("WM_REQUEST_FOCUS", params1, params2)


    #
    # установить новое значение
    #
    def setValue(self,new_value):
        self.value = new_value

    #
    #
    #
    # def setFocus(self,new_focus):
    #     pass





