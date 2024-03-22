#!/usr/bin/python3
#-*-encoding:utf8-*-
from random import *
import random
import numpy as np

__name__ = 'O burro'

MOVE_UP = 1
MOVE_DOWN = 2
MOVE_RIGHT = 3
MOVE_LEFT = 4

nearResources = []
caminhoIda = []
caminhoVolta = []
alcance = 2

class NoLista(object):
	def __init__(self, coluna=None, linha=None, anterior=None, proximo=None, heuristica=None):
		self.coluna = coluna
		self.linha = linha
		self.anterior = anterior
		self.proximo = proximo
		self.heuristica = heuristica

class ListaDuplamenteEncadeada(object):
 
	def __init__(self):
		self.cabeca = None
		self.rabo = None
 
	def acrescentar(self, coluna, linha, anterior, proximo, fitness):
		""" Acrescenta um novo no a lista. """
		# Cria um novo no apontando para None (anterior e proximo)
		novo_no = NoLista(coluna, linha, anterior, proximo, fitness)

		# Se a cabeca eh None a lista esta vazia
		# Tanto a cabeca quanto o rabo recebem o novo no
		if self.cabeca is None:
			self.cabeca = novo_no
			self.rabo = novo_no
		# Caso contrario, se ja existir algum valor na lista
		else:
			# O anterior 'aponta' para pai passado nos parametros
			novo_no.anterior = anterior
			# O proximo sempre aponta para None
			novo_no.proximo = None
			# O proximo do rabo sempre aponta para o novo no
			self.rabo.proximo = novo_no
			# O rabo agora eh o novo no
			self.rabo = novo_no
 
	def remover(self, coluna, linha):
		""" Remove um no da lista. """
		# O no atual eh o primeiro no da lista
		no_atual = self.cabeca
		print('cheguei no remover')
 
		# Vamos procurar pelo dado que queremos remover
		# Equanto o no atual for valido
		while no_atual is not None:
			print('dendo wile')
			# Verifica se eh o dado que estamos buscando
			if no_atual.linha == linha and no_atual.coluna == coluna:
				print('achou o elemento que tem que sair')
				# Se o dado que estamos buscando esta no primeiro no
				# da lista, nao temos anterior
				if no_atual.anterior is None:
					# A cabeca 'aponta' para o proximo no da lista
					self.cabeca = no_atual.proximo
					# E o anterior do proximo no aponta para None
					Auxno = no_atual.proximo
					Auxno.anterior = None
				#	no_atual.proximo.anterior = None
				
				else:
					Auxno = no_atual.anterior
					Auxno.proximo = no_atual.proximo
					#no_atual.anterior.proximo = no_atual.proximo
					Auxno = no_atual.proximo
					Auxno.anterior = no_atual.anterior
					#no_atual.proximo.anterior = no_atual.anterior

				# Se nao eh o no que estamos buscando va para o proximo
				no_atual = no_atual.proximo
		print('retirei alguma coisa')
		return 0
 
	def mostrar(self):
		# O no atual eh o primeiro no da lista
		no_atual = self.cabeca

		no = ""
		# Para cada no valido da lista
		while no_atual is not None:
			if no_atual.anterior is None:
				no += "None "
			no += "<---> | " + str(no_atual.coluna) + ", " + str(no_atual.linha) + " | "
			if no_atual.proximo is None:
				no += "<---> None"
 
			no_atual = no_atual.proximo
		print(no)
		print("="*80)

	def buscar(self, coluna, linha):
		no_atual = self.cabeca
		flag = False
		while no_atual and no_atual.proximo != None:	
			if no_atual.linha == linha:
				if no_atual.coluna == coluna:
					flag = True
			no_atual = no_atual.proximo
		if flag == True:
			print('o buscar achou o item na lista')
		return flag

	def buscaMenor(self):
		no_atual = self.cabeca
		menorValor = no_atual.heuristica
		menorNo = no_atual
		while no_atual and no_atual.proximo != self.rabo:
			if no_atual.heuristica < menorValor:
				menorValor = no_atual.heuristica
				menorNo = no_atual

			no_atual = no_atual.proximo
		return (menorNo.coluna, menorNo.linha)

	def estaVazia(self):
		return self.cabeca.proximo == self.rabo

	def buscaAlteraFitness(self, coluna, linha, newFitness):
		no_atual = self.cabeca
		while no_atual and no_atual.proximo != self.rabo:
			if no_atual.coluna == coluna and no_atual.linha == linha:
				if no_atual.fitness > newFitness:
					no_atual.fitness = newFitness
		return no_atual.fitness

	def melhorCaminho(self):
		noInverso = self.rabo
		caminho = []
		while noInverso and noInverso.anterior != self.cabeca:
			caminho.append(noInverso.linha, noInverso.coluna)
			noInverso = noInverso.anterior
		print('caminho inverso', caminho)
		return caminho

