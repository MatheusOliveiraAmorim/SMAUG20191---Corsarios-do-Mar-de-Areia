import pygame as pg
import random
from jogo_config import *
from fase import *

vec = pg.math.Vector2 #inicializa um vetor de 2 dimensões

class Jogador(pg.sprite.Sprite):
    def __init__(self, jogo):
        #Classe com os atributos do jogador
        pg.sprite.Sprite.__init__(self)
        #Passando o atributo jogo para o jogador ele toma conhecimento de todos os objetos(self) no codigo, assim esses podem ser usados como referencia
        self.jogo = jogo
        self.image = pg.Surface((200, 320))
        self.image.fill(AMARELO)
        self.rect = self.image.get_rect()
        self.rect.center = (ALTURA/2, LARGURA/2)
        #self.pos = vec(LARGURA/2, ALTURA/2) #utiliza o vetor de 2 posições aqui para armazenar parametros (Posicao, velocidade, aceleracao)
        self.pos = vec(0, 0) #utiliza o vetor de 2 posicoes aqui para armazenar parametros (Posicao, velocidade, aceleracao)
        self.vel = vec(0,0)
        self.acel = vec(0,0)
        #self.pulando = False
        self.xAntes = 0
    
    def set_position(self, x, y):
        self.pos = vec(x, y)

    def pulo(self):
        #verifica se existe plataforma abaixo antes de pular
        self.rect.x += 1
        colPlat = pg.sprite.spritecollide(self, self.jogo.plataformas, False)#exemplo de uso do parametro jogo para usar as plataformas para comparacao na colisão
        colChao = pg.sprite.spritecollide(self, self.jogo.chao, False)#exemplo de uso do parametro jogo para usar as plataformas para comparacao na colisão
        self.rect.x -= 1
        if colPlat or colChao:
            self.vel.y = -JOGADOR_PULO
            #self.pulando = False

    def interagir(self):
        colIobj = pg.sprite.spritecollide(self, self.jogo.iobjeto, False)
        if colIobj:
            for tobj in colIobj:
                if tobj.tag and tobj.tag == "porta-saida":
                    self.jogo.fase.nFase = int(1)
                    self.jogo.novo(LISTA_PLATAFORMA_FASE1)
                    print(self.jogo.fase.nFase)
                    print(self.jogo.fase.nQuadrante)

    def update(self):
        #Método que verifica a tecla pressionada e movimenta o jogador
        #print(self.pos)
        self.xAntes = self.pos.x
        self.acel = vec(0, JOGADOR_GRAV)
        tecla = pg.key.get_pressed()
        if tecla[pg.K_LEFT]:
            self.acel.x = -JOGADOR_ACEL
        if tecla[pg.K_RIGHT]:
            self.acel.x = JOGADOR_ACEL

        #Adiciona coeficiente de fricção a equação de movimento para estabilizar o movimento do jogador
        self.acel.x += self.vel.x * JOGADOR_FRIC
        #Equações de movimento
        self.vel += self.acel
        self.pos += self.vel + 0.5 * self.acel
        #Para na borda da tela
        '''if self.pos.x > LARGURA:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = LARGURA'''

        self.rect.midbottom = self.pos