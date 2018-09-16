#!/usr/bin/python3
#-*-encoding:utf8-*-

import random
import time
import numpy as np
import pygame
import os
import argparse

"""
Classe base e inicialização do trabalho de IA
sobre algoritmo de busca IFMG-Bambuí 2018/2
"""

class Game:
    """
    Classe do jogo
    """

    def __init__(self, seed, size):
        """
        Construtor da classe

        @param seed: Semente aleatória
        @param size: Tamanho do grid
        """

        # Inicializa atributos da classe
        self.__rand = random.Random(time.time() if seed is None else seed)
        self.__size = 30 if size is None else size
        self.__agents = list()
        self.__bases = list()

        # Constrói o mapa
        self.__map = np.ndarray([self.__size,self.__size],int)
        water_prob = .07 + self.__rand.random() * .10

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

    def add_agent(self, agent):
        """
        Adiciona o Agente ao ambiente

        @param agent: Módulo do agente
        """
        self.__agents.append(agent)

        while True:
            m = int(self.__rand.random() * self.__size)
            n = int(self.__rand.random() * self.__size)

            if (m,n) not in self.__resources and self.__map[m,n] != -1:
                self.__bases.append((m,n))
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
            c = pygame.Color(0,0,255,255) if self.__map[i,j] == -1 else pygame.Color(0, 100 + int(15 * self.__map[i,j]),0,255)
            pygame.draw.rect(pygame.display.get_surface(), c, (i*bw, j*bw, bw, bw))

        # Bordas
        while step <= 900:
            pygame.draw.line(pygame.display.get_surface(), pygame.Color('white'), (step,0), (step,900))
            pygame.draw.line(pygame.display.get_surface(), pygame.Color('white'), (0,step), (900,step))
            step += bw

        # recursos
        for i,j,t in self.__resources:
            c = pygame.Color('yellow') if t == 'g' else pygame.Color('brown')
            pygame.draw.ellipse(pygame.display.get_surface(), c, (i*bw + 1,j*bw + 1, bw - 1, bw - 1))

        pygame.display.update()

    def run(self):
        """
        Desenha e executa o jogo
        """

        running = True

        # Pygame init
        pygame.init()
        pygame.display.set_caption('IA-Empires!')
        pygame.display.set_mode((900, 900), 0, 32)

        while running:
            self.__update()
            self.__display()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    running = False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Configuração do ArgParse
    parser.add_argument('--size', help='World Size',type=int,default=30)
    parser.add_argument('--seed', help='Seed for Pseudo-Random numbers',type=float,default=None)
    parser.add_argument('agents', help='Agents to be used in the execution',type=str,nargs='+')
    args = parser.parse_args()

    # Configuração do ambiente
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    game = Game(args.seed,args.size)
    
    # Registro dos agentes
    for a in args.agents:
        am = __import__(a)
        print('Registring %s...'%am.__name__)
        game.add_agent(am)

    game.run()