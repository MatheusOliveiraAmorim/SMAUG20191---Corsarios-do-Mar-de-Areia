import pygame as pg
import random
from jogo_config import *
from fase import *

vec = pg.math.Vector2

class Tiro(pg.sprite.Sprite):
    def __init__(self, position, direcao):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 10))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.rect.center = position
        self.pos = position
        self.direcao = direcao
        self.disparado = False
        self.updated_at = 0
        self.vel = 8
        self.acel = vec(0, 0)

    def update(self):
        velocidade = 10
        if self.direcao == "left":
            velocidade = -10

        self.rect.x += velocidade