def addNearResources(coordenada):

	global nearResources

	if len(nearResources) == 0:	#se a lista estiver vazia
		nearResources.append(coordenada) # adiciona na lista
	else:
		flag = False
		quant = len(nearResources)
		for f in range (0, quant):
			if coordenada[0] == nearResources[f][0]:
				if coordenada[1] == nearResources[f][1]: #se o item ja esta na lista nao fazer nada
					flag = True
		if flag == False:
			nearResources.append(coordenada)	#adiciona na lista

	return 0

def definicaoMov(player_pos, fila):

	if player_pos[1] > moveQueue[0][1]:	#compara a posição do player com a lista de movimentos
		mover = MOVE_UP
	if player_pos[1] < moveQueue[0][1]:
		mover = MOVE_DOWN
	if player_pos[0] > moveQueue[0][0]:
		mover = MOVE_LEFT
	if player_pos[0] < moveQueue[0][0]:
		mover = MOVE_RIGHT
	return mover

def aEstrela(map, player_pos, resources):

	global nearResources
	global caminhoIda
	global caminhoVolta

	# ## A STAR ##
	# ##FILA DE MOVIMENTOS AINDA NÃO UTILIZADOS##
	if len(caminhoIda) > 0:
		mover = definicaoMov(player_pos, caminho[0])
		caminhoIda.pop(0)
		return mover
	if len(caminhoVolta) > 0:
		mover = definicaoMov(player_pos, caminho[len(caminhoVolta)])
		caminhoVolta.pop(len(caminhoVolta))
		return mover

	##INICIANDO A BUSCA##
	#ponto de saida
	startPoint = [] #vetor da posição inicial
	startPoint.append(player_pos[0])	#colocando o ponto separado
	startPoint.append(player_pos[1])
	#ponto final
	finalPoint = nearResources[0][0], nearResources[0][1]
	#lista de caminhos abertos
	listaAberta = ListaDuplamenteEncadeada()
	#lista de caminhos fechados
	listaFechada = ListaDuplamenteEncadeada()
	#lista de vizinhos
	vizinhos = []
	#coloca o ponto inicial na lista aberta
	listaAberta.acrescentar(startPoint[0], startPoint[1], None, None, map[startPoint[0]][startPoint[1]])
	
	#controle while
	destino = False #se chegou ao objetivo
	quadradoPremiado = False	#se encontrou recurso antes de chegar ao objetivo

	while np.logical_and(destino != True, quadradoPremiado != True):
		#menor no vira pos atual
		posAtual = listaAberta.buscaMenor() 
		#removendo posAtual da lista aberta
		print('======== lista aberta =======')
		listaAberta.mostrar()
		print('minha posicaos', posAtual)
		listaAberta.remover(posAtual[0], posAtual[1])
		#adicionando na lista fechada
		custoInicial = map[posAtual[0]][posAtual[1]]	#custo da primeira celula
		listaFechada.acrescentar(posAtual[0], posAtual[1], None, None, custoInicial)
		print('======== lista fechada =======')
		listaFechada.mostrar()
		print('======== lista aberta =======')
		listaAberta.mostrar()

		print('ponto de inicio', startPoint)
		#acha os vizinhos
		if posAtual[1] - 1 > 0 and posAtual[1] - 1 < len(map) - 1: #testa limites do mapa
			#custo em cima
			custoCima = map[posAtual[0]][posAtual[1] - 1]
			#posicao de cima
			vizinhos.append((posAtual[0], posAtual[1] - 1, custoCima))
		if posAtual[1] + 1 > 0 and posAtual [1] + 1 < len(map) - 1: #testa limites do mapa
			#custo em baixo
			custoBaixo = map[posAtual[0]][posAtual[1] + 1]
			#posicao de baixo
			vizinhos.append((posAtual[0], posAtual[1] + 1, custoBaixo))
		if posAtual[0] - 1 > 0 and posAtual[0] - 1 < len(map) - 1: #testa limites do mapa
			#custo na esquerda
			custoEsquerda = map[posAtual[0] - 1][posAtual[1]]
			#posicao da esquerda
			vizinhos.append((posAtual[0] - 1, posAtual[1], custoEsquerda))
		if posAtual[0] + 1 > 0 and posAtual[0] + 1 < len(map) - 1: #testa limites do mapa
			#custo na direita
			custoDireita = map[posAtual[0] + 1][posAtual[1]]
			#posicao da direita
			vizinhos.append((posAtual[0] + 1, posAtual[1], custoDireita))

		print('posicao dos vizinhos == ' , vizinhos)


		for f in range (0, len(vizinhos)): # laco de 0 até o total de vizinhos

			if listaFechada.buscar(vizinhos[f][0], vizinhos[f][1]) == False: #se o vizinho NAO esta na lista fechada
				if vizinhos[f][2] > 0: #e o vizinho NAO é agua
					
					#se passou nos 2 acima:
					###CALCULO DE CUSTOS###
					#Gcusto custo proxima celula menos inicial
					gcusto = abs(vizinhos[f][2] - map[posAtual[0]][posAtual[1]])
					#H estimativa de todos os custos ate o destino
					#usando abs para pegar o valor absoluto
					hcusto = (abs(nearResources[0][0] - vizinhos[f][0])) + (abs(nearResources[0][1] - vizinhos[f][1]))
					#F = G + H custo total da celula
					fcusto = gcusto + hcusto
					#se o vizinho nao esta na lista aberta
					if listaAberta.buscar(vizinhos[f][0], vizinhos[f][1]) == False:
						#colocando na lista aberta, com pos Atual como pai e fcusto
						listaAberta.acrescentar(vizinhos[f][0], vizinhos[f][1], posAtual, None, fcusto)
					else: #se ja estiver na lista aberta, recalcular para achar possivel menor fitness
						listaAberta.buscaAlteraFitness(vizinhos[f][0], vizinhos[f][1], fcusto)
		#limpa o vetor de vizinhos para nao ter problemas nas proximas iteraçoes
		vizinhos.clear()

	#apos o while e todos os caminhos testados na lista fechada
	caminhoIda = listaFechada.melhorCaminho()
	caminhoVolta = caminhoIda

	print('caminho depois do return == ', caminhoIda)
	if len(caminhoIda) > 0:
		mover = definicaoMov(player_pos, caminho[0])
		caminhoIda.pop(0)

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

	start[0] = MOVE_UP

	global nearResources

	pesquisaRecursos(player_pos, resources)

	print('recursos mais proximos ============== ', nearResources)
	print('pontuação ===== ', score)
	print(e_score)

	if len(nearResources) > 0:
		start[0] = aEstrela(map, player_pos, resources)
	else:
		start[0] = MOVE_UP

	if len(nearResources) > 0:	#testa se o player nao passou por algum recurso da lista
		for y in range (0, len(nearResources) - 1):
			if player_pos[0] == nearResources[y][0] and player_pos[1] == nearResources[y][1]:
				nearResources.pop(0)

	return start[0] # Return a Action