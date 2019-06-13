import os
import pygame as pg
import random
from jogo_config import *
from c_jogador import *
from c_inimigo import *

class Jogo:
    def __init__(self, janela):
        # Inicializa a tela
        self.janela = janela
        self.clock = pg.time.Clock()
        self.rodando = True
        self.todos_sprites = pg.sprite.Group()
        self.jogador = Jogador(self)
        self.inimigo = Inimigo(self)
        self.chao = pg.sprite.Group()
        self.plataformas = pg.sprite.Group()
        self.iobjeto = pg.sprite.Group()
        self.tiros = pg.sprite.Group()
        self.tiros_jogador = pg.sprite.Group()

    def novo(self, fase):
        self.todos_sprites.empty()
        self.chao.empty()
        self.plataformas.empty()

        # Comeca um jogo novo
        self.fase = Mapa(FASE, FASE_Q)
        self.camera = Camera(self.fase.MapaLargura, self.fase.MapaAltura)

        self.jogador.set_position(*fase["player"])
        self.todos_sprites.add(self.jogador)
        c0 = Plataforma(-1280, ALTURA - 40, LARGURA*2, 40)

        enemyPos = fase.get("enemy", -1)

        if enemyPos != -1:
            self.inimigo.set_position(*enemyPos)
            self.todos_sprites.add(self.inimigo)

        self.todos_sprites.add(c0)
        self.chao.add(c0)

        for plat in fase["shapes"]:
            p = Plataforma(*plat)
            self.todos_sprites.add(p)

            if p.tag == "porta-entrada" or p.tag == "porta-saida":
                self.iobjeto.add(p)
            else:
                self.plataformas.add(p)

        self.desenhar()

    def executando(self):
        # Loop do jogo
        self.jogando = True
        pg.mixer.music.load(os.path.join(os.path.dirname(__file__), "asset/sound/music/music.mp3"))

        while self.jogando:
            self.clock.tick(FPS)
            self.eventos()
            self.update()
            self.desenhar()

    def update(self):
        # Loop do jogo - atualiza a interface
        self.todos_sprites.update()

        colChao = pg.sprite.spritecollide(self.jogador, self.chao, False)
        colPlat = pg.sprite.spritecollide(self.jogador, self.plataformas, False)
        colPlatInimigo = pg.sprite.spritecollide(self.inimigo, self.plataformas, False)

        if colChao:
            self.jogador.pos.y = colChao[0].rect.top + 1
            self.jogador.vel.y = 0
        #Checa se o jogador colidiu com a plataforma(Cima e baixo)
        if colPlat:
            if self.jogador.vel.y > 0:
                #checa se colidiu com o topo
                self.jogador.pos.y = colPlat[0].rect.top + 1
                self.jogador.vel.y = 0
                seguranca = False
            else:
                #caso nao, checa se colidiu com o fundo e regride o pulo
                self.jogador.vel.y *= -1
                seguranca = True
        #Colisao com os lados
            if seguranca:
                #verifica a variavel de seguranca para saber se esta colidindo com y, caso nao, ocorre a colisao com x
                #resetando a posicao do jogador antes de colidir com a caixa
                if self.jogador.vel.x != 0 or self.jogador.pos.y > 0:
                    self.jogador.pos.x = self.jogador.xAntes
                self.jogador.vel.x = 0

        if colPlatInimigo:
            if self.inimigo.vel.y > 0:
                self.inimigo.pos.y = colPlatInimigo[0].rect.top + 1
                self.inimigo.vel.y = 0
            else:
                self.inimigo.vel.y *= -1


        self.camera.update(self.jogador)
        #se jogador chegar em certo ponto da tela
        '''if self.jogador.rect.left <= ALTURA - 200:
            self.jogador.pos.x -= abs(self.jogador.vel.x)
            for plat in self.plataformas:
                plat.rect.x -= abs(self.jogador. vel.x)
        if self.jogador.rect.right <= ALTURA/4:
            self.jogador.pos.x += abs(self.jogador.vel.x)
            for plat in self.plataformas:
                plat.rect.x += abs(self.jogador.vel.x)'''

    def eventos(self):
        # Loop do jogo - captura de eventos
        for event in pg.event.get():
            #Verifica se a janela foi fechada
            if event.type == pg.QUIT:
                if self.jogando:
                    self.jogando = False
                self.executando = False

    def desenhar(self):
        # Loop do jogo - desenha a tela
        #self.janela.blit(bg, (-1280,-720))
        self.janela.fill(BRANCO)
        # self.jogador.draw()
        self.inimigo.draw()
        #self.todos_sprites.draw(self.janela)
        for sprite in self.todos_sprites:
            self.janela.blit(sprite.image, self.camera.apply(sprite))
        #pg.display.flip()
        pg.display.update()
