#!/usr/bin/python3
#-*-encoding:utf8-*-
from random import *
import random
import numpy as np

__name__ = 'Burroritmo'

MOVE_UP = 1
MOVE_DOWN = 2
MOVE_RIGHT = 3
MOVE_LEFT = 4

#variaveis globais necessarias
nearResources = []
caminhoIda = []
caminhoVolta = []
alcance = 2

def buscaMenor(lista): #busca o menor fitness entre os elementos
	fit = lista[0][2] #fitness inicial
	indice = 0 #indice que estava
	for i in range(0, len(lista)):
		if lista[i][2] < fit:
			fit = lista[i][2]
			indice = i
	return (lista[indice][0], lista[indice][1]) #retorna linha e coluna do item com menor custo

def buscaIndice(lista, coluna, linha): # Busca da posicao de um item
	for i in range(0, len(lista)):	
		if lista[i][0] == coluna and lista[i][1] == linha: # se achar na linha
			return i # retorna posicao
	return -1 #nao esta na lista

def melhorCaminho(lista, posInicial): #apos chegar ao destino volta ao inicio passando pelos pais
	global caminhoVolta
	
	#primeiro no
	caminhoVolta.append((lista[len(lista) - 1][0], lista[len(lista) - 1][1]))
	#primeiro pai
	caminhoVolta.append((lista[len(lista) - 1][3], lista[len(lista) - 1][4]))

	while True: #loop infinito ate achar o caminho de volta
		#busca posicao do pai e adiciona seu pai
		indice = buscaIndice(lista, caminhoVolta[len(caminhoVolta) - 1][0], caminhoVolta[len(caminhoVolta) - 1][1])
		#se NAO chegou ate o inicio da lista
		if lista[indice][3] or lista[indice][4] is not None: # se tiver pai
			caminhoVolta.append((lista[indice][3], lista[indice][4])) #adiciona o pai do pai
		else: # se chegar ao ponto de inicio
			return 0	#termina

	return 0



def addNearResources(coordenada):

	global nearResources

	if len(nearResources) == 0:	#se a lista estiver vazia
		nearResources.append(coordenada) # adiciona na lista
	else:
		flag = False
		for f in range (0, len(nearResources) - 1):
			if coordenada[0] == nearResources[f][0]:
				if coordenada[1] == nearResources[f][1]: #se o item ja esta na lista nao fazer nada
					flag = True
		if flag == False:
			nearResources.append(coordenada)	#adiciona na lista

	return 0

def definicaoMov(player_col, player_lin, filaCol, filaLin):
	mover = MOVE_UP

	if player_lin > filaLin:	#compara a posição do player com a lista de movimentos
		mover = MOVE_UP
		print('movendo para (',player_col, ', ', filaLin, ')')
	if player_lin < filaLin:
		mover = MOVE_DOWN
		print('movendo para (',player_col, ', ', filaLin, ')')
	if player_col > filaCol:
		mover = MOVE_LEFT
		print('movendo para (',filaCol, ', ', player_lin, ')')
	if player_col < filaCol:
		mover = MOVE_RIGHT
		print('movendo para (',filaCol, ', ', player_lin, ')')
	return mover

