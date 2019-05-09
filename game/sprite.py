import pygame as pg
import random
#from jogo-config import *

class Jogador(pg.sprite.Sprite):
    def __init__(self):
        #Classe com os atributos do jogador
        pg.sprite.Sprite.__init__(self)
        self.imagem = pg.Surface((30,40))
        self.imagem.fill(AMARELO)
        self.rect = self.imagem.get_rect()
        self.vx = 0
        self.vx = 0

    def update(self):
        #Método que verifica a tecla pressionada e movimenta o jogador
        self.vx = 0
        tecla = pg.keys.get_pressed()
        if tecla[pg.K_LEFT]:
            self.vx = -5
        if tecla[pg.K_RIGHT]:
            self.vx = 5

        self.rect.x += self.vx
        self.rect.y += self.vy