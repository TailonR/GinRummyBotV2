from node import Node
from state import State
# Comparing MCTS vs Minimax when playing Rummy
import random
import copy
from pile import Pile
from game import Game
from player import Player

"""############## Main for the MCTS ######################"""
random.seed(4)
game1 = Game()
game1.setup()
winner = game1.game_loop()


# def mock_game_setup(hand_p1, hand_p2, game, discard_pile_size):
#     mock_players = [Player() for _ in range(2)]
#     mock_players[0].create_hand(hand_p1)
#     mock_players[1].create_hand(hand_p2)
#     game.set_players(mock_players)
#     game.create_stock_pile()
#     for i in range(discard_pile_size):
#         game.discard_pile.add_to_pile(game.stock_pile.get_top_card())
#     # initial_state = State(game.get_game_state(), True)
#     game.create_game_ai(Node(game.get_game_state(), 0, True))
#
#
# mock_hand_p1 = [[0, 1], [1, 1], [2, 1], [3, 1], [0, 2], [1, 3], [2, 4]]
# mock_hand_p2 = [[0, 4], [0, 5], [0, 6], [3, 3], [0, 7], [2, 3], [1, 4]]
# random.seed(5)
# game = Game()
# pile_size_discard = 18
# mock_game_setup(mock_hand_p1, mock_hand_p2, game, pile_size_discard)
# game.game_loop()

# The following player's hand is a 4x13 matrix
# The following matrix shows that p1 has the hand [0, 0], [1, 0], [2, 0], [3, 0], [0, 1], [1, 2], [2, 3]
#   as well as the card to be considered [3, 4]
# Might just need to subtract 1 to the rank the user enters to make sure the index into the matrix is correct
#                  A    2    3    4    5    6    7    8    9   10    J    Q    K
# player1_hand = [[1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # H
#                 [1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # S
#                 [1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # C
#                 [1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]  # D
#
# expected_evaluation = [[100500.0, 500.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#                        [100000.0,   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#                        [100000.0,   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#                        [100000.0,   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
#
# testing = NeuralNetwork(player1_hand, expected_evaluation)
# testing.test()
