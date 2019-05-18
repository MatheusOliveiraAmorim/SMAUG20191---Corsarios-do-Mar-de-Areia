import pygame as pg
import random
from jogo_config import *
from c_jogador import *
from fase import *



#Arrumar Import
#Arrumar Scroll da tela

class Jogo:
    def __init__(self):
        # Inicializa a tela
        pg.init()
        pg.mixer.init()
        pg.display.set_caption(TITULO)
        self.janela = pg.display.set_mode((LARGURA, ALTURA))
        self.clock = pg.time.Clock()
        self.rodando = True

    def novo(self):
        # Começa um jogo novo
        self.mapa = Mapa(4)
        self.todos_sprites = pg.sprite.Group()
        self.plataformas = pg.sprite.Group()
        self.chao = pg.sprite.Group()
        self.jogador = Jogador(self)
        self.iobjeto = pg.sprite.Group()
        self.todos_sprites.add(self.jogador)
        c0 = Plataforma(-1280, ALTURA - 40, LARGURA*2, 40)
        self.todos_sprites.add(c0)
        self.chao.add(c0)
        op = Iobjeto(222, -770, 200, 320)
        self.todos_sprites.add(op)
        self.iobjeto.add(op)
        for plat in LISTA_PLATAFORMA_TUTO:
            p = Plataforma(*plat)
            self.todos_sprites.add(p)
            self.plataformas.add(p)
        self.camera = Camera(self.mapa.MapaLargura, self.mapa.MapaAltura)
        self.executando()

    def executando(self):
        # Loop´do jogo
        self.jogando = True

        while self.jogando:
            self.clock.tick(FPS)
            self.eventos()
            self.update()
            self.desenhar()


    def update(self):
        # Loop´do jogo - atualiza a interface
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
            else:
                #caso não, checa se colidiu com o fundo e regride o pulo
                self.jogador.vel.y *= -1
        #Colisão com os lados
            '''if self.jogador.vel.x > 0:
                self.jogador.pos.x = colPlat[0].rect.left - self.jogador.rect.width
            if self.jogador.vel.x < 0:
                self.jogador.pos.x = colPlat[0].rect.right - self.jogador.rect.width
            self.jogador.vel.x = 0
            self.jogador.rect.x = self.jogador.pos.x'''



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
        # Loop´do jogo - captura de eventos
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
                if event.key == pg.K_SPACE:
                    self.jogador.interagir()

    def desenhar(self):
        # Loop´do jogo - desenha a tela
        self.janela.fill(PRETO)
        #self.todos_sprites.draw(self.janela)
        for sprite in self.todos_sprites:
            self.janela.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def mostra_tela_inicio(self):
        pass

    def mostra_tela_game_over(self):
        pass

g = Jogo()
g.mostra_tela_inicio()
while g.rodando:
    g.novo()
    g.mostra_tela_game_over

pg.quit()