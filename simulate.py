# import the classes from the project directory
from classes.game import Game
from classes.player import Player
from classes.round import Round

# import the external libraries required
import csv



def write_log(filename, data):
	''' 
	write results to a log file. data is a tuple for each line of the log file representing the number of iterations and the non_loss_pct
	'''

	log = open(filename, 'a')
	log.write(str(data[0]) + " " + str(data[1]) + '\n')
	log.close()

	return



def write_matrix(filename, decision_matrix):
	''' 
	write the current decision matrix to the disk to preserve information if the script gets interrupted and to aid in analysis when finished. 
	'''

	with open(filename, 'w', newline='') as csvfile:
		csv_writer = csv.writer(csvfile, delimiter=',')

		for row in decision_matrix:
			csv_writer.writerow(row)

	return



def game_exp(n_players, log_filename, matrix_filename):
	''' 
	run any experiment that involves learning based on game outcomes only 
	''' 

	# all games start with 7 cards
	n_cards = 7

	learners = [Player(j, random_play=False) for j in range(n_players)]
	rand_players = [learners[0]] + [Player(1, random_play=True) for j in range(n_players - 1)]

	# run 1,000,000 games but stop every 10,000 to check the agent's win percentage against a random agent.
	for k in range(100):

		# play 10000 games
		for i in range(10000): 
			game = Game(learners, n_cards)
			game.play()

		# reset counters to get non_loss_pct
		learners[0].games_played, learners[0].losses = 0, 0

		# stop and play 100 games against 
		for i in range(100): 
			game = Game(rand_players, n_cards)
			game.play()

		# record performance before proceeding 
		non_loss_pct = round(1 - learners[0].losses / learners[0].games_played, 4)
		write_log(log_filename, ((k + 1) * 10000, non_loss_pct))

		# write decision matrix to disk before proceeding
		write_matrix(matrix_filename, learners[0].decision_matrix)

	return




if __name__ == '__main__':

	# experiment 1: three players, learn based on game outcomes only
	game_exp(3, 'logs/3p_games.txt', 'matrices/3p_games.csv')

	# # experiment 2: two players, learn based on game outcomes only
	# game_exp(2, 'logs/2p_games.txt', 'matrices/2p_games.csv')

	# # experiment 3: four players, learn based on game outcomes only
	# game_exp(4, 'logs/4p_games.txt', 'matrices/4p_games.csv')











		