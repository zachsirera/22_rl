from .round import Round
from .deck import Deck
from .player import Player


class Game:
	''' 
	this class handles each game of 22. A game of 22 is just n repeated rounds until one player amasses a score 22 or greater. 
	'''

	def __init__(self, players, n_cards):
		'''
		
		'''
		self.deck = Deck()
		self.players = players
		self.n_players = len(self.players)
		self.n_cards = n_cards
		self.loser = None
		self.leader = 0


	def play(self):
		'''
		play a game. 
		'''


		while not self.end_game():
			leader, n_cards = self.play_round(self.leader)
			self.leader = leader
			self.n_cards = n_cards

		self.assign_loss()
		self.reset_game()
		
			


	def end_game(self):
		''' 
		check if a player has ammassed a score of 22 or greater. returns the index of the losing player or returns False to continue game 
		'''

		count = 0
		for index, player in enumerate(self.players):
			if player.score >= 22:
				count += 1

		return count != 0




	def play_round(self, leader):
		''' 
		play a round 
		'''

		# deal hands
		hands = self.deck.deal(self.n_players, self.n_cards)
		for i, hand in enumerate(hands):
			self.players[i].set_hand(hand)

		# play the round
		r = Round(self.players)
		last_cards = r.play()

		# determine the loser(s), administer points
		losing_card = max(last_cards, key=lambda x:x.value)
		round_loser = [i for i, x in enumerate(last_cards) if x.value == losing_card.value]
		for i in round_loser:
			self.players[i].add_score(losing_card.score_value // len(round_loser))

		# get next leader and number of cards to deal for next round
		if round_loser[0] == 0:
			return self.n_players - 1, losing_card.to_deal(self.n_players)
		else:
			return round_loser[0] - 1, losing_card.to_deal(self.n_players)


	def assign_loss(self):
		''' 
		after a loss, assign loss to a player
		'''

		for player in self.players:
			if player.score >= 22:
				player.add_loss()



	def reset_game(self):
		'''
		after the game ends, reset the 
		'''
		for player in self.players:
			player.add_game()
			player.score = 0



