import pygame as pg
import random
from jogo_config import *
from c_jogador import *


FASE = 0
FASE_Q = 0
    

LISTA_PLATAFORMA_TUTO = [
                        (-234, 349, 330, 330),#caixa esquerda
                        (-566, 349, 330, 330), #caixa direita
                        (-1280, 0, 445, 35), #plataforma canto
                        (-505, -315, 300, 35), #degrau
                        (0, -450, 445, 35), #plataforma porta
                        (1280, -500, 400, 1200)] 

LISTA_PLATAFORMA_FASE1 = [
                        (-234, 349, 330, 330)] #plataforma port


#LISTA_PLATAFORMA = [(0, ALTURA - 40, LARGURA, 40),
                    #(LARGURA/2 - 50, ALTURA * 3 / 4, 100, 20),
                    #(125, ALTURA - 350, 100, 20),
                    #(50, 90, 60, 10),
                    #(175, 100, 50, 20),
                    #(175, 100, 50, 20)]

class Plataforma(pg.sprite.Sprite):
    def __init__(self, x, y, l, a):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((l, a))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Chao(pg.sprite.Sprite):
    def __init__(self, x, y, l, a):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((l, a))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Iobjeto(pg.sprite.Sprite):
    def __init__(self, x, y, l, a, tag):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((l, a))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tag = tag

class Mapa:
    #def __init__(self, nFase, nQuadrante, filename):
    def __init__(self, nFase, nQuadrante):
        self.nFase = nFase
        self.nQuadrante = nQuadrante
        self.filename = filename
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
        self.camLimAlt = Mapa(self.nFase, self.nQuadrante).MapaAltura
        self.camLimLarg = Mapa(self.nFase, self.nQuadrante).MapaLargura

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