def aEstrela(map, player_pos, resources):

	global nearResources
	global caminhoIda
	global caminhoVolta

	# ## A STAR ##
	# ##FILA DE MOVIMENTOS AINDA NÃO UTILIZADOS##
	if len(caminhoIda) > 0:
		mover = definicaoMov(player_pos[0], player_pos[1], caminhoIda[len(caminhoIda) - 1][0], caminhoIda[len(caminhoIda) - 1][1])
		caminhoIda.pop(len(caminhoIda) - 1)
		return mover
	if len(caminhoVolta) > 0:
		mover = definicaoMov(player_pos[0], player_pos[1], caminhoVolta[0][0], caminhoVolta[0][1])
		caminhoVolta.pop(0)
		return mover

	##INICIANDO A BUSCA##
	#ponto de saida
	startPoint = [] #vetor da posição inicial
	startPoint.append(player_pos[0])	#colocando o ponto separado
	startPoint.append(player_pos[1])
	#ponto final
	finalPoint = nearResources[0][0], nearResources[0][1]
	#lista de caminhos abertos
	listaAberta = []	#(coluna, linha, custo, paiCol, paiLin)
	#lista de caminhos fechados
	listaFechada = []
	#lista de vizinhos
	vizinhos = []
	#coloca o ponto inicial na lista aberta
	listaAberta.append((startPoint[0], startPoint[1], map[startPoint[0]][startPoint[1]], None, None))
	mover = MOVE_UP
	
	#controle while
	destino = False #se chegou ao objetivo
	quadradoPremiado = False	#se encontrou recurso antes de chegar ao objetivo

	while np.logical_and(destino != True, quadradoPremiado != True):
		
		posAtual = buscaMenor(listaAberta) #menor no vira pos atual

		#adicionando na lista fechada
		custoInicial = map[posAtual[0]][posAtual[1]]	#custo da primeira celula
		indice = buscaIndice(listaAberta, posAtual[0], posAtual[1]) # indice do menor custo na lista aberta

		if len(listaFechada) == 0: # se lista fechada tiver vazia
			listaFechada.append((posAtual[0], posAtual[1], custoInicial, None, None)) # pai valendo None
		else:
			listaFechada.append((posAtual[0], posAtual[1], custoInicial, listaAberta[indice][3], listaAberta[indice][4])) #pai transferido da lista aberta

		#removendo posAtual da lista aberta
		print('======== lista aberta =======')
		print(listaAberta)
		listaAberta.pop(indice)

		print('======== lista fechada =======')
		print(listaFechada)


		#ACHA OS VIZINHOS E SEUS CUSTOS, E COLOCAM EM UM VETOR
		if posAtual[1] - 1 >= 0 and posAtual[1] - 1 < len(map): #testa limites do mapa
			custoCima = map[posAtual[0]][posAtual[1] - 1] #custo em cima
			vizinhos.append((posAtual[0], posAtual[1] - 1, custoCima)) #posicao de cima

		if posAtual[1] + 1 >= 0 and posAtual [1] + 1 < len(map): #testa limites do mapa
			custoBaixo = map[posAtual[0]][posAtual[1] + 1] #custo em baixo
			vizinhos.append((posAtual[0], posAtual[1] + 1, custoBaixo)) #posicao de baixo

		if posAtual[0] - 1 >= 0 and posAtual[0] - 1 < len(map): #testa limites do mapa
			custoEsquerda = map[posAtual[0] - 1][posAtual[1]] #custo na esquerda
			vizinhos.append((posAtual[0] - 1, posAtual[1], custoEsquerda)) #posicao da esquerda

		if posAtual[0] + 1 >= 0 and posAtual[0] + 1 < len(map): #testa limites do mapa
			custoDireita = map[posAtual[0] + 1][posAtual[1]] 	#custo na direita
			vizinhos.append((posAtual[0] + 1, posAtual[1], custoDireita)) 	#posicao da direita

		print('posicao dos vizinhos == ' , vizinhos)


		for f in range (0, len(vizinhos)): # laco de 0 até o total de vizinhos

			if buscaIndice(listaFechada, vizinhos[f][0], vizinhos[f][1]) == -1: #se for -1 o vizinho NAO esta na lista fechada
				if vizinhos[f][2] >= 0: #e o vizinho NAO é agua
					###CALCULO DE CUSTOS###
					#Gcusto custo proxima celula menos inicial
					gcusto = abs(vizinhos[f][2] + map[posAtual[0]][posAtual[1]])
					#H estimativa de todos os custos ate o destino
					#usando abs para pegar o valor absoluto
					hcusto = (abs(nearResources[0][0] - vizinhos[f][0])) + (abs(nearResources[0][1] - vizinhos[f][1]))
					#F = G + H custo total da celula
					fcusto = gcusto + hcusto
					#se o vizinho nao esta na lista aberta
					if buscaIndice(listaAberta, vizinhos[f][0], vizinhos[f][1]) == -1: #se for -1 o vizinho NAO esta na lista aberta
						#colocando na lista aberta, com pos Atual como pai e fcusto
						listaAberta.append((vizinhos[f][0], vizinhos[f][1], fcusto, posAtual[0], posAtual[1]))
					else: #se ja estiver na lista aberta, recalcular para achar possivel menor fitness
						aux = buscaIndice(listaAberta, vizinhos[f][0], vizinhos[f][1]) #busca o indice do item
						if(listaAberta[aux][2] > fcusto):	#se o custo for menor
							listaAberta.append((vizinhos[f][0], vizinhos[f][1], fcusto, posAtual[0], posAtual[1])) #adiciona com o novo custo e pai
							listaAberta.pop(aux) # tira o antigo

		#limpando a lista de vizinhos para nao gerar erros
		vizinhos.clear()

		#testes de controle do while
		#chegou ao destino
		if np.logical_and(posAtual[0] == finalPoint[0], posAtual[1] == finalPoint[1]):
			destino = True
		#se tiver recurso no ponto
		for j in range(0, len(resources)):
			if posAtual[0] == resources[j][0] and posAtual[1] == resources[j][1]: #procurou recurso na posicao atual
				quadradoPremiado = True #fecha o while

	#apos o while e todos os caminhos testados na lista fechada
	melhorCaminho(listaFechada, startPoint) # acha o melhor caminho
	caminhoIda = caminhoVolta.copy() #copia o caminho volta para a ida
	caminhoIda.pop(len(caminhoIda) - 1) #tira a posicao atual do player
	caminhoVolta.pop(0) #tira a posicao final do player

	print('caminho ida   == ', caminhoIda)
	print('caminho volta == ', caminhoVolta)

	#começa a movimentação
	if len(caminhoIda) > 0: 
		mover = definicaoMov(player_pos[0], player_pos[1], caminhoIda[len(caminhoIda) - 1][0], caminhoIda[len(caminhoIda) - 1][1])
		caminhoIda.pop(len(caminhoIda) - 1) #retira o caminho usado

	return mover

