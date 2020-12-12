import random


class Deck:
	''' 
	This is a class to handle the operations that a normal game of 22 would require.
	'''

	def __init__(self):
		''' 
		initializing a deck is as simple as generating the cards that are in a full deck 
		''' 

		self.cards = []
		self.generate()
		self.cards_remaining = len(self.cards)



	def generate(self, number_of_suits=4):
		''' 
		A deck is generated at the beginning of every game and then regenerated any time there are insufficient cards to deal a new round.
		'''

		self.cards = []

		# Create a literal list of dicts. Suits don't matter in 22. 
		cards_list = [
		{"face": "2", "value": 2, "score_value": 2, "deal_2": 5, "deal_3": 5, "deal_4": 5, 'ind': 0},
		{"face": "3", "value": 3, "score_value": 3, "deal_2": 5, "deal_3": 5, "deal_4": 5, 'ind': 1},
		{"face": "4", "value": 4, "score_value": 4, "deal_2": 5, "deal_3": 5, "deal_4": 5, 'ind': 2},
		{"face": "5", "value": 5, "score_value": 5, "deal_2": 5, "deal_3": 5, "deal_4": 5, 'ind': 3},
		{"face": "6", "value": 6, "score_value": 6, "deal_2": 6, "deal_3": 6, "deal_4": 6, 'ind': 4},
		{"face": "7", "value": 7, "score_value": 7, "deal_2": 7, "deal_3": 7, "deal_4": 7, 'ind': 5},
		{"face": "8", "value": 8, "score_value": 8, "deal_2": 8, "deal_3": 8, "deal_4": 7, 'ind': 6},
		{"face": "9", "value": 9, "score_value": 9, "deal_2": 9, "deal_3": 9, "deal_4": 7, 'ind': 7},
		{"face": "10", "value": 10, "score_value": 10, "deal_2": 10, "deal_3": 10, "deal_4": 7, 'ind': 8},
		{"face": "J", "value": 11, "score_value": 10, "deal_2": 10, "deal_3": 10, "deal_4": 7, 'ind': 9},
		{"face": "Q", "value": 12, "score_value": 10, "deal_2": 10, "deal_3": 10, "deal_4": 7, 'ind': 10},
		{"face": "K", "value": 13, "score_value": 10, "deal_2": 10, "deal_3": 10, "deal_4": 7, 'ind': 11},
		{"face": "A", "value": 14, "score_value": 11, "deal_2": 11, "deal_3": 11, "deal_4": 7, 'ind': 12}]


		for i in range(number_of_suits):
			for each in cards_list:
				self.cards.append(Card(each['face'], each['value'], each['score_value'], each['deal_2'], each['deal_3'], each['deal_4'], each['ind']))

		self.cards_remaining = len(self.cards)



	def deal(self, number_of_players, number_of_cards):
		''' 
		method to handle the deal operation. At the beginning of each hand each player is dealt a hand of cards to play with. 
		''' 

		if self.cards_remaining <= number_of_players * number_of_cards:
			self.generate()


		hands = [[self.cards.pop(random.randint(1, len(self.cards) - 1)) for i in range(number_of_cards)] for j in range(number_of_players)]
		self.cards_remaining = len(self.cards)

		return hands



	def dealback(self, cards_to_be_exchanged):
		''' 
		the dealback is a crucial part of the game 22. Before a hand starts players have the chance to exchange cards they don't like to try to improve their hand.
		dealbacks are limited to cards remaining in the deck. If a player requests 5 but there are only 4 cards left, they will get 4 cards. 
		If this is the case, cards_to_be_exchanged is a list of cards sorted by how much the agent wants to keep them. The bottom n cards will be replaced. 
		if there are no cards left in the deck, a player cannot perform a dealback and the same cards they want to exchange are returned to them. 
		'''

		if self.cards_remaining == 0:
			return cards_to_be_exchanged
		
		elif self.cards_remaining < len(cards_to_be_exchanged):
			for _ in range(self.cards):
				cards_to_be_exchanged.pop()

			for each in self.cards:
				cards_to_be_exchanged.append(each)

			return cards_to_be_exchanged

		else:
			return [self.cards.pop(random.randint(1, len(self.cards) - 1)) for i in range(len(cards_to_be_exchanged))]





class Card:
	''' 
	This is a class to handle all of the card 
	'''

	def __init__(self, face, value, score_value, deal_2, deal_3, deal_4, ind):

		self.face = face
		self.value = value
		self.score_value = score_value
		self.deal_2 = deal_2
		self.deal_3 = deal_3
		self.deal_4 = deal_4
		self.ind = ind


	def to_deal(self, n_players):
		''' 
		get how many cards to deal on the next round
		'''

		if n_players == 2:
			return self.deal_2
		elif n_players == 3:
			return self.deal_3
		elif n_players == 4:
			return self.deal_4





	