import os

from bot import Bot
from time import sleep
from player import Player
from random import shuffle
from hand_checker import HandChecker

class GameState:
	def __init__(self):
		self.checker = HandChecker()
		self.loop = True
		self.amountOfRevealedCards = 0
		self.potAmount = 0
		self.subRound = 0
		self.betAmount = 0
		self.commonCards = []
		self.deck = []
		self.queue = []
		self.players = []
	
	def startNewMatch(self) -> None:
		self.resetMatch(int(input("Quantidade de jogadores: ")), int(input("Quantidade de bots: ")))
		self.startNewRound()
		
		while self.loop:
			if self.subRound >= 4:
				self.distributeWinnings()
				sleep(3)

				self.printGameState()
				self.continueRoundMenu()
				continue

			if len(self.queue) > 0:
				currentPlayer = self.queue[0]
				if not currentPlayer.playingThisRound:
					continue

				while True:
					self.printGameState()
					revealedCards = self.commonCards[0:self.amountOfRevealedCards]
					decision = currentPlayer.decide(revealedCards, self.betAmount)
					success = self.action(decision, currentPlayer)
					
					if success:
						self.printGameState()
						print(self.formatDecision(decision))
						sleep(3)
						break
					else:
						print("Invalid action!")
						sleep(3)

				self.queue.pop(0)
			else:
				self.nextSubRound()
				self.printGameState()
				print("Novo subround!")
				sleep(2)

	def printGameState(self) -> None:
		currentPlayer = None if len(self.queue) == 0 else self.queue[0]
		number = 1

		self.clear()
		revealedCards = self.commonCards[0:self.amountOfRevealedCards]
		print("Sub round: {:n}".format(self.subRound+1))
		print("Cartas comuns: {:s}".format(self.formatCards(revealedCards)))
		print("Valor de aposta atual: {:n}".format(self.betAmount))
		print("----------------------")
		for player in self.players:
			print(str(player), end="")
			if player == currentPlayer:
				print(" <--", end="")

			number += 1
			print()
		print("----------------------")

	def clear(self) -> None:
		os.system('cls' if os.name=='nt' else 'clear')

	def continueRoundMenu(self) -> None:
		decision = input("Novo round, novo jogo ou quit? (r ou j ou q)")

		decision = decision.lower()
		if decision == "q":
			self.loop = False
		elif decision == "j":
			self.resetMatch(int(input("Quantidade de jogadores: ")), int(input("Quantidade de bots: ")))

		self.startNewRound()
			
	def resetMatch(self, amountOfPlayers, amountOfBots) -> None:
		players = []
		for i in range(1, amountOfPlayers+1):
			players.append(Player([], 1000, input("Nome do jogado {:n}: ".format(i)), i))

		bots = [Bot([], 1000, i+amountOfPlayers) for i in range(1, amountOfBots+1)]
		self.players = players + bots

	def startNewRound(self) -> None:
		self.queue = []
		self.commonCards = []
		self.potAmount = 0
		self.betAmount = 0
		self.subRound = 0
		self.amountOfRevealedCards = 0
		self.resetDeck()

		shuffle(self.players)
		for player in self.players:
			player.cards.clear()
			player.cards.append(self.deck.pop())
			player.cards.append(self.deck.pop())
			player.betAmount = 0
			player.playingThisRound = player.money > 0
			
			if player.playingThisRound:
				self.queue.append(player)

		for i in range(0, 5):
			self.commonCards.append(self.deck.pop())
	
	def nextSubRound(self) -> None:
		self.subRound += 1
		revealCards = [0, 3, 4, 5, 5]
		for player in self.players:			
			if player.money > 0 and player.playingThisRound:
				self.queue.append(player)
	
		self.amountOfRevealedCards = revealCards[self.subRound]
		
	def resetDeck(self) -> None:
		self.deck = []
		for number in range(1, 14):
			for suit in "CEOP":
				self.deck.append((number, suit))
		shuffle(self.deck)

	#--Player Actions--
	#All in = bet(player.money)
	#Raise  = bet(x) and self.betAmount > 0
	#Bet    = bet(x) and self.betAmount = 0
	#Check  = bet(0) and self.betAmount = 0
	def action(self, decision, player) -> bool:
		if not isinstance(decision, list) and len(decision) <= 0:
			return False

		operationId = decision[0]
		operationId = operationId.lower()
		if operationId == "call":
			return self.call(player)
		elif operationId == "check":
			return self.check(player)
		elif operationId == "bet" or operationId == "raise":
			return self.bet(decision[1], player)
		elif operationId == "allin":
			return self.allIn(player)
		elif operationId == "fold":
			return self.fold(player)
		else:
			return False

	def call(self, player) -> bool:
		return self.bet(self.betAmount, player)
	
	def check(self, player) -> bool:
		return self.bet(0, player)
	
	def allIn(self, player) -> bool:
		return self.bet(player.money+player.betAmount, player)

	def bet(self, amount, player) -> bool:
		if amount < self.betAmount and amount < player.money:
			return False
		
		if amount > self.betAmount:
			self.betAmount = amount
			for p in self.players:
				if p == player: continue
				if p.playingThisRound and not p in self.queue:
					self.queue.append(p)

		player.money -= amount - player.betAmount
		self.potAmount += amount - player.betAmount 
		player.betAmount = amount
		return True

	def fold(self, player) -> bool:
		player.playingThisRound = False
		return True

	def distributeWinnings(self) -> None:
		winner = self.checker.checkWinner(self.players, self.commonCards)

		for player in winner:
			self.potAmount -= player.betAmount
			player.money += player.betAmount

		for player in winner:
			if self.betAmount <= 0:
				break

			ratio = float(player.betAmount)/float(self.betAmount)
			earnedMoney = ratio * (self.potAmount/len(winner))
			player.money += earnedMoney
			print("Vencedor {:s}! +{:n} cards: {:s}".format(str(player), earnedMoney, self.formatCards(player.cards)))
		self.startNewRound()

	def formatDecision(self, decision) -> str:
		if not isinstance(decision, list) and len(decision) <= 0:
			return ""

		if decision[0] == "raise" or decision[0] == "bet":
			return "{:s}: {:n}".format(decision[0], decision[1])
		else:
			return decision[0]

	def formatCards(self, cards) -> str:
		result = ""
		for i, card in enumerate(cards):
			if i > 0:
				result += ", "
			result += "{:n}{:s}".format(card[0], card[1])
		return result