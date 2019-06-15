import os
import pygame as pg
import random
from jogo_config import *
from c_jogador import *

#(554.167, 681)
FASE = 0
FASE_Q = 0

LISTA_FASES = [
    {
        "player": (554.167, 681),
        "shapes": [
            (-234, 350, 330, 330, "caixa"),#caixa esquerda
            (-566, 350, 330, 330, "caixa"), #caixa direita
            (-1280, 0, 445, 35, "platf1"), #plataforma canto
            (-505, -315, 300, 35, "platf2"), #degrau
            (0, -450, 445, 35, "platf1"), #plataforma porta
            (1279, -500, 400, 1200, "par1"), #Parede direita down
            (450, -959, 1200, 950, "par2"), #Parede direita up
            (-1680, -1000, 400, 1690, "par3"), #Parede esquerda
            (-1280, -1000, LARGURA*2, 40) #teto
        ],
        "portas": [
            (222, -770, "porta-saida")
        ]
    },
    {
        "player": (-1100, 675),
        "enemy": (900, 681),
        "shapes": [
            # (-1280, 359, 200, 320, "porta-entrada"),
            (-234, 20, 330, 330, "caixa"),
            (-234, 350, 330, 330, "caixa"),
            (-566, 350, 330, 330, "caixa"),
            (-1680, -1000, 400, 1690, "par3"),
            (1279, -500, 400, 1200, "par1")
        ],
        "portas": [
            (-1280, 359, "porta-entrada")
        ]
    }
]

dirname = os.path.dirname(__file__)

#bg = pg.image.load(os.path.join(dirname, 'asset/image/bg/f0_bg.jpg'))

class Plataforma(pg.sprite.Sprite):
    def __init__(self, x, y, l, a, tag=""):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((l, a))

        if tag == "":
            self.image.fill(MARROM)
        elif tag == "porta-saida" or tag == "porta-entrada":
            self.image = scn_porta
        elif tag == "caixa":
            self.image = scn_caixa
        elif tag == "platf1":
            self.image = scn_plat1
        elif tag == "platf2":
            self.image = scn_plat2
        elif tag == "par1":
            self.image = scn_parede1
        elif tag == "par2":
            self.image = scn_parede2
        elif tag == "par3":
            self.image = scn_parede3

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

class Porta(pg.sprite.Sprite):
    def __init__(self, x, y, tag):
        pg.sprite.Sprite.__init__(self)
        self.image = scn_porta
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tag = tag

        self.rendered_at = pg.time.get_ticks() / 1000
        self.delay = 3
        self.enabled = False

    def update(self):
        now = pg.time.get_ticks() / 1000

        if now - self.rendered_at >= self.delay and not self.enabled:
            self.enabled = True

class Mapa:
    #def __init__(self, nFase, nQuadrante, filename):
    def __init__(self, nFase, nQuadrante):
        self.nQuadrante = nQuadrante
        #self.filename = filename
        self.qAltura = ALTURA
        self.qLargura = LARGURA
        self.MapaAltura = nQuadrante * self.qAltura / 2
        self.MapaLargura = nQuadrante * self.qLargura / 2


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
