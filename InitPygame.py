import pygame as pg
from config import *

pg.init()
pg.font.init()

pg.display.set_caption(MAIN_WND_TITLE)
if MAIN_WND_FULLSCREEN:
    # вариант для FULLSCREEN
    g_main_srf = pg.display.set_mode(
        # (1600, 900),
        (MAIN_WND_WIDTH, MAIN_WND_HEIGHT),
        pg.FULLSCREEN
    )

else:
    # вариант для запуска в окне
    g_main_srf = pg.display.set_mode(
        (MAIN_WND_WIDTH, MAIN_WND_HEIGHT)
    )