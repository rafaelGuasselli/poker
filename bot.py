from player import Player
from math import floor, ceil
from random import shuffle, seed, randint

class Bot(Player):
	def __init__(self, cards, money, index):
		super().__init__(cards, money, "Bot", index)
	
	def decide(self, revealedCards, betAmount, amountOfPlayers):
		decision = ["", 0]
		possible = self.possibleActions(betAmount, amountOfPlayers)

		seed(randint(0, 10000000000))
		shuffle(possible)
		decision[0] = possible[0]

		if decision[0] == "bet" or decision[0] == "raise":
			minVal = int(betAmount) + 1
			maxVal = int(round(0.7 * (self.money+self.betAmount)))

			if minVal == maxVal:
				maxVal += 10

			decision[1] = randint(minVal, maxVal)

		return decision