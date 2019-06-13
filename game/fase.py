import os
import pygame as pg
import random
from jogo_config import *
from c_jogador import *

#(554.167, 681)
FASE = 0
FASE_Q = 0

dirname = os.path.dirname(__file__)

bg = pg.image.load(os.path.join(dirname, 'asset/image/bg/f0_bg.jpg'))


LISTA_PLATAFORMA_TUTO = {
    "player": (554.167, 681),
    "shapes": [
        (-234, 349, 330, 330, "caixa"),#caixa esquerda
        (-566, 349, 330, 330, "caixa"), #caixa direita
        (-1280, 0, 445, 35), #plataforma canto
        (-505, -315, 300, 35), #degrau
        (0, -450, 445, 35), #plataforma porta
        (1280, -500, 400, 1200), #Parede direita down
        (450, -959, 1200, 950), #Parede direita up
        (-1685, -1000, 400, 1690), #Parede esquerda
        (-1280, -1000, LARGURA*2, 40), #teto
        (222, -770, 200, 320, "porta-saida")
    ]
}

LISTA_PLATAFORMA_TUTO_2 = {
    "player": (222, -450),
    "shapes": [
        (-234, 349, 330, 330, "caixa"),#caixa esquerda
        (-566, 349, 330, 330, "caixa"), #caixa direita
        (-1280, 0, 445, 35, "plataforma"), #plataforma canto
        (-505, -315, 300, 35, "plataforma"), #degrau
        (0, -450, 445, 35, "plataforma"), #plataforma porta
        (1280, -500, 400, 1200), #Parede direita down
        (450, -959, 1200, 950), #Parede direita up
        (-1685, -1000, 400, 1690), #Parede esquerda
        (-1280, -1000, LARGURA*2, 40), #teto
        (222, -770, 200, 320, "porta-saida")
    ]
}

LISTA_PLATAFORMA_FASE1 = {
    "player": (-1100, 675),
    "enemy": (900, 681),
    "shapes": [(-1280, 359, 200, 320, "porta-entrada"),
    (-234, 18, 330, 330, "caixa"),
    (-234, 349, 330, 330, "caixa"),
    (-566, 349, 330, 330, "caixa"),
    (-1685, -1000, 400, 1690)
    ]
}


class Plataforma(pg.sprite.Sprite):
    def __init__(self, x, y, l, a, tag=""):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((l, a))

        if tag == "":
            self.image.fill(VERDE)
        elif tag == "porta-saida" or tag == "porta-entrada":
            self.image = scn_porta
        elif tag == "caixa":
            self.image = scn_caixa

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tag = tag

class Chao(pg.sprite.DirtySprite):
    def __init__(self, x, y, l, a):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((l, a))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.layer = 1

class Mapa:
    #def __init__(self, nFase, nQuadrante, filename):
    def __init__(self, nFase, nQuadrante):
        self.nFase = nFase
        self.nQuadrante = nQuadrante
        #self.filename = filename
        self.qAltura = ALTURA
        self.qLargura = LARGURA
        self.MapaAltura = nQuadrante * self.qAltura / 2
        self.MapaLargura = nQuadrante * self.qLargura / 2
        #print(self.MapaAltura, self.MapaLargura)

    def update(self, nFase):
        if self.nFase == 0:
            pg.image.load(self.filename)
            self.nQuadrante = 4
        if self.nFase == 1:
            self.nQuadrante = 6


class Camera:
    def __init__(self, cLargura, cAltura):
        self.camera = pg.Rect(0, 0, cLargura, cAltura)
        self.cAltura = cAltura
        self.cLargura = cLargura
        self.camLimAlt = Mapa(FASE, FASE_Q).MapaAltura
        self.camLimLarg = Mapa(FASE, FASE_Q).MapaLargura

    def apply(self, entidade):
        return entidade.rect.move(self.camera.topleft)

    def update(self, alvo):
        x = -alvo.rect.x + int(LARGURA/2)
        y = -alvo.rect.y + int(ALTURA/2)

        '''#limitar câmera
        x = min(0, x)
        x = max(-(self.camLimLarg - LARGURA), x)
        y = min(0, y)
        y = max(-(self.camLimAlt - ALTURA), y)
        #print(x, y)
        if alvo.vel.x > 0:
            x += 400'''
        self.camera = pg.Rect(x, y, self.cLargura, self.cAltura)