def pesquisaRecursos(player_pos, resources):

	global nearResources
	global alcance

	### procura recursos de sua posicao ate (alcance) ###
	for visao in range (1, alcance + 1):
		for i in range (0, len(resources)):	#pesquisando pela tupla de recursos
		##PESQUISA NA HORIZONTAL##
			#CIMA
			if player_pos[1] - visao == resources[i][1]:	#testando linha com linha
				if player_pos[0] == resources[i][0]: #testando coluna com coluna
					coordenada = (player_pos[0], player_pos[1] - visao)
					addNearResources(coordenada)
			#BAIXO
			if player_pos[1] + visao == resources[i][1]:	#testando linha com linha
				if player_pos[0] == resources[i][0]:	#testando coluna com coluna
					coordenada = (player_pos[0], player_pos[1] + visao)
					addNearResources(coordenada)
			#ESQUERDA
			if player_pos[1] == resources[i][1]:	#testando linha com linha
				if player_pos[0] - visao == resources[i][0]:	#testando coluna com coluna
					coordenada = (player_pos[0] - visao, player_pos[1])
					addNearResources(coordenada)
			#DIREITA
			if player_pos[1] == resources[i][1]:	#testando linha com linha
				if player_pos[0] + visao == resources[i][0]:	#testando coluna com coluna
					coordenada = (player_pos[0] + visao, player_pos[1])
					addNearResources(coordenada)
		##PESQUISA NA DIAGONAL##
			if visao > 1:	#so tem diagonal para alcance > 1
				diagonal = visao - 1
					#diagonal cima direita
				if player_pos[1] - diagonal == resources[i][1]:	#testando linha com linha
					if player_pos[0] + diagonal == resources[i][0]: #testando coluna com coluna
						coordenada = (player_pos[0] + diagonal, player_pos[1] - diagonal)
						addNearResources(coordenada)
					#diagonal cima esquerda
				if player_pos[1] - diagonal == resources[i][1]:	#testando linha com linha
					if player_pos[0] - diagonal == resources[i][0]: #testando coluna com coluna
						coordenada = (player_pos[0] - diagonal, player_pos[1] - diagonal)
						addNearResources(coordenada)
					#diagonal baixo direita
				if player_pos[1] + diagonal == resources[i][1]:	#testando linha com linha
					if player_pos[0] + diagonal == resources[i][0]: #testando coluna com coluna
						coordenada = (player_pos[0] + diagonal, player_pos[1] + diagonal)
						addNearResources(coordenada)
				if player_pos[1] + diagonal == resources[i][1]:	#testando linha com linha
					if player_pos[0] - diagonal == resources[i][0]: #testando coluna com coluna	
						coordenada = (player_pos[0] - diagonal, player_pos[1] + diagonal)
						addNearResources(coordenada)
	return 0



def move(map,resources,enemies_pos, enemies_bases, player_pos, player_base, carrying, score, e_score):

	start = [MOVE_UP, MOVE_DOWN, MOVE_RIGHT, MOVE_LEFT]

	global nearResources

	pesquisaRecursos(player_pos, resources)

	print('recursos mais proximos ============== ', nearResources)
	print('pontuação ===== ', score)

	if len(nearResources) > 0:
		start[0] = aEstrela(map, player_pos, resources)
	else:
		random.shuffle(start)

	if len(nearResources) > 0:	#testa se o player nao passou por algum recurso da lista
		for y in range (0, len(nearResources) - 1): 
			if np.logical_and( player_pos[0] == nearResources[y][0], player_pos[1] == nearResources[y][1]): # se onde o player esta tinha um recurso, retira do nearResources
				nearResources.pop(y)

	return start[0] # Return a Action