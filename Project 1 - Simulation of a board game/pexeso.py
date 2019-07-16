# -*- coding: UTF-8 -*-
"""FI MUNI Brno - IB111: Basics of Programming, Advanced Group
-Project 1: Simulation of various strategies in a simple board game.
Autor: Miroslav Bezák, 485221
"""

import matplotlib.pyplot as plt

from classes import PexesoGame

# MAX_GRID_SIZE = int(input("Enter Max Grid Size:"))
MAX_GRID_SIZE = 8


def play_games(max_grid_size):
    """Runs the simulation on different grid sizes starting from 4x4 up to
    max_grid_size by max_grid_size."""
    games = []
    for size in range(4, max_grid_size + 1, 2):
        games.append(PexesoGame(size, size))
    return games


def define_line_colors():
    """Define the line colors list for different colors of the lines in the
    graph."""
    line_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for color, _ in enumerate(line_colors):
        line_colors[color] += "o-"

    return line_colors


def handle_player_strategies(games):
    """Handle the strategies of the players and puts them into one list."""
    player_strategies = []
    for player in games[0].players:
        player_strategies.append(
            player.strategy + " " + player.buffer_type + " " + str(
                player.buffer_length))
    return player_strategies


def handle_player_results(games, line_colors, player_strategies):
    """Handle the player results and put them into a MyPlotLib plot."""
    player_results = []
    for _ in games[0].players:
        player_results.append([])

    for game in games:
        players_with_wins = {""}
        all_players = {""}
        for player_id in range(len(game.players)):
            all_players.add(player_id)
        for j in range(len(game.results_tuples)):
            players_with_wins.add(game.results_tuples[j][0])
        all_players.remove("")
        players_with_wins.remove("")
        without_wins = all_players - players_with_wins
        for player_id in without_wins:
            game.results_tuples.insert(player_id, (0, 0))

        for player_id in range(len(game.players)):
            player_results[player_id].append(game.results_tuples[player_id][1])

    for player_id, _ in enumerate(player_results):
        plt.plot(range(4, MAX_GRID_SIZE + 1, 2), player_results[player_id],
                 line_colors[player_id], label=player_strategies[player_id])


def plot():
    """Display the plot."""
    plt.xlabel("Grid Size")
    plt.ylabel("Games Won")
    plt.legend(loc='best')
    plt.show()


GAMES = play_games(MAX_GRID_SIZE)
PLAYER_STRATEGIES = handle_player_strategies(GAMES)
handle_player_results(GAMES, define_line_colors(), PLAYER_STRATEGIES)
plot()
