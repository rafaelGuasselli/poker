class Player:
	def __init__(self, cards, money, name, index):
		self.cards = cards or []
		self.money = money or 1000
		self.playingThisRound = True
		self.betAmount = 0
		self.index = index
		self.name = name or "Player"

	def decide(self, revealedCards, betAmount, amountOfPlayers):
		print("Suas cartas: {:s}".format(self.formatCards(self.cards)))

		decision = ["", 0]
		possible = self.possibleActions(betAmount, amountOfPlayers)
		
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

	def possibleActions(self, betAmount, amountOfPlayers):
		possible = []
		if betAmount == 0:
			possible = ["allin", "check", "bet", "fold"]
		elif self.betAmount == betAmount:
			possible = ["allin", "check", "raise", "fold"]
		elif self.betAmount < betAmount and self.betAmount + self.money > betAmount:
			possible = ["allin", "call", "raise", "fold"]
		else:
			possible = ["allin", "fold"]
		
		if amountOfPlayers == 1:
			possible.pop()
		
		return possible

	def __str__(self):
		state = "Jogando" if self.playingThisRound else "Desistiu"
		state = "Perdeu" if self.money + self.betAmount <= 0 else state
		return "{:s}({:n}) - {:s}: R${:n}".format(self.name, self.index, state, self.money)
	
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