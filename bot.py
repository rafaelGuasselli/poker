from player import Player
from random import shuffle, randint

class Bot(Player):
	def __init__(self, cards, money, index):
		super().__init__(cards, money, "Bot", index)
	
	def decide(self, revealedCards, betAmount):
		decision = ["", 0]
		possible = self.possibleActions(betAmount)

		shuffle(possible)
		decision[0] = possible[0]
		if decision[0] == "bet" or decision[0] == "raise":
			minVal = betAmount + 1
			maxVal = round(0.7 * (self.money+self.betAmount))
			decision[1] = randint(minVal, maxVal)

		return decision