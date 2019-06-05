import os
import pygame as pg
import random
from jogo_config import *
from c_jogador import *
from fase import *

#TO DO:
# Dar continuidade a logica de troca de fase
# Adicionar inimigos
# Adicionar golpe e colisao com inimigo
# ------- Tres etapas de verificacao: colisao, animacao, direcao que o personagem olha
# Caixa de texto e dialogo
#


#pg.init()
#bg0 = pg.image.load(os.path.join("asset/image/bg/f0_bg.jpg")).convert()

class Jogo:
    def __init__(self):
        # Inicializa a tela
        pg.init()
        pg.mixer.init()
        pg.display.set_caption(TITULO)
        self.janela = pg.display.set_mode((LARGURA, ALTURA))
        self.clock = pg.time.Clock()
        self.rodando = True
        self.todos_sprites = pg.sprite.Group()
        self.jogador = Jogador(self)
        self.chao = pg.sprite.Group()
        self.plataformas = pg.sprite.Group()
        self.iobjeto = pg.sprite.Group()

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
        self.todos_sprites.add(c0)
        self.chao.add(c0)
        # op = Iobjeto(222, -770, 200, 320, "porta-saida-tuto")
        # self.todos_sprites.add(op)
        # self.iobjeto.add(op)

        for plat in fase["shapes"]:
            p = Plataforma(*plat)
            self.todos_sprites.add(p)

            if p.tag != "":
                self.iobjeto.add(p)
            else:
                self.plataformas.add(p)

        self.update()
        self.desenhar()

    # def tfase():
    #     self.fase = Mapa(FASE, FASE_Q)
    #     self.todos_sprites = pg.sprite.Group()
    #     self.plataformas = pg.sprite.Group()
    #     self.chao = pg.sprite.Group()
    #     self.jogador = Jogador(self)
    #     self.iobjeto = pg.sprite.Group()
    #     self.todos_sprites.add(self.jogador)
    #     pos = (-2240, 681)
    #     c0 = Plataforma(-2560, ALTURA - 40, LARGURA*2, 40)
    #     self.todos_sprites.add(c0)
    #     self.chao.add(c0)
    #     op = Iobjeto(-2560, -770, 200, 320, "porta-ent-tuto")
    #     self.todos_sprites.add(op)
    #     self.iobjeto.add(op)
    #     for plat in LISTA_PLATAFORMA_FASE1:
    #         p = Plataforma(*plat)
    #         self.todos_sprites.add(p)
    #         self.plataformas.add(p)
    #     self.camera = Camera(self.fase.MapaLargura, self.fase.MapaAltura)
    #     self.executando()

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

        if colChao:
            self.jogador.pos.y = colChao[0].rect.top + 1
            self.jogador.vel.y = 0
        #Checa se o jogador colidiu com a plataforma(Cima e baixo)
        colPlat = pg.sprite.spritecollide(self.jogador, self.plataformas, False)
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
            #Verifica se alguma tecla foi pressionada
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    self.jogador.pulo()
                    self.jogador.pulando = True
                if event.key == pg.K_SPACE:
                    self.jogador.interagir()

    def desenhar(self):
        # Loop do jogo - desenha a tela
        self.janela.fill(BRANCO)
        self.jogador.draw(self.janela)
        #self.todos_sprites.draw(self.janela)
        for sprite in self.todos_sprites:
            self.janela.blit(sprite.image, self.camera.apply(sprite))
        #pg.display.flip()
        pg.display.update()

    def mostra_tela_inicio(self):
        pass

    def mostra_tela_game_over(self):
        pass

g = Jogo()
g.novo(LISTA_PLATAFORMA_TUTO)

#g.mostra_tela_inicio()
while g.rodando:
    g.executando()
    #g.mostra_tela_game_over
pg.quit()
