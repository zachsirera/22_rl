class Round:
	''' 
	this is a class to implement the basic structure of a "round". A round is more commonly known as a "hand" but I wanted to avoid the confusion 
	of referring to it as the same thing as a player's hand, ie a collection of cards
	'''

	def __init__(self, players, next_leader = None):
		self.players = players
		self.cards_left = len(players[0].hand)
		self.next_leader = 0



	def play(self):
		'''
		method to play a round. 
		at the begining of a game, the leader is player_1 (0). however, in each subsequent round the leader is the player who played the last 'winning' 
		hand. hence the confustion around the way the indexing. you'll see. 
		'''

		
		while not self.end_round():

			# determine the playing order of the round. the round starts with the leader at position 0, but each successive hand starts with the previous hand's
			# winner. think of this like play clockwise from the winner each time. 
			order = [i for i in range(self.next_leader, len(self.players))] + [i for i in range(self.next_leader)]

			# get the lead
			current_play = self.get_lead(order[0])
			
			# and start playing
			for i in order[1:]:
				proposed_play = self.get_play(i, current_play)

				# check if each play beats the previous play, if so, it becomes the play to beat
				if self.check_if_beat(current_play, proposed_play):
					current_play = proposed_play
					self.next_leader = i

		# when agents are down to a single card, return the cards to determine who accumulates score, who deals the next hand, and how many cards to deal
		return [card for player in self.players for card in player.hand]
		
		

	def get_lead(self, leader):
		''' 
		The lead is the play that starts the round. The "leader" may choose how many cards to play and other players must follow suit. 

		In a round, one player "leads". The leader may choose to play 1 to 4 cards. If a player leads more than 1 card, 
		they must be of the same value.

		This function takes one argument, an int representing which player is leading. At the start of a game, the player after the loser gets to lead the opening round. 
		At the start of each successive round, the player who played the highest card or cards in the previous round gets to lead. 

		When called, this function returns a list containing the leader's lead.
		''' 

		return self.players[leader].lead()


	def get_play(self, player_i, current_play): 
		''' 
		after a lead, each other player in the game gets to play in response. a player must 
		'''

		return self.players[player_i].play(current_play)




	def check_if_beat(self, previous_play, current_play):
		'''
		determine if the current play beat the previous play on the table, if so it becomes the play to beat. The last person to play a 'winning' 
		play in a round leads the next round.

		to 'beat' the previous play an agent must play n cards that individually tie or beat the n cards in the previous play. 

		example: 

		previous_play = [4, 6]
		current_play which beats previous_play: [4, 6], [5, 6], [5, 10], etc. 
		current_play which doesn't beat previous_play: [2, 2] (agent playing their lowest cards)

		plays are sorted so this reduces the amount of comparisons needed to just n_cards

		'''
		count = 0
		for i, card in enumerate(current_play):
			if card.value < previous_play[i].value:
				count += 1

		return count == 0


	def end_round(self):
		''' 
		a round ends when all players have a single card left. 
		'''

		return len(self.players[0].hand) == 1



