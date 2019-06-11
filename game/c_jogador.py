import pygame as pg
import random
from jogo_config import *
from fase import *
from c_tiro import *

vec = pg.math.Vector2 #inicializa um vetor de 2 dimensões

class Jogador(pg.sprite.Sprite):
    def __init__(self, jogo):
        #Classe com os atributos do jogador
        pg.sprite.Sprite.__init__(self)
        #Passando o atributo jogo para o jogador ele toma conhecimento de todos os objetos(self) no codigo, assim esses podem ser usados como referencia
        self.jogo = jogo
        self.image = char_r
        #self.image.fill(AMARELO)
        self.rect = self.image.get_rect()
        self.rect.center = (ALTURA/2, LARGURA/2)
        #self.pos = vec(LARGURA/2, ALTURA/2) #utiliza o vetor de 2 posições aqui para armazenar parametros (Posicao, velocidade, aceleracao)
        self.pos = vec(0, 0) #utiliza o vetor de 2 posicoes aqui para armazenar parametros (Posicao, velocidade, aceleracao)
        self.vel = vec(0,0)
        self.acel = vec(0,0)
        #self.pulando = False
        self.xAntes = 0
        self.Aleft = False
        self.Aright = False
        self.Pleft = False
        self.Pright = False
        self.facingRight = False
        self.facingLeft = False
        self.walkCount = 0
        self.updated_at = 0
        self.is_song_paused = True
        self.vida = 30

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
                if tobj.tag and tobj.tag == "porta-entrada":
                    self.jogo.fase.nFase = int(1)
                    self.jogo.novo(LISTA_PLATAFORMA_TUTO_2)
                    print(self.jogo.fase.nFase)
                    print(self.jogo.fase.nQuadrante)

    def draw (self):
        now = pg.time.get_ticks() / 1000
        delay = .1

        if self.walkCount + 1 >= 4:
            self.walkCount = 0
        if self.Aleft:
            if (now - self.updated_at > delay):
                self.image = walkLeft[self.walkCount]
                self.updated_at = now
                self.walkCount += 1
        elif self.Aright:
            if (now - self.updated_at > delay):
                self.image = walkRight[self.walkCount]
                self.updated_at = now
                self.walkCount += 1
        else:
            if self.Pleft:
                self.image = char_l
            if self.Pright:
                self.image = char_r

    def play_music(self):
        # if self.is_song_paused:
        #     if pg.mixer.music.get_pos() == -1:
        #         pg.mixer.music.play()
        #     else:
        #         pg.mixer.music.unpause()

            self.is_song_paused = False

    def stop_music(self):
        if not self.is_song_paused:
            pg.mixer.music.pause()
            self.is_song_paused = True

    def colisao(self):
        tiroColidido = pg.sprite.spritecollideany(self, self.jogo.tiros, False)

        if tiroColidido:
            self.vida -= 10
            tiroColidido.kill()

        if self.vida <= 0:
            self.kill()

    def atirar(self):
        direcao = "left" if self.facingLeft == True else "right"
        tiro = Tiro(vec(self.pos.x, self.pos.y - 150), direcao)

        self.jogo.todos_sprites.add(tiro)
        self.jogo.tiros_jogador.add(tiro)

    def update(self):
        #Método que verifica a tecla pressionada e movimenta o jogador
        #print(self.pos)
        self.xAntes = self.pos.x
        self.acel = vec(0, JOGADOR_GRAV)
        tecla = pg.key.get_pressed()

        self.colisao()

        if tecla[pg.K_LEFT]:
            self.play_music()

            self.acel.x = -JOGADOR_ACEL

            self.Aleft = True
            self.Aright = False

            self.Pleft = False
            self.Pright = False

            self.facingRight = False
            self.facingLeft = True

        if tecla[pg.K_RIGHT]:
            self.play_music()

            self.acel.x = JOGADOR_ACEL

            self.Aleft = False
            self.Aright = True

            self.Pleft = False
            self.Pright = False

            self.facingRight = True
            self.facingLeft = False

        if not tecla[pg.K_RIGHT] and not tecla[pg.K_LEFT]:
            self.stop_music()

        if not tecla[pg.K_RIGHT] and self.facingRight:
            self.Pleft = False
            self.Pright = True

            self.Aleft = False
            self.Aright = False

            self.walkCount = 0

        if not tecla[pg.K_LEFT] and self.facingLeft:
            self.Pleft = True
            self.Pright = False

            self.Aleft = False
            self.Aright = False

            self.walkCount = 0

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
