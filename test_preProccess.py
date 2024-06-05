from hand_checker import HandChecker
handChecker = HandChecker()

handStraight = handChecker.straightPreProccessCards([(10, 'E'), (6, 'O'), (7, 'P'), (1, 'E'), (2, 'E'), (2, 'C'), (1, 'C')])
handFlush = handChecker.flushPreProccessCards([(10, 'E'), (6, 'O'), (7, 'P'), (1, 'E'), (2, 'E'), (2, 'C'), (1, 'C')])
for card in handStraight:
	print("{:n} {:s}".format(card[0], card[1]))

print("--------------------")
for suit in handFlush:
	cards = handFlush[suit]
	print("{:s} {:s}".format(suit, str(cards)))