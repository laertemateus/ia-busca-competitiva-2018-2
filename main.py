#!/usr/bin/python3
#-*-encoding:utf8-*-

#
# MÓDULOS
#
import time
import numpy as np
import pygame
import os
import argparse
import copy
import random

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
        self.__scores = list()
        self.__positions = list()
        self.__carry = list()
        self.__death_coutdown = list()
        self.__turn = 0
        
        # Constrói o mapa
        self.__map = np.ndarray([self.__size,self.__size],int)
        water_prob = .07 + self.__rand.random() * .10

        for i in range(self.__size):
            for j in range(self.__size):
                r = self.__rand.random()

                if r < water_prob: self.__map[i,j] = -1
                else: self.__map[i,j] = int(self.__rand.random() * 10)

        # Cria e posiciona os recursos no mapa
        total_resources = int(self.__size * 10)
        self.__resources = list()

        for i in range(total_resources):
            while True:
                m = int(self.__rand.random() * self.__size)
                n = int(self.__rand.random() * self.__size)
                resources = list()

                if (m,n) not in map(lambda x:(x[0],x[1]),self.__resources) and self.__map[m,n] != -1:
                    self.__resources.append((m,n, 'w' if .5 < self.__rand.random() else 'g', True))
                    break

    def add_agent(self, agent):
        """
        Adiciona o Agente ao ambiente

        @param agent: Módulo do agente
        """
        self.__agents.append(agent)
        self.__scores.append(0)

        while True:
            m = int(self.__rand.random() * self.__size)
            n = int(self.__rand.random() * self.__size)

            if (m,n) not in map(lambda x:(x[0],x[1]),self.__resources) and self.__map[m,n] != -1:
                self.__bases.append((m,n))
                self.__positions.append((m,n))
                self.__carry.append(None)
                self.__death_coutdown.append(0)
                break

    def __update(self):
        """
        Atualiza o jogo
        """

        # Para o jogo se chegar à 10.000 turnos
        if self.__turn == 1e4:
            pass

        # Requisita aos agentes o movimento
        for i,a in enumerate(self.__agents):

            # Verifica se o agente está inativo
            if self.__death_coutdown[i] > 0:
                self.__death_coutdown[i] -= 1
                continue

            e_bases = self.__bases[:]
            e_scores = self.__scores[:]
            e_positions = list()
            del e_bases[i]
            del e_scores[i]

            # Informações do inimigo
            for j,x in enumerate(self.__agents):
                if j != i:
                    e_positions.append((self.__positions[j][0],self.__positions[j][1],self.__carry[j]))

            m = a.move(np.copy(self.__map), self.__resources[:], e_positions, e_bases, self.__positions[i][:], self.__bases[i][:], copy.copy(self.__carry[i]), self.__scores[i], e_scores)
            k1 = (self.__positions[i][0],self.__positions[i][1])

            if m == 1: # Mover para cima
                k2 = (self.__positions[i][0],self.__positions[i][1]-1)
            elif m == 2: # Mover para baixo
                k2 = (self.__positions[i][0],self.__positions[i][1]+1)
            elif m == 3: # Mover para a direita
                k2 = (self.__positions[i][0]+1,self.__positions[i][1])
            elif m == 4: # Mover para a esquerda
                k2 = (self.__positions[i][0]-1,self.__positions[i][1])

            # Atualiza pontuação baseado novimento e a posição do agente
            self.__scores[i] += -abs(self.__map[k1[0]][k1[1]] - self.__map[k2[0]][k2[1]]) - 1 if self.__map[k1[0]][k1[1]] != -1 and self.__map[k2[0]][k2[1]] != -1 else -10
            self.__positions[i] = (k2[0], k2[1])

            # Verifica se o agente chegou à base com recurso
            if self.__positions[i] == self.__bases[i] and self.__carry[i] is not None:
                self.__scores[i] += 30 if self.__carry[i] == 'w' else 50
                self.__carry[i] = None
            
            # Verifica se o agente está sob um recurso
            if self.__positions[i] in map(lambda x:(x[0],x[1]),self.__resources) and self.__carry[i] is None:
                p = list(map(lambda x:(x[0],x[1]),self.__resources)).index(self.__positions[i])
                self.__carry[i] = self.__resources[p][-2]
                del self.__resources[p]

        # Verifica se houve alguma colisão entre os agentes
        for i in range(len(self.__agents)):
            for j in range(i):
                if self.__positions[i] == self.__positions[j]:

                    # Verifica quem deve ser penalizado
                    if self.__scores[i] < self.__scores[j]:
                        if self.__carry[i] is not None:
                            self.__resources.append((self.__positions[i][0], self.__positions[i][1], self.__carry[i], False))
                            self.__carry[i] = None

                        self.__scores[i] -= 5
                        self.__scores[j] += 5
                        self.__positions[i] = (self.__bases[i][0], self.__bases[i][1])
                        self.__death_coutdown[i] = 5
                    
                    if self.__scores[j] < self.__scores[i]:
                        if self.__carry[j] is not None:
                            self.__resources.append((self.__positions[j][0], self.__positions[j][1], self.__carry[j], False))
                            self.__carry[j] = None

                        self.__scores[j] -= 5
                        self.__scores[i] += 5
                        self.__positions[j] = (self.__bases[j][0], self.__bases[j][1])
                        self.__death_coutdown[j] = 5
        
    def __display(self):
        """
        Renderiza na tela o jogo
        """
        # Calcula o tamanho do bloco
        bw = 900 / self.__size
        step = 0

        # Background
        pygame.draw.rect(pygame.display.get_surface(), pygame.Color('white'), (0,0,1300,900))

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
        for i,j,t,collected in self.__resources:
            c = pygame.Color('yellow') if t == 'g' else pygame.Color('brown')
            pygame.draw.ellipse(pygame.display.get_surface(), c, (i*bw + 1,j*bw + 1, bw - 1, bw - 1))

        # Bases
        for i,b in enumerate(self.__bases):
            pygame.display.get_surface().blit(pygame.transform.scale(self.__house, (int(bw),int(bw))), (b[0] * bw, b[1] * bw))

        # Agentes
        for i,a in enumerate(self.__agents):
            pygame.display.get_surface().blit(pygame.transform.scale(self.__sprites[i], (int(bw),int(bw))), (self.__positions[i][0] * bw, self.__positions[i][1] * bw) )

        pygame.display.update()

    def run(self):
        """
        Desenha e executa o jogo
        """

        running = True

        # Pygame init
        pygame.init()
        pygame.display.set_caption('IA-Empires!')
        pygame.display.set_mode((1000, 750), 0, 32)

        # Carrega os sprites
        self.__sprites = [
            pygame.image.load('sprites/seiya.png').convert_alpha(),
            pygame.image.load('sprites/shiryu.png').convert_alpha(),
            pygame.image.load('sprites/shun.png').convert_alpha(),
            pygame.image.load('sprites/ikki.png').convert_alpha(),
            pygame.image.load('sprites/hyoga.png').convert_alpha(),
        ]
        self.__house = pygame.image.load('sprites/house.png').convert_alpha()

        # Toca a música tema
        pygame.mixer.music.load('sfx/theme.mp3')
        pygame.mixer.music.play(loops=-1)

        while running:
            self.__update()
            self.__display()
            pygame.time.wait(1000)

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