import pygame as pg
import random
from jogo_config import *
from fase import *
from c_tiro import *
import copy
from random import randint

vec = pg.math.Vector2 #inicializa um vetor de 2 dimensões

class Inimigo(pg.sprite.Sprite):
    def __init__(self, jogo):
        #Classe com os atributos do jogador
        pg.sprite.Sprite.__init__(self)
        #Passando o atributo jogo para o jogador ele toma conhecimento de todos os objetos(self) no codigo, assim esses podem ser usados como referencia
        self.image = enemy_l
        self.jogo = jogo
        #self.image.fill(AMARELO)
        self.pos = vec(0, 0)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.vel = vec(0,0)
        self.acel = vec(0, 0)
        self.xAntes = 0
        self.facingRight = False
        self.facingLeft = True
        self.shot_at = 0
        self.jumped_at = 0
        self.vida = 30
        self.pulando = False

    def set_position(self, x, y):
        self.pos = vec(x, y)

    def draw(self):
        pass

    def colisao(self):
        tiroColidido = pg.sprite.spritecollideany(self, self.jogo.tiros_jogador, False)

        if tiroColidido:
            self.vida -= 10
            tiroColidido.kill()

        if self.vida <= 0:
            self.kill()

    def pulo(self):
        self.rect.x += 1
        colPlat = pg.sprite.spritecollide(self, self.jogo.plataformas, False)
        colChao = pg.sprite.spritecollide(self, self.jogo.chao, False)
        self.rect.x -= 1

        if not colPlat or not colChao:
            now = pg.time.get_ticks() / 1000
            delay = 3

            prob_pulo = randint(0, 5)

            if prob_pulo % 2 != 0 and now - self.jumped_at > delay:
                print("pulo")
                self.pulando = True
                self.jumped_at = now
                self.vel.y = -10

    def update(self):
        self.colisao()

        self.rect.midbottom = self.pos
        now = pg.time.get_ticks() / 1000
        delay = 1

        if now - self.shot_at > delay:
            self.shot_at = now

            direcao = "left" if self.facingLeft == True else "right"
            tiro = Tiro(vec(self.pos.x, self.pos.y - 150), direcao)

            self.jogo.todos_sprites.add(tiro)
            self.jogo.tiros.add(tiro)

        self.vel += self.acel
        self.pos += self.vel + 0.5 * self.acel
