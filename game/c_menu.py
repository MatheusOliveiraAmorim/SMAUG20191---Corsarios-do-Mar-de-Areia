import os
import pygame as pg
import random
from jogo_config import *
from c_jogador import *
from c_inimigo import *
from fase import *

font = pg.font.SysFont("arial", 16, False, False)
font_gameover = pg.font.SysFont("arial", 42, False, False)

class MenuInicial:
    def __init__(self, menu):
        self.menu = menu

        self.img_jogar = font.render("JOGAR", True, (255, 0, 0))
        self.r_jogar = self.img_jogar.get_rect()
        self.r_jogar.topleft = (LARGURA/2, ALTURA/2)

        self.img_creditos = font.render("CREDITOS", True, (255, 0, 0))
        self.r_creditos = self.img_creditos.get_rect()
        self.r_creditos.topleft = ((LARGURA/2) - 8, (ALTURA/2) + 16)

    def executando(self):
        self.eventos()

        self.menu.janela.blit(self.img_jogar, self.r_jogar.topleft)
        self.menu.janela.blit(self.img_creditos, self.r_creditos.topleft)

    def eventos(self):
        for e in pg.event.get(pg.MOUSEBUTTONDOWN):
            if self.r_jogar.collidepoint(e.pos):
                self.menu.is_jogando = True

class GameOver:
    def __init__(self, menu):
        self.menu = menu

        self.txt_morreu = font_gameover.render("VOCE FALICEU", True, (255, 0, 0))
        self.reiniciar = self.txt_morreu.get_rect()
        self.reiniciar.topleft = (LARGURA/2, ALTURA/2)

    def executando(self):
        self.menu.janela.blit(self.txt_morreu, self.reiniciar.topleft)

class Menu:
    def __init__(self, janela):
        self.janela = janela
        self.is_rodando = True
        self.is_jogando = False
        self.is_credito = False
        self.is_gameover = False

    def menu_inicial(self):
        menu_inicial = MenuInicial(self)
        menu_inicial.executando()

    def gameover(self):
        gameover = GameOver(self)
        gameover.executando()

    def executando(self):
        self.eventos()

        if self.is_gameover:
            self.gameover()
        elif not self.is_jogando:
            self.menu_inicial()

    def eventos(self):
        if pg.event.peek(pg.QUIT):
            self.is_rodando = False
