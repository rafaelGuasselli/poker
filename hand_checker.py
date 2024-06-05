#Hearts,Spades,Diamonds,Clubs
#Copas, Espadas, Ouros, Paus
#1H, 2H, 3H, 4H, 5H, 6H, 7H, 8H, 9H, 10H, 11H, 12H, 13H
#1E, 2E, 3E, 4E, 5E, 6E, 7E, 8E, 9E, 10E, 11E, 12E, 13E
from functools import cmp_to_key, reduce

class HandChecker:
	def __init__(self):
		self.cardValue = { 1: 14, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13 }
		
	def checkWinner(self, players, commonCards):
		values = []

		for player in players:
			if player.playingThisRound:
				value = self.checkHandValue(player.cards+commonCards)
				values.append((value, player))
		
		values.sort(reverse=True, key=lambda val:val[0])
		winners = []
		previousValue = 0
		for playerValue in values:
			value, player = playerValue
			if value >= previousValue:
				winners.append(player)
				previousValue = value
				
		return winners
	
	def checkHandValue(self, hand):
		checkers = [
			self.royalFlush,    # 10 * 100 + valorDaMelhorCombinação
			self.straightFlush, # 9  * 100 + valorDaMelhorCombinação
			self.fourOfAKind,   # 8  * 100 + valorDaMelhorCombinação
			self.fullHouse,     # 7  * 100 + valorDaMelhorCombinação
			self.flush,         # 6  * 100 + valorDaMelhorCombinação
			self.straight,		# 5  * 100 + valorDaMelhorCombinação
			self.threeOfAKind,	# 4  * 100 + valorDaMelhorCombinação
			self.twoPair,		# 3  * 100 + valorDaMelhorCombinação
			self.onePair,		# 2  * 100 + valorDaMelhorCombinação
			self.highCard		# 1  * 100 + valorDaMelhorCombinação
		]

		for i, check in enumerate(checkers):
			value = len(checkers) - i
			cardSum = check(hand)
			if cardSum:
				return value * 100 + cardSum
		return 0
	
	def royalFlush(self, hand):
		hand = self.straightPreProccessCards(hand)

		previousSuit = "SHDC"
		previousNumber = 15

		if len(hand) < 5:
			return 0

		for i in range(0, 5):
			number, suit = hand[i]
			
			if number != previousNumber-1 or not self.hasSuit(suit, previousSuit):
				return 0

			previousSuit = suit
			previousNumber = number
		return 60
	
	def straightFlush(self, hand):
		hand = self.straightPreProccessCards(hand)

		startIndex = -1
		previousSuit = "SHDC"
		previousNumber = -1
		cardSum = 0

		for i in range(0, len(hand)):
			number, suit = hand[i]
			if number != previousNumber-1 or not self.hasSuit(suit, previousSuit):
				startIndex = i
				cardSum = 0

			cardSum += number
			if i - startIndex + 1 >= 5:
				break

			previousSuit = suit
			previousNumber = number

		if startIndex > 2 or len(hand) < 5:
			return 0

		return cardSum

	def fourOfAKind(self, hand):
		hand = self.straightPreProccessCards(hand)
		for card in hand:
			if len(card[1]) == 4:
				return card[0] * 4

		return 0
	
	def fullHouse(self, hand):
		hand = self.straightPreProccessCards(hand)
		treeOfAKind = 0
		twoOfAKind = 0
	
		for card in hand:
			if len(card[1]) == 3:
				treeOfAKind = max(treeOfAKind, card[0] * 3)

			if len(card[1]) == 2:
				twoOfAKind = max(twoOfAKind, card[0] * 2)
	
			if twoOfAKind and treeOfAKind:
				return twoOfAKind + treeOfAKind

		return 0
	
	def flush(self, hand):
		hand = self.flushPreProccessCards(hand)
		
		for suit in hand:
			cards = hand[suit]
			if len(cards) >= 5:
				return reduce(lambda a,b: a+b, cards[0:5])

		return 0

	def straight(self, hand):
		hand = self.straightPreProccessCards(hand)

		startIndex = -1
		previousNumber = -1
		cardSum = 0

		for i in range(0, len(hand)):
			number, suit = hand[i]
			if number != previousNumber-1:
				startIndex = i
				cardSum = 0
			
			cardSum += number
			if i - startIndex + 1 >= 5:
				break

			previousNumber = number

		if startIndex > 2 or len(hand) < 5:
			return 0

		return cardSum
	
	def threeOfAKind(self, hand):
		hand = self.straightPreProccessCards(hand)

		for card in hand:
			if len(card[1]) == 3:
				return card[0] * 3

		return 0
	
	def twoPair(self, hand):
		hand = self.straightPreProccessCards(hand)
		pairsFound = 0

		for card in hand:
			if len(card[1]) == 2 and not pairsFound:
				pairsFound = card[0]
			elif len(card[1]) == 2:
				return card[0] * 2 + pairsFound * 2

		return 0
	
	def onePair(self, hand):
		hand = self.straightPreProccessCards(hand)
		for card in hand:
			if len(card[1]) == 2:
				return card[0] * 2

		return 0

	def highCard(self, hand):
		hand = self.straightPreProccessCards(hand)
		cardSum = 0
		for card in hand[0:5]:
			cardSum += card[0]
		return cardSum

	def hasSuit(self, a, b):
		for suit in a:
			if suit in b:
				return True
		return False
	
	def straightPreProccessCards(self, hand):
		hand.sort(key=cmp_to_key(self.compareCards))
		
		newHand = []
		for card in hand:
			number, suit = card
			number = self.cardValue[number]
			if len(newHand) > 0 and number == newHand[-1][0]:
				newHand[-1][1] += suit
			else:
				newHand.append([number, suit])

		return newHand
	
	def flushPreProccessCards(self, hand):
		hand.sort(key=cmp_to_key(self.compareCards))
		newHand = {
			"E": [],
			"C": [],
			"O": [],
			"P": []
		}

		for card in hand:
			number, suit = card
			number = self.cardValue[number]			
			newHand[suit].append(number)

		return newHand

	def compareCards(self, a, b):
		if self.cardValue[a[0]] < self.cardValue[b[0]]:
			return 1

		if self.cardValue[a[0]] > self.cardValue[b[0]]:
			return -1

		return 0