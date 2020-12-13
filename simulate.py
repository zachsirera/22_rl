from classes.game import Game
from classes.player import Player

import matplotlib.pyplot as plt

if __name__ == '__main__':

	n_cards = 7
	n_players = 2

	print("Training: ", n_players, " players")
	
	players = [Player(j, random_play=False) for j in range(n_players)]

	for i in range(10000): # play 100 games
		game = Game(players, n_cards)
		game.play()

	print(str(n_players) + " players win percentage: ", [round(x.losses / x.games_played, 4) for x in players])

	faces = ["2", "3", "4", "5", "6", "7", "8", "9", "10","J", "Q", "K", "A"]

	one_card_subset = [row[0:13] for row in players[0].decision_matrix[1:14]]
	two_card_subset = [row[14:183] for row in players[0].decision_matrix[15:184]]
	three_card_subset = [row[184:2379] for row in players[0].decision_matrix[185:2380]]

	plt.imshow(one_card_subset)
	plt.title("Single Card Plays")
	plt.xlabel("My move")
	plt.ylabel("Their move")
	plt.xticks([i for i in range(13)], faces)
	plt.yticks([i for i in range(13)], faces)
	plt.savefig('figures/single_card_10000.png')
	plt.clf()

	plt.imshow(two_card_subset)
	plt.title("Two Card Plays")
	plt.xlabel("My move")
	plt.ylabel("Their move")
	plt.xticks([i * 13 for i in range(13)], faces)
	plt.yticks([i * 13 for i in range(13)], faces)
	plt.savefig('figures/two_card_10000.png')
	plt.clf()

	plt.imshow(three_card_subset)
	plt.title("Three Card Plays")
	plt.xlabel("My move")
	plt.ylabel("Their move")
	plt.xticks([i * 169 for i in range(13)], faces)
	plt.yticks([i * 169 for i in range(13)], faces)
	plt.savefig('figures/three_card_10000.png')
	plt.clf()
	
	print("Trained Agent aganst a random player")

	players[0].games_played = 0
	players[0].losses = 0

	new_players = [players[0], Player(1, random_play=True)]

	for i in range(100):
		game = Game(new_players, n_cards)
		game.play()

	print(str(n_players) + " players win percentage: ", [round(x.losses / x.games_played, 4) for x in new_players])





		