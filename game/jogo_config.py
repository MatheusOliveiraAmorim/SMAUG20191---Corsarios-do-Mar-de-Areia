import os
import pygame as pg

#opções e variaves imutaveis do jogo
TITULO = "Corsários do Mar de Areia"
LARGURA = 1280
ALTURA = 720
FPS = 60

#Propriedades de jogador
JOGADOR_ACEL = 0.8
JOGADOR_FRIC = -0.12
JOGADOR_GRAV = 0.85
JOGADOR_PULO = 25

#C:/Users/Matheus/PycharmProjects/SMAUG20191---Corsarios-do-Mar-de-Areia/game/asset/image/char

dirname = os.path.dirname(__file__)

char_r = pg.image.load(os.path.join(dirname, 'asset/image/char/pnp_idle_right.png'))
char_l = pg.image.load(os.path.join(dirname, 'asset/image/char/pnp_idle_left.png'))

walkRight = [pg.image.load(os.path.join(dirname, 'asset/image/char/pnp_right_01.png')), pg.image.load(os.path.join(dirname, 'asset/image/char/pnp_right_02.png')),
             pg.image.load(os.path.join(dirname, 'asset/image/char/pnp_right_03.png')), pg.image.load(os.path.join(dirname, 'asset/image/char/pnp_right_04.png'))]

walkLeft = [pg.image.load(os.path.join(dirname, 'asset/image/char/pnp_left_01.png')), pg.image.load(os.path.join(dirname, 'asset/image/char/pnp_left_03.png')),
            pg.image.load(os.path.join(dirname, 'asset/image/char/pnp_left_02.png')), pg.image.load(os.path.join(dirname, 'asset/image/char/pnp_left_04.png'))]

# char_r = pg.image.load('asset\image\char\pnp_idle_right.png')
# char_l = pg.image.load('asset\image\char\pnp_idle_left.png')

# walkRight = [pg.image.load('asset\image\char\pnp_right_01.png'), pg.image.load('asset\image\char\pnp_right_02.png'),
#              pg.image.load('asset\image\char\pnp_right_03.png'), pg.image.load('asset\image\char\pnp_right_04.png')]

# walkLeft = [pg.image.load('asset\image\char\pnp_left_01.png'), pg.image.load('asset\image\char\pnp_left_03.png'),
#             pg.image.load('asset\image\char\pnp_left_02.png'), pg.image.load('asset\image\char\pnp_left_04.png')]

#Paleta de cores (VALORES EM RGB)
BRANCO = (255,255,255)
PRETO = (0,0,0)
VERMELHO = (255,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)
AMARELO = (255,255,0)
