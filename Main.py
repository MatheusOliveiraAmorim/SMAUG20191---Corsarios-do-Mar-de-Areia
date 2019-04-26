import pygame

pygame.init()

janela = pygame.display.set_mode((500, 500))

idioma = 0

titulo_port = "Corsários do Mar de Areia"
titulo_eng = "Corsairs of the Sand Sea"


if (idioma == 0):
    pygame.display.set_caption(titulo_port)
else:
    pygame.display.set_caption(titulo_eng)

#sprites = {"aDireita":[],"aEsquerda":[]}
#aDireita = []
#aEsquerda = []

clock = pygame.time.Clock()

class spritesheet(object):
    def __init__(self, arquivo, nLinha, nColuna):
        self.folha = pygame.image.load(arquivo).convert_alpha()
        self.nColuna = nColuna
        self.nLinha = nLinha
        self.totalCel = nLinha * nColuna
        self.ret = self.folha.get_rect()#traz largura e altura, largura e altura / 2
        cLarg  = self.largCel = self.ret.width / nColuna #define a largura da célula do sprite
        cAlt = self.altCel = self.ret.height / nLinha #define a altura da célula do sprite
        mAlt, mLarg  = self.centroCel = (cLarg/2, cAlt/2) #metade da largura e altura do sprite (centro)
        #define as células da spritesheet em index
        self.nCelula = list ([(index % nColuna * cLarg, index / nColuna * cAlt, cLarg, cAlt) for index in range(self.totalCel)])
        #define a coordenada do sprite no plano cartesiano#
        self.coordenada = list([
            (0,0),(-mLarg,0),(-cLarg,0),
            (0, -mAlt), (-mLarg, -mAlt),(-cLarg, -mAlt),
            (0, -cAlt), (-mLarg, -cAlt), (-cLarg, -cAlt)])

    def desenhar(self, superficie, celIndex, x, y, coordenada=0):
        superficie.blit(self.folha, (x + self.coordenada[coordenada][0], x + self.coordenada[coordenada][1]), self.nCelula[celIndex])

class jogador(object):
    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.velo = 5
        self.vPulo = False
        self.vCarr = False
        self.contPulo = 10
        self.esquerda = False
        self.direita = False
        self.contPasso = 0
        self.parado = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)


    # def desenhar(self, janela):
    #     if self.contPasso + 1 >= 27:
    #         self.contPasso = 0
    #     if not (self.parado):
    #         if self.esquerda:
    #             janela.blit(aEsquerda[self.contPasso // 3], (self.x, self.y))
    #             self.contPasso += 1
    #         elif self.direita:
    #             janela.blit(aDireita[self.contPasso // 3], (self.x, self.y))
    #             self.contPasso += 1
    #     else:
    #         if self.direita:
    #             janela.blit(aDireita[0], (self.x, self.y))
    #         else:
    #             janela.blit(aEsquerda[0], (self.x, self.y))
    #     #self.hitbox = (self.x + 17, self.y + 11, 29, 52)
    #     #pygame.draw.rect(janela, (255, 0,0), self.hitbox, 2)



run = True
while run:
    clock.tick(27)