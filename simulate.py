from classes.game import Game
from classes.player import Player

if __name__ == '__main__':

	n_players = 4
	n_cards = 7

	players = [Player(i) for i in range(n_players)]

	for i in range(1000):
		game = Game(players, n_cards)
		game.play()
		

	print("win percentage: ", [round(x.losses / x.games_played, 4) for x in players])
	
		

	pass






		