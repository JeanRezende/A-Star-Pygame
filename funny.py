#!/usr/bin/python3
#-*-encoding:utf8-*-
from random import *
import random

__name__ = 'The Dummy Agent'

MOVE_UP = 1
MOVE_DOWN = 2
MOVE_RIGHT = 3
MOVE_LEFT = 4

def move(map,resources,enemies_pos, enemies_bases, player_pos, player_base, carrying, score, e_score):
	
	start = [MOVE_UP, MOVE_DOWN, MOVE_RIGHT, MOVE_LEFT]
	random.shuffle(start)

	print(player_pos)

	### Retornando pra base ###
	if carrying != None:
		if player_base[1] < player_pos[1]:
			start[0] = MOVE_UP
		if player_base[1] > player_pos[1]:
			start[0] = MOVE_DOWN
		if player_base[0] < player_pos[0]:
			start[0] = MOVE_LEFT
		if player_base[0] > player_pos[0]:
			start[0] = MOVE_RIGHT
		return start[0]

	### teste dos limites do mapa ###
	if carrying == None:
		if player_pos[0] >= len(map) - 1: #se chegar aos limites da direita
			start = [MOVE_UP, MOVE_LEFT, MOVE_DOWN]
			random.shuffle(start)

		if player_pos[0] <= 0: # se chegar aos limites da esquerda
			start = [MOVE_RIGHT, MOVE_DOWN, MOVE_UP]
			random.shuffle(start)

		if player_pos[1] >= len(map) - 1: #se chegar aos limites de baixo
			start = [MOVE_UP, MOVE_RIGHT, MOVE_LEFT]

			if player_pos[0] >= len(map) - 1: #se chegar aos limites de baixo e da direita
				start = [MOVE_LEFT, MOVE_UP]

			if player_pos[0] <= 0: #se chegar aos limites de baixo e da esquerda
				start = [MOVE_RIGHT, MOVE_UP]

			random.shuffle(start)

		if player_pos[1] <= 0: #se chegar aos limites de cima
			start = [MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT]

			if player_pos[0] >= len(map) - 1: #se chegar aos limites de cima e da direita
				start = [MOVE_LEFT, MOVE_DOWN]

			if player_pos[0] <= 0: #se chegar aos limites de baixo e da esquerda
				start = [MOVE_RIGHT, MOVE_DOWN]

			random.shuffle(start)


	###procurando recursos###
	#teste recurso em cima
	for i in range (0, len(resources)):	#pesquisando pela tupla de recursos
		if player_pos[1] - 1 == resources[i][1]:	#testando linha com linha
			if player_pos[0] == resources[i][0]: #testando coluna com coluna
				start[0] = MOVE_UP

	#teste recurso em baixo
	for i in range (0, len(resources)):	#pesquisando pela tupla de recursos
		if player_pos[1] + 1 == resources[i][1]:	#testando linha com linha
			if player_pos[0] == resources[i][0]:	#testando coluna com coluna
				start[0] = MOVE_DOWN

	#teste recurso na esquerda
	for i in range (0, len(resources)):	#pesquisando pela tupla de recursos
		if player_pos[1] == resources[i][1]:	#testando linha com linha
			if player_pos[0] - 1 == resources[i][0]:	#testando coluna com coluna
				start[0] = MOVE_LEFT

	#teste recurso na  direita
	for i in range (0, len(resources)):	#pesquisando pela tupla de recursos
		if player_pos[1] == resources[i][1]:	#testando linha com linha
			if player_pos[0] + 1 == resources[i][0]:	#testando coluna com coluna
				start[0] = MOVE_RIGHT

	print('pontuação ====', score)


	return start[0] # Return a Action