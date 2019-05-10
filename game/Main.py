import pygame as pg
import random
#from jogo-config import *
#from sprite import *



#Arrumar Import
#Arrumar Scroll da tela

#3333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
#                                                                                            2
#   Arquivo: jogo-config.py                                                                  2
#                                                                                            2
#222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222

#opções e variáves imutáveis do jogo
TITULO = "Corsários do Mar de Areia"
LARGURA = 1280
ALTURA = 720
FPS = 60

#Propriedades de jogador
JOGADOR_ACEL = 0.5
JOGADOR_FRIC = -0.12
JOGADOR_GRAV = 0.8
JOGADOR_PULO = 20

#Propriedades de plataformas

LISTA_PLATAFORMA = [(0, ALTURA - 40, LARGURA, 40),#chão
                    (300, 600, 100, 100),#caixa esquerda
                    (400, 600, 100, 100), #caixa direita
                    (0, 430, 150, 35), #plataforma canto
                    (240, 250, 180, 35), #degrau
                    (630, 250, 180, 35)] #plataforma porta


#LISTA_PLATAFORMA = [(0, ALTURA - 40, LARGURA, 40),
                    #(LARGURA/2 - 50, ALTURA * 3 / 4, 100, 20),
                    #(125, ALTURA - 350, 100, 20),
                    #(50, 90, 60, 10),
                    #(175, 100, 50, 20),
                    #(175, 100, 50, 20)]
#Paleta de cores (VALORES EM RGB)
BRANCO = (255,255,255)
PRETO = (0,0,0)
VERMELHO = (255,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)
AMARELO = (255,255,0)


#222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222
#                                                                                            2
#   Arquivo: sprite.py                                                                       2
#                                                                                            2
#222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222

vec = pg.math.Vector2 #inicializa um vetor de 2 dimensões

class Jogador(pg.sprite.Sprite):
    def __init__(self, jogo):
        #Classe com os atributos do jogador
        pg.sprite.Sprite.__init__(self)
        #Passando o atributo jogo para o jogador ele toma conhecimento de todos os objetos(self) no código, assim esses podem ser usados como referencia
        self.jogo = jogo
        self.image = pg.Surface((30,40))
        self.image.fill(AMARELO)
        self.rect = self.image.get_rect()
        self.rect.center = (ALTURA/2, LARGURA/2)
        #self.pos = vec(LARGURA/2, ALTURA/2) #utiliza o vetor de 2 posições aqui para armazenar parametros (Posição, velocidade, aceleração)
        self.pos = vec(1000, 700) #utiliza o vetor de 2 posições aqui para armazenar parametros (Posição, velocidade, aceleração)
        self.vel = vec(0,0)
        self.acel = vec(0,0)

    def pulo(self):
        #verifica se existe plataforma abaixo antes de pular
        self.rect.x += 1
        colPlat = pg.sprite.spritecollide(self, self.jogo.plataformas, False)#exemplo de uso do parametro jogo para usar as plataformas para comparação na colisão
        self.rect.x -= 1
        if colPlat:
            self.vel.y = -JOGADOR_PULO

    def update(self):
        #Método que verifica a tecla pressionada e movimenta o jogador
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
        if self.pos.x > LARGURA:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = LARGURA

        self.rect.midbottom = self.pos

class Plataforma(pg.sprite.Sprite):
    def __init__(self, x, y, l, a):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((l, a))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#3333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333

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
        self.todos_sprites = pg.sprite.Group()
        self.plataformas = pg.sprite.Group()
        self.jogador = Jogador(self)
        self.todos_sprites.add(self.jogador)
        for plat in LISTA_PLATAFORMA:
            p = Plataforma(*plat)
            self.todos_sprites.add(p)
            self.plataformas.add(p)
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
        #Checa se o jogador colidiu com a plataforma(apenas se estiver caindo)
        if self.jogador.vel.y > 0:
            colPlat = pg.sprite.spritecollide(self.jogador, self.plataformas, False)
            if colPlat:
                self.jogador.pos.y = colPlat[0].rect.top +1
                self.jogador.vel.y = 0
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

    def desenhar(self):
        # Loop´do jogo - desenha a tela
        self.janela.fill(PRETO)
        self.todos_sprites.draw(self.janela)
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