from classes.game import Game
from classes.player import Player

import matplotlib.pyplot as plt

if __name__ == '__main__':

	n_cards = 7
	n_players = 2

	# going to run 1,000,000 games but stop every 10,000 to check the agent's win percentage against a random agent.
	for k in range(100):
		
		players = [Player(j, random_play=False) for j in range(n_players)]

		for i in range(10000): # play 100 games
			game = Game(players, n_cards)
			game.play()
		


		players[0].games_played, players[0].losses = 0, 0

		new_players = [players[0], Player(1, random_play=True)]

		for i in range(100):
			game = Game(new_players, n_cards)
			game.play()

		log = open('log_2.txt', 'a')
		log.write(str((k + 1) * 10000) + " " + str(round(1 - players[0].losses / players[0].games_played, 4)) + "\n")
		log.close()
 




		