# IA-Empires
## Trabalho da disciplina de IA 
## Engenharia de computação IFMG - Campus Bambuí - 2018/2

O trabalho consiste em montar um agente que maximize a pontuação a ser atingida de tal modo que cada jogador possa executar uma ação em cada turno (esquerda, direita, cima e baixo).

### Pré-requisitos

O projeto necessita da linguagem Python (3+) e das bibliotecas pygame, numpy e argparse.

Para instalação execute o comando

`python3 -m pip pygame numpy argparse`

## O ambiente

O ambiente do jogo é formado por um mapa representado numa matriz nxn tal que cada posição indica a altura (relevo) daquela posição no mapa (os quadrados verdes) ou se é um lago (quadrado azul). Além disso, no mapa existem 2 tipos de recursos que podem ser coletados, são eles madeira (círculo marrom) e ouro (círculo amarelo).

Cada jogador terá sua base posicionada no mapa, e, todo recurso coletado será armazenado no mesmo. Sendo assim, é necessário o jogador buscar recursos no mapa e devolvê-los ao ponto inicial. Cada jogador poderá carregar um único recurso.

Cada jogador poderá atacar o adversário para roubar recursos bem como pode interceptá-lo durante a coleta.

O jogo termina quando todos os recursos já estiverem todos dentro da base ou atingir 10.000 turnos.

### Pontuação

A pontução do jogo dá-se pela aplicação das seguintes regras em cada turno:

1. Cada movimento penaliza a pontuação pela fórmula (relevo_proximo - relevo_atual) - 1 sendo um movimento que não entre ou saia de um lago.

2. Ao entrar ou sair de um lago perde-se 10 pontos.

3. Ao pegar um recurso (sendo este um de cada vez) ganha-se 3 ou 5 pontos para madeira e outro respectivamente.

4. Ao entregar o recurso na base o jogador ganha 30 pontos para madeira e 50 para ouro quando este for coletado no mapa.

5. Ao invadir a base inimiga o atacante recebe 4 pontos e o atacado perde o mesmo valor sendo que o atacante leva ALEATORIAMENTE um único recurso consigo e sendo este entregue na base terá a bonificação de 20 pontos.

6. Se um jogador interceptar o adversário será aplicado uma das regras a seguir:

    * O jogador com a menor pontuação irá "morrer" (irá perder 5 pontos e 5 turnos e irá iniciar na base novamente)

    * O jogador de maior pontuação poderá pegar o recurso do de menor pontuação (desde que não esteja carregando nada).

    * Caso ambos estejam carregando recurso o recurso ficará no local da morte do primeiro jogador (mas quem o coletar não receberá a pontuação de coleta)

### Implementação e execução dos agentes

O módulo do agente deverá conter uma função chamada "move" com a assinatura descrita abaixo:

``move(map,resources,enemies_pos, enemies_bases, player_pos, player_base, carrying)``

Onde

1. map: Matriz (numpy) de nxn com a configuração do relevo

2. resources: Lista com tuplas no formato (LINHA,COLUNA,RECURSO) onde RECURSO pode ser 'w' (madeira) ou 'g' (ouro) representado a posição no mapa de todos os recursos disponíveis

3. enemies_pos: Lista com as tuplas (LINHA,COLUNA,CARRYING) de todos os adversários do agente. CARRYING indica se o adversário está carregando ouro ('g'), madeira ('w') ou nada (None)

4. enemies_bases: Lista com as tuplas (LINHA,COLUNA) da base de todos os adversários

5. player_pos: Tupla com a linha e coluna da posição atual do agente

6. carrying: Status do que o agente está carregando, ouro ('g'), madeira('w') ou nada (None)

A função deve retornar qual o movimento a ser feito pelo agente (1 - CIMA, 2 - BAIXO, 3 - ESQUERDA, 4 - DIREITA)

Para executar o programa basta colocar na mesma pasta do projeto o módulo com o agente e passar o seu nome na lista de execução

``python3 main.py dummy agent1 agent2 agent3``

### Disposições gerais

O código pode ser atualizado (então fique de olho com frequencia nas versões do git)

O mesmo código apresentado aqui será utilizado nos testes do dia da apresentação do trabalho