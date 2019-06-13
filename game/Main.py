import pygame as pg
from jogo_config import *

pg.init()
pg.mixer.init()
pg.display.set_caption(TITULO)
janela = pg.display.set_mode((LARGURA, ALTURA))

from c_menu import *
from c_jogo import *

menu = Menu(janela)
jogo = Jogo(janela)

while menu.is_rodando:
    janela.fill((255, 255, 255))
    pg.event.pump()
    menu.executando()

    if menu.is_jogando:
        jogo.novo(LISTA_PLATAFORMA_TUTO)
        jogo.executando()
        jogo.update()

    pg.event.clear()
    pg.display.flip()

pg.quit()
