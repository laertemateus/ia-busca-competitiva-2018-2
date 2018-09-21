#!/usr/bin/python3
#-*-encoding:utf8-*-

import random

__name__ = 'The Dummy Agent'

MOVE_UP = 1
MOVE_DOWN = 2
MOVE_RIGHT = 3
MOVE_LEFT = 4

def move(map,resources,enemies_pos, enemies_bases, player_pos, player_base, carrying):
    m = [MOVE_UP, MOVE_DOWN, MOVE_RIGHT, MOVE_LEFT]
    random.shuffle(m)

    return m[0] # Return a Action