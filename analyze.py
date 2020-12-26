import matplotlib.pyplot as plt 
import csv
from typing import List





def visualize_decision_matrix(filename, n_players, n_games):
	'''
	create heat map to visualize the decision matrix value assessment.
	'''

	# get limits for the areas in the decision matrix that correspond to the play 
	one = {'col_start': 0, 'col_end': 13, 'row_start': 1, 'row_end': 14}
	two = {'col_start': 14, 'col_end': 183, 'row_start': 15, 'row_end': 184}
	three = {'col_start': 184, 'col_end': 2379, 'row_start': 185, 'row_end': 2380} 

	one_card_subset = []
	two_card_subset = []
	three_card_subset = []

	with open(filename, 'r', newline='') as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)

		# row = next(csv_reader)
		# print(type(row[0][0]))

		for index, row in enumerate(csv_reader):
			if one['row_start'] <= index <= one['row_end']:
				one_card_subset.append(row[one['col_start']:one['col_end']])
			if two['row_start'] <= index <= two['row_end']:
				two_card_subset.append(row[two['col_start']:two['col_end']])
			if three['row_start'] <= index <= three['row_end']:	
				three_card_subset.append(row[three['col_start']:three['col_end']])

	# for plotting purposes
	faces = ["2", "3", "4", "5", "6", "7", "8", "9", "10","J", "Q", "K", "A"]

	# plot the heat map for 1 card plays
	plt.imshow(one_card_subset)
	plt.title("Single Card Plays: \n" + str(n_players) + " Players")
	plt.xlabel("My move")
	plt.ylabel("Their move")
	plt.xticks([i for i in range(13)], faces)
	plt.yticks([i for i in range(13)], faces)
	plt.savefig('figures/dm_' + str(n_players) + 'p_1c_' + str(n_games) + '.png')
	plt.clf()

	# plot the heat map for 2 card plays
	plt.imshow(two_card_subset)
	plt.title("Two Card Plays: \n" + str(n_players) + " Players")
	plt.xlabel("My move")
	plt.ylabel("Their move")
	plt.xticks([i * 13 for i in range(13)], faces)
	plt.yticks([i * 13 for i in range(13)], faces)
	plt.savefig('figures/dm_' + str(n_players) + 'p_2c_' + str(n_games) + '.png')
	plt.clf()

	# plot the heat map for 3 card plays
	plt.imshow(three_card_subset)
	plt.title("Three Card Plays: \n" + str(n_players) + " Players")
	plt.xlabel("My move")
	plt.ylabel("Their move")
	plt.xticks([i * 169 for i in range(13)], faces)
	plt.yticks([i * 169 for i in range(13)], faces)
	plt.savefig('figures/dm_' + str(n_players) + 'p_3c_' + str(n_games) + '.png')
	plt.clf()

	return


def get_avg(data):
	'''
	function to get average of a list
	'''

	return sum(data) / len(data)



def plot_learning_curve(filename, n_players, n_games):
	''' 
	function to plot the learning curve of the agent 
	'''

	iters = []
	success_rates = []

	file = open(filename, 'r')
	for line in file:
		iters.append(int(line.split(" ")[0]))
		success_rates.append(float(line.split(" ")[1]) / ((n_players - 1) / n_players))

	avg_success_rate = get_avg(success_rates)

	moving_avg_success_rates = []

	for i in range(len(success_rates)):
		if i == 0:
			moving_avg_success_rates.append(success_rates[0])
		elif i < 5:
			moving_avg_success_rates.append(get_avg(success_rates[0:i]))
		else:
			moving_avg_success_rates.append(get_avg(success_rates[i - 5:i + 1]))



	plt.plot(iters, success_rates, c="b", lw="0.75", label="Success Rate")
	plt.plot(iters, moving_avg_success_rates, c="r", label="5-Corpus Moving Average")
	plt.plot([iters[0], iters[-1]], [1, 1], c="k", ls="dashed", label="Minimum Success Rate")
	plt.plot([iters[0], iters[-1]], [avg_success_rate, avg_success_rate], c="g", label="Average Success Rate")
	plt.title(str(n_players) + " Players: Learning Curve \n" + str(n_games) + " Games")
	plt.legend(loc="upper right")
	plt.ylabel("Success Rate")
	plt.xlabel("Training Games Played")
	plt.tight_layout()
	# plt.show()
	plt.savefig('figures/lc_' + str(n_players) + 'p_' + str(n_games) + '.png')
	plt.clf()


def combined_decision_matrix(filenames: List, n_games):
	''' 
	function to present multiple decision matrix visualizations on the same line. 

	params: 
		filenames:  list of file names that contain the decision matrices of the agents, sorted by number of players in ascending order: 2, 3, 4. 
		n_games: 	int representing the number of trained self-play games that an agent trained over
	'''

	# get limits for the areas in the decision matrix that correspond to the play 
	limits = [{'col_start': 0, 'col_end': 13, 'row_start': 1, 'row_end': 13}, 
	{'col_start': 14, 'col_end': 183, 'row_start': 15, 'row_end': 184}, 
	{'col_start': 184, 'col_end': 2379, 'row_start': 185, 'row_end': 2380}]

	# for plotting purposes
	faces = ["2", "3", "4", "5", "6", "7", "8", "9", "10","J", "Q", "K", "A"]

	# map j to number of players
	players = ['Two Players', 'Three Players', 'Four Players']

	# map i to number of cards
	cards = ['One Card', 'Two Cards', 'Three Cards']

	for i in range(len(limits)):
		for j, filename in enumerate(filenames):
			card_subset = []

			with open(filename, 'r', newline='') as csvfile:
				csv_reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)

				for index, row in enumerate(csv_reader):
					if limits[i]['row_start'] <= index <= limits[i]['row_end']:
						card_subset.append(row[limits[i]['col_start']: limits[i]['col_end']])

			# plot the heat map for 1 card plays
			plt.subplot(1, 3, j + 1)
			plt.imshow(card_subset)
			plt.title(str(players[j]))
			plt.xlabel("My move")
			plt.xticks([k * 13 ** i for k in range(13)], faces)
			if j == 0:
				plt.ylabel("Their move")
				plt.yticks([k * 13 ** i for k in range(13)], faces)
			else:
				plt.yticks([], [])

		# plt.suptitle(str(cards[i]) + ", " + str(n_games) + " Games, Self-play")
		# plt.subplots_adjust(top=1.5)
		# plt.figure(figsize=(5, 2.5))
		plt.tight_layout()
		plt.savefig('figures/combined_dm_' + str(i + 1) + 'c_' + str(n_games) + '.png')
		plt.clf()
		# plt.show()






if __name__ == '__main__':
	# 3-player games 
	# visualize_decision_matrix('matrices/3p_games.csv', 3, 1000000)
	plot_learning_curve('logs/3p_games.txt', 3, 1000000)

	# 4-player games
	# visualize_decision_matrix('matrices/4p_games.csv', 4, 1000000)
	# plot_learning_curve('logs/4p_games.txt', 4, 1000000)

	# 2-player games
	# visualize_decision_matrix('matrices/2p_games.csv', 2, 1000000)
	# plot_learning_curve('logs/2p_games.txt', 2, 1000000)

	# generate combined decision matrix graphic
	# combined_decision_matrix(['matrices/2p_games.csv', 'matrices/3p_games.csv', 'matrices/4p_games.csv'], 1000000)
	# combined_decision_matrix(['matrices/2p_games.csv'], 1000000)






