#!/usr/bin/python3
#-*-encoding:utf8-*-

from random import *
from time import *
import numpy as np
import pygame
import os

"""
Classe base e inicialização do trabalho de IA
sobre algoritmo de busca IFMG-Bambuí 2018/2
"""

class Game:
    """
    Classe do jogo
    """

    def __init__(self, seed = None, size = 30):
        """
        Construtor da classe

        @param seed: Semente aleatória
        @param size: Tamanho do grid
        """

        # Inicializa atributos da classe
        self.__rand = Random(time() if seed is None else seed)
        self.__size = size

        # Constrói o mapa
        self.__map = np.ndarray([self.__size,self.__size],int)
        water_prob = .02 + self.__rand.random() * .10

        for i in range(self.__size):
            for j in range(self.__size):
                r = self.__rand.random()

                if r < water_prob: self.__map[i,j] = -1
                else: self.__map[i,j] = int(self.__rand.random() * 10)

        # Cria e posiciona os recursos no mapa
        total_resources = int(15 + self.__size / 5)
        self.__resources = list()

        for i in range(total_resources):
            while True:
                m = int(self.__rand.random() * self.__size)
                n = int(self.__rand.random() * self.__size)

                if (m,n) not in self.__resources and self.__map[m,n] != -1:
                    self.__resources.append((m,n, 'w' if .5 < self.__rand.random() else 'g'))
                    break


    def __update(self):
        """
        Atualiza o jogo
        """
        pass
        
    def __display(self):
        """
        Renderiza na tela o jogo
        """
        # Calcula o tamanho do bloco
        bw = 900 / self.__size
        step = 0

        # Mapa
        for i,j in np.ndindex(self.__map.shape):
            c = pygame.Color(0,0,255,255) if self.__map[i,j] == -1 else pygame.Color(0, 25 + int(25 * self.__map[i,j]),0,255)
            pygame.draw.rect(pygame.display.get_surface(), c, (i*bw, j*bw, bw, bw))

        # Bordas
        while step <= 900:
            pygame.draw.line(pygame.display.get_surface(), pygame.Color('white'), (step,0), (step,900))
            pygame.draw.line(pygame.display.get_surface(), pygame.Color('white'), (0,step), (900,step))
            step += bw

        pygame.display.update()

    def run(self):
        """
        Desenha e executa o jogo
        """

        running = True

        # Pygame init config
        pygame.init()
        pygame.display.set_caption('Hello world!')
        pygame.display.set_mode((900, 900), 0, 32)

        while running:
            self.__update()
            self.__display()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    running = False





if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    game = Game(size=20)
    game.run()