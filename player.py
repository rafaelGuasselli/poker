class Player:
	def __init__(self, cards, money, name, index):
		self.cards = cards or []
		self.money = money or 1000
		self.playingThisRound = True
		self.betAmount = 0
		self.index = index
		self.name = name or "Player"

	def decide(self, revealedCards, betAmount):
		print("Suas cartas: {:s}".format(self.formatCards(self.cards)))

		decision = ["", 0]
		possible = self.possibleActions(betAmount)
		
		while True:
			print("Escolha uma ação: {:s}".format(self.formatChoices(possible)))
			decision[0] = input()

			if decision[0] in possible:
				break
			else:
				print("Ação invalida!")
		
		if decision[0] == "bet" or decision[0] == "raise":
			decision[1] = float(input("Qual Valor? "))

		return decision

	def possibleActions(self, betAmount):
		if betAmount == 0:
			return ["allin", "check", "bet", "fold"]
		elif betAmount > 0 and self.betAmount <= betAmount and self.betAmount + self.money > betAmount:
			return ["allin", "call", "raise", "fold"]
		else:
			return ["allin", "fold"]

	def __str__(self):
		state = "Jogando" if self.playingThisRound else "Desistiu"
		state = "Perdeu" if self.money + self.betAmount <= 0 else state
		return "{:n} - {:s} - {:s}: R${:n}".format(self.index, self.name, state, self.money)
	
	def formatChoices(self, possible):
		result = ""
		for i, choice in enumerate(possible):
			if i > 0:
				result += ", "
			result += choice
		return result
	
	def formatCards(self, cards):
		result = ""
		for i, card in enumerate(cards):
			if i > 0:
				result += ", "
			result += "{:n}{:s}".format(card[0], card[1])
		return result