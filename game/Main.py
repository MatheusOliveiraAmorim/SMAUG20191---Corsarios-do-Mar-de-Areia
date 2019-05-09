import pygame as pg
import random
#import jogo-config
#from jogo-config import *



#opções e variáves imutáveis do jogo
TITULO = "Corsários do Mar de Areia"
LARGURA = 360
ALTURA = 480
FPS = 30

#Paleta de cores (VALORES EM RGB)
BRANCO = (255,255,255)
PRETO = (0,0,0)
VERMELHO = (255,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)

class jogo:
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
        self.todos_sprites = pg.sprite.Group()
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

    def eventos(self):
        # Loop´do jogo - captura de eventos
        for event in pg.event.get():
            #Verifica se a janela foi fechada
            if event.type == pg.QUIT:
                if self.jogando:
                    self.jogando = False
                self.executando = False

    def desenhar(self):
        # Loop´do jogo - desenha a tela
        self.janela.fill(PRETO)
        self.todos_sprites.draw(self.janela)
        pg.display.flip()

    def mostra_tela_inicio(self):
        pass

    def mostra_tela_game_over(self):
        pass

g = jogo()
g.mostra_tela_inicio()
while g.rodando:
    g.novo()
    g.mostra_tela_game_over

pg.quit()