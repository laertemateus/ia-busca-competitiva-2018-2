#!/usr/bin/python3
#-*-encoding:utf8-*-

from random import *
from time import *
from numpy import *
import pygame

"""
Classe base e inicialização do trabalho de IA
sobre algoritmo de busca IFMG-Bambuí 2018/2
"""

class Game:
    """
    Classe do jogo
    """

    def __init__(self, seed = None, size = None):
        """
        Construtor da classe

        @param seed: Semente aleatória
        @param size: Tamanho do grid
        """

        # Inicializa atributos da classe
        self.__rand = Random(time() if seed is None else seed)
        self.__size = 50 if size is None else size

        # Constrói o mapa
        self.__map = ndarray([self.__size,self.__size],int)
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


    def __update():
        """
        Atualiza o jogo
        """
        pass

    def run(self):
        """
        Desenha e executa o jogo
        """

        running = True

        # Pygame init config
        pygame.init()
        pygame.display.set_caption('Hello world!')
        pygame.display.set_mode((500, 400), 0, 32)

        while running:
            self.__update()
            self.__display()
            pygame.time.delay(3000)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    running = False





if __name__ == '__main__':
    game = Game()
    game.run()