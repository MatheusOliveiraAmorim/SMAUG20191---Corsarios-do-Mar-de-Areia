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
JOGADOR_ACEL = 0.8
JOGADOR_FRIC = -0.12
JOGADOR_GRAV = 0.85
JOGADOR_PULO = 25


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
ipos = (554.167, 681) #posição inicial do jogador

class Jogador(pg.sprite.Sprite):
    def __init__(self, jogo):
        #Classe com os atributos do jogador
        pg.sprite.Sprite.__init__(self)
        #Passando o atributo jogo para o jogador ele toma conhecimento de todos os objetos(self) no código, assim esses podem ser usados como referencia
        self.jogo = jogo
        self.image = pg.Surface((200, 320))
        self.image.fill(AMARELO)
        self.rect = self.image.get_rect()
        self.rect.center = (ALTURA/2, LARGURA/2)
        #self.pos = vec(LARGURA/2, ALTURA/2) #utiliza o vetor de 2 posições aqui para armazenar parametros (Posição, velocidade, aceleração)
        self.pos = vec(ipos) #utiliza o vetor de 2 posições aqui para armazenar parametros (Posição, velocidade, aceleração)
        self.vel = vec(0,0)
        self.acel = vec(0,0)

    def pulo(self):
        #verifica se existe plataforma abaixo antes de pular
        self.rect.x += 1
        colPlat = pg.sprite.spritecollide(self, self.jogo.plataformas, False)#exemplo de uso do parametro jogo para usar as plataformas para comparação na colisão
        colChao = pg.sprite.spritecollide(self, self.jogo.chao, False)#exemplo de uso do parametro jogo para usar as plataformas para comparação na colisão
        self.rect.x -= 1
        if colPlat or colChao:
            self.vel.y = -JOGADOR_PULO

    def update(self):
        #Método que verifica a tecla pressionada e movimenta o jogador
        #print(self.pos)
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


#222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222
#                                                                                            2
#   Arquivo: fase.py                                                                         2
#                                                                                            2
#222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222



LISTA_PLATAFORMA_TUTO = [#chao
                        (-165, 349, 330, 330),#caixa esquerda
                        (-496, 349, 330, 330), #caixa direita
                        (-1280, 200, 360, 35), #plataforma canto
                        (-1280, 250, 180, 35), #degrau
                        (-1280, -1, 180, 35)] #plataforma porta


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

class Mapa:
    #def __init__(self, nFase, nQuadrante, filename):
    def __init__(self, nQuadrante):
        #self.nFase = nFase
        self.nQuadrante = nQuadrante
        self.qAltura = ALTURA
        self.qLargura = LARGURA
        self.MapaAltura = nQuadrante * self.qAltura / 2
        self.MapaLargura = nQuadrante * self.qLargura / 2
        #print(self.MapaAltura, self.MapaLargura)

class Camera:
    def __init__(self, cLargura, cAltura):
        self.camera = pg.Rect(0, 0, cLargura, cAltura)
        self.cAltura = cAltura
        self.cLargura = cLargura
        self.camLimAlt = Mapa(4).MapaAltura
        self.camLimLarg = Mapa(4).MapaLargura

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
        self.mapa = Mapa(4)
        self.todos_sprites = pg.sprite.Group()
        self.plataformas = pg.sprite.Group()
        self.chao = pg.sprite.Group()
        self.jogador = Jogador(self)
        self.todos_sprites.add(self.jogador)
        c0 = Plataforma(-1280, ALTURA - 40, LARGURA*2, 40)
        self.todos_sprites.add(c0)
        self.chao.add(c0)
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
        colTopoPlat = pg.sprite.spritecollide(self.jogador, self.plataformas, False)
        if colTopoPlat:
            if self.jogador.vel.y > 0:
                #checa se colidiu com o topo
                self.jogador.pos.y = colTopoPlat[0].rect.top + 1
                self.jogador.vel.y = 0
            else:
                #caso não, checa se colidiu com o fundo e regride o pulo
                self.jogador.vel.y *= -1
            #Colisão com os lados
            if self.jogador.vel.x > 0:
                self.jogador.pos.x = colTopoPlat[0].rect.left - self.jogador.rect.width
            if self.jogador.vel.x < 0:
                self.jogador.pos.x = colTopoPlat[0].rect.right - self.jogador.rect.width
            self.jogador.vel.x = 0
            self.jogador.rect.x = self.jogador.pos.x


        '''if self.jogador.vel.y > 0:
            colTopoPlat = pg.sprite.spritecollide(self.jogador, self.plataformas, False)
            if colTopoPlat:
                self.jogador.pos.y = colTopoPlat[0].rect.top +1
                self.jogador.vel.y = 0

        if self.jogador.vel.y < 0:
            colTopoPlat = pg.sprite.spritecollide(self.jogador, self.plataformas, False)
            if colTopoPlat:
                self.jogador.pos.y = colTopoPlat[0].rect.bottom +1
                self.jogador.vel.y = 0'''



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