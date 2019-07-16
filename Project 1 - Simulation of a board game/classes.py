# -*- coding: UTF-8 -*-
"""FI MUNI Brno - IB111: Basics of Programming, Advanced Group
-Project 1: Simulation of various strategies in a simple board game."""

import random
import math


class PexesoGame:
    """Main control class of the game."""

    def __init__(self, width=20, height=20, games_count=2000):
        """Only initializes the needed parameters of the class,
        creates card pairs."""
        self.players = []
        self.width = width
        self.height = height
        # board is a 2d array - board[][]
        self.board = [["null" for _ in range(self.width)]
                      for _ in range(self.height)]
        self.cards_amount = self.width * self.height
        self.pairs_left = self.cards_amount // 2
        self.cards = []
        # Here you choose the strategies for the game - "random", "infinite"
        # or "finite <buffer_type> <buffer_length>"
        # self.strategies = ["random", "infinite", "finite stack 15",
        #                    "finite queue 10"]
        self.strategies = ["finite stack 10", "finite queue 10"]
        self.games_count = games_count

        self.results = []
        self.results_tuples = []
        self.scores = []
        self.on_move = 0

        self.create_board()
        self.multiplayer(len(self.strategies))

    def create_board(self):
        """Creates the game board, placing the cards randomly."""
        self.cards = []
        for i in range(self.cards_amount // 2):
            self.cards.append(str(i + 1))
            self.cards.append(str(i + 1))
        for row in range(self.height):
            for col in range(self.width):
                selected_card = random.randrange(len(self.cards))
                self.board[row][col] = self.cards[selected_card]
                self.cards.pop(selected_card)

    def add_players(self, player_count):
        """Create a new player with a random strategy."""

        for plr_id in range(player_count):
            if self.strategies[plr_id][:6] == "finite":
                strategy_split = self.strategies[plr_id].split(" ")
                self.players.append(Player(self, "finite", plr_id,
                                           int(strategy_split[2]),
                                           strategy_split[1]))
            else:
                self.players.append(Player(self, self.strategies[plr_id],
                                           plr_id))

    def multiplayer(self, player_count):
        """Starts a series of games between between given
        amount of opponents."""

        print("\nStarting game:", self.width, "x", self.height)

        self.add_players(player_count)

        for _ in range(self.games_count):
            while self.pairs_left > 0:
                self.players[self.on_move].general_move()

            winners = []
            high_score = 0
            for player in self.players:
                high_score = player.score if player.score >= high_score \
                    else high_score
            for player in self.players:
                if player.score == high_score:
                    winners.append(player)

            for winner in winners:
                self.results.append({winner.id: winner.moves_count})
                self.scores.append({winner.id: winner.score})
            # self.switch_player()
            self.on_move = 0
            self.game_reset()

        self.output_results()

    def print_header(self):
        """Print the beginning of the output, basic info about players,
        scores and strategies."""

        print("Results: {winner: moves count}")
        print(self.results)
        print("Scores: {winner: amount of pairs collected}")
        print(self.scores)
        print("Strategies:")
        print("| ", end="")
        for player in self.players:
            print(player.strategy, player.buffer_type, player.buffer_length,
                  end=" | ")
        print("\n", end="")

    def get_result_moves_data(self, results_data, moves_data):
        """Fill the given `results_data` and `moves_data` dictionaries with
        information about results and moves."""

        for result in self.results:
            if list(result.keys())[0] in results_data.keys():
                results_data[list(result.keys())[0]] += 1
                moves_data[list(result.keys())[0]] += list(result.values())[0]
            else:
                results_data[list(result.keys())[0]] = 1
                moves_data[list(result.keys())[0]] = list(result.values())[0]

    def print_win_counts(self, results_data):
        """Print information about how many games have all the players won.
        Also fill the `result_tuples` dictionary need for the main programme."""
        print("Wins counts:")
        print("| ", end="")
        self.results_tuples = [(k, v) for k, v in results_data.items()]
        self.results_tuples = sorted(self.results_tuples, key=lambda x: x[0])
        for result in self.results_tuples:
            print(result[1], end=" | ")
        print("\n", end="")

    @staticmethod
    def print_avg_moves(results_data, moves_data):
        """Print information about average move counts for all players."""
        print("Average moves counts per won game:")
        for key in moves_data:
            moves_data[key] /= results_data[key]
            moves_data[key] = round(moves_data[key], 3)
        print("| ", end="")
        moves_tuples = [(k, v) for k, v in moves_data.items()]
        moves_tuples = sorted(moves_tuples, key=lambda x: x[0])
        for result in moves_tuples:
            print(result[1], end=" | ")
        print("\n", end="")

    def output_results(self):
        """Outputs the information about the result of the game
        into the console."""
        self.print_header()

        results_data = {}
        moves_data = {}
        self.get_result_moves_data(results_data, moves_data)

        self.print_win_counts(results_data)

        self.print_avg_moves(results_data, moves_data)

    def switch_player(self):
        """Switches to the next player in the players array."""
        if self.on_move == len(self.players) - 1:
            self.on_move = 0
        else:
            self.on_move += 1

    def game_reset(self):
        """Resets the game and the players' stats."""
        for player in self.players:
            player.moves_count = 0
            player.score = 0
        self.create_board()
        self.pairs_left = self.cards_amount // 2


class Player:
    """Class for controlling the individual player, their actions and scores."""

    def __init__(self, game_obj, strategy, my_id, buf_len=None, buf_type=None):
        self.game = game_obj
        self.strategy = strategy
        self.id = my_id
        if buf_len:
            self.buffer_length = buf_len
        else:
            self.buffer_length = math.inf
        if buf_type:
            self.buffer_type = buf_type
        else:
            self.buffer_type = ""

        self.score = 0
        self.moves_count = 0
        self.buffer = {}

    def general_move(self):
        """Carry out 1 move according to one of the predefined strategies."""
        if self.strategy == "random":
            self.random_move()

        elif self.strategy == "infinite" or self.strategy == "finite":
            self.finite_infinite_move()

    def pick_random_card(self, card_1=None):
        """Pick a random card from the deck and return it."""
        card = [random.randrange(self.game.width),
                random.randrange(self.game.height)]
        while self.game.board[card[0]][
            card[1]] == "null" or card_1 == card:
            card = [random.randrange(self.game.width),
                    random.randrange(self.game.height)]

        return card

    def add_card_to_inf_buffer(self, card_1):
        """Remember what card was turned on the table for other players."""
        for player in self.game.players:
            if player.strategy == "infinite":
                # Add card to buffer
                if self.game.board[card_1[0]][card_1[1]] not in player.buffer:
                    player.buffer[self.game.board[card_1[0]][card_1[1]]] = []
                player.buffer[self.game.board[card_1[0]][card_1[1]]].append(
                    card_1)

    def random_move(self):
        """Simulate one move in the random strategy,
        both cards are picked randomly."""

        card_1 = self.pick_random_card()
        self.add_card_to_inf_buffer(card_1)

        card_2 = self.pick_random_card(card_1)
        self.moves_count += 1

        if self.game.board[card_1[0]][card_1[1]] == self.game.board[card_2[0]][
            card_2[1]]:
            self.score += 1
            self.game.board[card_1[0]][card_1[1]] = "null"
            self.game.board[card_2[0]][card_2[1]] = "null"
            self.game.pairs_left -= 1
        else:
            self.save_for_others(card_1, card_2)
            self.game.switch_player()

    def buffer_full_handle(self):
        """Remove the first or last entry of the buffer according to its
        type."""
        if self.buffer_type == "stack":
            # Stack is Last In, First Out
            del self.buffer[list(self.buffer.keys())[-1]]
        elif self.buffer_type == "queue":
            # Queue is First In, First Out
            del self.buffer[list(self.buffer.keys())[0]]

    def add_to_buffer(self, card_1):
        """Add the new card into buffer."""
        if self.game.board[card_1[0]][card_1[1]] not in self.buffer:
            self.buffer[self.game.board[card_1[0]][card_1[1]]] = []
        self.buffer[self.game.board[card_1[0]][card_1[1]]].append(card_1)

    def found_pair(self, card_1, card_2):
        """Handle the event of found pair on the board."""
        self.score += 1
        del self.buffer[self.game.board[card_1[0]][card_1[1]]]
        self.game.board[card_1[0]][card_1[1]] = "null"
        self.game.board[card_2[0]][card_2[1]] = "null"
        self.game.pairs_left -= 1

    def finite_infinite_move(self):
        """Simulate one move in the strategy with limited or unlimited buffer,
        the memory is used to find the second card of the pair."""
        card_1 = self.pick_random_card()
        self.moves_count += 1

        # Save card into the buffer
        if self.game.board[card_1[0]][card_1[1]] not in self.buffer.keys():
            if len(self.buffer) >= self.buffer_length:
                self.buffer_full_handle()

            self.add_to_buffer(card_1)
            card_2 = self.pick_random_card(card_1)
            self.save_for_others(card_1, card_2)

            if self.game.board[card_1[0]][card_1[1]] == \
                    self.game.board[card_2[0]][card_2[1]]:
                self.found_pair(card_1, card_2)
            else:
                self.game.switch_player()

        # The position of the pair is already known
        else:
            card_2 = self.buffer[self.game.board[card_1[0]][card_1[1]]][0]
            self.found_pair(card_1, card_2)

    @staticmethod
    def card_insert_into_buffer(card_id, card, player):
        """Inserts the card into player's buffer."""
        if player.game.board[card[card_id][0]][card[card_id][1]] \
                not in player.buffer.keys():
            # Buffer full
            if not len(player.buffer) < player.buffer_length:
                if player.buffer_type == "stack":
                    # Stack is Last In, First Out
                    del player.buffer[list(player.buffer.keys())[-1]]
                elif player.buffer_type == "queue":
                    # Queue is First In, First Out
                    del player.buffer[list(player.buffer.keys())[0]]

            # Space in the buffer
            if player.game.board[card[card_id][0]][card[card_id][1]] \
                    not in player.buffer:
                player.buffer[
                    player.game.board[card[card_id][0]][card[card_id][1]]] = []
            player.buffer[
                player.game.board[card[card_id][0]][card[card_id][1]]].append(
                card[card_id])

    def save_for_others(self, card_1, card_2):
        """Save the showed cards into buffers of other players."""
        cards = [card_1, card_2]
        for card_id, _ in enumerate(cards):
            for player in self.game.players:
                if player is not self and player.strategy != "random":
                    self.card_insert_into_buffer(card_id, cards, player)
