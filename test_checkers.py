from hand_checker import HandChecker
from player import Player
from bot import Bot

handChecker = HandChecker()

hands = {
	"royalFlush":    [(11, 'C'), (13, 'C'), (12, 'C'), (10, 'E'), (10, 'C'), (2, 'E'), (1, 'C') ],
	"straightFlush": [(11, 'C'), (13, 'C'), (12, 'C'), (10, 'E'), (10, 'C'), (2, 'E'), (9, 'C') ],
	"fourOfAKind":   [(1, 'C'),  (1, 'E'),  (1, 'P'),  (1, 'O'),  (10, 'C'), (2, 'E'), (9, 'C') ],
	"fullHouse":     [(1, 'C'),  (1, 'E'),  (1, 'P'),  (12, 'O'), (12, 'C'), (2, 'E'), (9, 'C') ],
	"flush":         [(2, 'C'),  (4, 'C'),  (6, 'C'),  (1, 'E'),  (7, 'C'),  (2, 'E'), (10, 'C')],
	"straight":      [(11, 'C'), (13, 'E'), (12, 'C'), (10, 'E'), (10, 'C'), (2, 'E'), (9, 'C') ],
	"threeOfAKind":  [(1, 'C'),  (1, 'E'),  (1, 'P'),  (12, 'O'), (3, 'C'),  (2, 'E'), (9, 'C') ],
	"twoPair":       [(1, 'C'),  (1, 'E'),  (4, 'P'),  (12, 'O'), (12, 'C'), (2, 'E'), (9, 'C') ],
	"onePair":       [(1, 'C'),  (1, 'E'),  (4, 'P'),  (7, 'O'),  (12, 'C'), (2, 'E'), (9, 'C') ],
	"highCard":      [(1, 'C'),  (3, 'E'),  (4, 'P'),  (12, 'O'), (6, 'C'),  (2, 'E'), (9, 'C') ],
	"notRoyalFlush": [(10, 'E'), (6, 'O'),  (7, 'P'),  (1, 'E'),  (2, 'E'),  (2, 'E'), (1, 'C') ],
}

checkers = {
	"royalFlush": handChecker.royalFlush,
	"straightFlush": handChecker.straightFlush,
	"fourOfAKind": handChecker.fourOfAKind,
	"fullHouse": handChecker.fullHouse,
	"flush": handChecker.flush,
	"straight": handChecker.straight,
	"threeOfAKind":  handChecker.threeOfAKind,
	"twoPair":  handChecker.twoPair,
	"onePair":  handChecker.onePair,
	"highCard": handChecker.highCard
}

for key in hands:
	hand = hands[key]
	for name in checkers:
		check = checkers[name]
		cardSum = check(hand)
		if cardSum:
			print("{:s} {:s}: {:n}".format(key, name, cardSum))
	print("--------------------------------")

for key in hands:
	hand = hands[key]
	print(handChecker.checkHandValue(hand))


commonCards = [(11, 'C'), (12, 'C'), (10, 'E'), (10, 'C'), (2, 'E')]
players = {
	"royalFlush": Player([(13, 'C'),(1, 'C')], 400, "Player", 0),
 	"empate": Bot([(13, 'C'),(1, 'C')], 400, 1),
	"straightFlush": Player([(9, 'C'), (8, 'C')],400, "Player", 2),
	"fourOfAKind": Player([(10, 'P'), (10, 'O')],400, "Player", 3),
	"fullHouse": Player([(2, 'P'), (2, 'O')],400, "Player", 4),
 	"fullHouse2": Player([(12, 'P'), (12, 'O')],400, "Player", 5),
	"flush": Bot([(1, 'C'), (2, 'C')],400, 6),
	"straight": Player([(13, 'P'), (1, 'O')],400, "Player", 7),
	"threeOfAKind":  Player([(10, 'P'), (1, 'O')], 400, "Player", 8),
	"twoPair":  Player([(12, 'P'), (1, 'O')], 400, "Player", 9),
	"onePair":  Player([(1, 'P'), (3, 'O')], 400, "Player", 10),
}

winners = handChecker.checkWinner(players.values(), commonCards)
print("-----------------------")
print("Winners: ")
for player in winners:
	print(str(player))