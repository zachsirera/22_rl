import random
from collections import Counter
from itertools import combinations

class Player:
	''' 
	this is a class to handle all of the instance variables for a player
	'''

	def __init__(self, index, random_play=False):
		self.score = 0
		self.hand = []
		self.index = index
		self.games_played = 0
		self.losses = 0
		self.decision_matrix = self.initialize_decision_matrix()
		self.random_play = random_play



	def set_hand(self, hand):
		''' 
		setter method for the agent's hand
		'''
		self.hand = sorted(hand, key=lambda x: x.value, reverse=False)
		return 



	def lead(self): 
		''' 
		method to call the agent's lead play based on its decision matrix
		''' 
		# get the row index which describes the state the agent finds itself in
		row_ind = self.decision_map_row(lead=True)

		# don't let the agent lead all of their cards or 4 of a kind
		max_play = min(3, len(self.hand) - 1)

		# group the hand by multiple cards
		grouped_hand = dict(Counter(getattr(card, 'ind') for card in self.hand))

		# initialize vals and iterate through groups and get the value of each play. 
		vals = []
		for card in grouped_hand:
			# need to check not only the value of playing a pair, but also playing a single when they have two of the same cards, two when three, etc
			for i in range(grouped_hand[card]):
				if i < (max_play):
					play = [card] * (i + 1)
					col_ind = self.decision_map_col(play)
					vals.append({'play': play, 'value': self.decision_matrix[row_ind][col_ind]})

		# call the pick function to pick the play based on the values in the decision matrix
		chosen_play = self.pick(vals)

		# here is where it gets a little nasty... taking the play choice and reconstructing it as a list of Card objects and removing that from the hand
		count = len(chosen_play['play'])
		all_play = [chosen_play['play'][0] for i in range(count)]

		# get the indices of cards in the hand that correspond to the chosen play and 
		# card_inds = sorted([i for i, x in enumerate(self.hand) if x.ind == all_play[0]], reverse=True)
		card_inds = []
		for i, x in enumerate(self.hand):
			if x.ind == all_play[0]:
				card_inds.append(i)
			if len(card_inds) == len(all_play):
				break

		card_inds.sort(reverse = True)

		play = [self.hand[i] for i in card_inds]

		for i in card_inds:
			del self.hand[i]

		return play

		

	def play(self, current_play): 
		''' 
		method to call the agent's play as a response to the current play based on its understanding of the current landscape
		'''

		# get the row index which describes the state the agent finds it self in
		row_ind = self.decision_map_row(current_play=[x.ind for x in current_play])

		# get all options
		all_options = list(combinations(self.hand, len(current_play)))

		# playing under is always a valid option. If an agent has no cards to beat the current play, that is its only option. 
		# however, an agent might want to strategically play under. this preserves that option in all states. 
		valid_options = [[self.hand[i] for i in range(len(current_play))]]

		# iterate across all options and validates them.
		for option in all_options:
			score = 0
			for index, card in enumerate(option):
				if card.ind < current_play[index].ind:
					score += 1
			if score == 0:
				valid_options.append(option)

		# get the value of all valid options
		vals = [0 for _ in valid_options]
		for index, option in enumerate(valid_options):
			play = [x.ind for x in option]
			col_ind = self.decision_map_col(play)
			vals[index] = {'play': play, 'value': self.decision_matrix[row_ind][col_ind]}

		# call the pick function to pick the play based on the values in the decision matrix
		chosen_play = self.pick(vals)

		# here is where it gets a little nasty... taking the play choice and reconstructing it as a list of Card objects and removing that from the hand
		card_inds = []
		
		for i, x in enumerate(self.hand):
			for card in chosen_play['play']:
				if card == x.ind:
					card_inds.append(i)
					break
			if len(card_inds) == len(current_play):
				break

		card_inds.sort(reverse = True) 
		play = sorted([self.hand[i] for i in card_inds], key=lambda x:x.ind)

		for i in card_inds:
			del self.hand[i]

		return play


			
	def decision_map_row(self, current_play=None, lead=False):
		'''
		method to get the row index of the decision matrix based on the current state.
		current_play is list of Card.ind values
		''' 

		# the lead is at the first row of the decision matrix 
		if lead:
			return 0

		# the play section is the remaining rows
		else:
			if not current_play:
				raise ValueError('Need current_play')
			else:
				if len(current_play) == 1:
					return 1 + current_play[0]
				elif len(current_play) == 2:
					return 1 + 13 + current_play[0] + 13 * current_play[1]
				else:
					return 1 + 13 + 169 + current_play[0] + 13 * current_play[1] + 169 * current_play[2]
				


	def decision_map_col(self, possible_play):
		'''
		method to get the column index of the decision matrix that represents a potential action based on the agents cards. 
		'''

		if len(possible_play) == 1:
			return possible_play[0]
		elif len(possible_play) == 2:
			return 13 + possible_play[0] + 13 * possible_play[1]
		else:
			return 13 + 169 + possible_play[0] + 13 * possible_play[1] + 169 * possible_play[2]



	def initialize_decision_matrix(self):
		'''
		method to initialize the decision matrix that the agent will use to learn the value of each play and then make decisions

		Matrix structure: each row represents a state in the game, defined by the current play or whether the player has the lead. 
		Each column represents a possible action at that state. 
		'''

		n_plays = 13 + (13 ** 2) + (13 ** 3)

		n_rows = n_plays + 1
		n_cols = n_plays

		return [[0 for _ in range(n_cols)] for _ in range(n_rows)]



	def pick(self, vals):
		''' 
		method to randomly pick the play based on the value of all of the plays based on an algorithm similar to simmulated annealing
		'''

		# right now it just randomly picks from those plays who have the max value
		if self.random_play == True:
			# if an agent is playing randomly, just pick at random from the valid plays 
			plays = vals
		else:
			# if an agent is playing 'intelligenty', apply a more sophisticated choise algorithm
			# right now it picks the max value, but I will incorporate something resembling simmulated annealing so that agents can 
			# explore the entire state space
			plays = [x for x in vals if x['value'] == max(vals, key=lambda x:x['value'])['value']]


		return random.choice(plays)



	def add_score(self, value):
		'''
		setter method for accumulating points
		'''

		self.score += value
		return



	def add_game(self):
		'''
		setter method for game count
		'''

		self.games_played += 1



	def add_loss(self):
		'''
		setter method for loss
		'''

		self.losses += 1

