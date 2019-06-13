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
        self.rect.w = 160
        #self.pos = vec(LARGURA/2, ALTURA/2) #utiliza o vetor de 2 posições aqui para armazenar parametros (Posicao, velocidade, aceleracao)
        self.pos = vec(0, 0) #utiliza o vetor de 2 posicoes aqui para armazenar parametros (Posicao, velocidade, aceleracao)
        self.vel = vec(0,0)
        self.acel = vec(0,0)
        #self.pulando = False
        self.xAntes = 0
        self.running = False
        self.facing = False
        self.walkCount = 0
        self.updated_at = 0
        self.shot_at = 0
        self.shot_delay = .2
        self.is_song_paused = True
        self.atirando = False
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
                if tobj.tag and tobj.tag == "porta-entrada":
                    self.jogo.fase.nFase = int(1)
                    self.jogo.novo(LISTA_PLATAFORMA_TUTO_2)

    def set_sprite(self, image):
        self.image = image

    def draw (self):
        now = pg.time.get_ticks() / 1000
        delay = .1

        if self.atirando:
            return

        if self.walkCount + 1 > 3:
            self.walkCount = 0

        if self.running:
            if now - self.updated_at > delay:
                if self.facing == "left":
                    self.set_sprite(walkLeft[self.walkCount])
                    self.updated_at = now
                    self.walkCount += 1
                elif self.facing == "right":
                    self.set_sprite(walkRight[self.walkCount])
                    self.updated_at = now
                    self.walkCount += 1
        else:
            if self.facing == "left":
                self.set_sprite(char_l)
            elif self.facing == "right":
                self.set_sprite(char_r)

    def play_music(self):
        if self.is_song_paused:
            if pg.mixer.music.get_pos() == -1:
                pg.mixer.music.play()
            else:
                pg.mixer.music.unpause()

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
            self.stop_music()
            self.kill()

    def atirar(self):
        agora = pg.time.get_ticks() / 1000

        if agora - self.shot_at >= self.shot_delay:
            self.atirando = True

            posicao_tiro = vec(0, 0)
            if self.facing == "left":
                self.set_sprite(char_sl)
                posicao_tiro = vec(self.pos.x - 120, self.pos.y - 160)
            elif self.facing == "right":
                self.set_sprite(char_sr)
                posicao_tiro = vec(self.pos.x + 150, self.pos.y - 160)

            tiro = Tiro(posicao_tiro, self.facing)

            self.jogo.todos_sprites.add(tiro)
            self.jogo.tiros_jogador.add(tiro)
            self.shot_at = agora
            self.running = False

    def update(self):
        self.xAntes = self.pos.x
        self.acel = vec(0, JOGADOR_GRAV)

        tecla = pg.key.get_pressed()

        self.colisao()

        agora = pg.time.get_ticks() / 1000
        if self.shot_at != 0 and agora - self.shot_at < self.shot_delay * 2:
            self.atirando = False
            return

        if tecla[pg.K_LEFT]:
            self.acel.x = -JOGADOR_ACEL
            self.facing = "left"

        if tecla[pg.K_RIGHT]:
            self.acel.x = JOGADOR_ACEL
            self.facing = "right"

        if tecla[pg.K_RIGHT] or tecla[pg.K_LEFT]:
            self.play_music()
            self.running = True

        if not tecla[pg.K_RIGHT] and not tecla[pg.K_LEFT]:
            self.stop_music()

        if not tecla[pg.K_RIGHT] and self.facing == "right" or not tecla[pg.K_LEFT] and self.facing == "left":
            self.running = False
            self.walkCount = 0

        if tecla[pg.K_x]:
            self.atirar()

        if tecla[pg.K_z]:
            self.pulo()

        if tecla[pg.K_SPACE]:
            self.interagir()

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
        self.draw()
