"""
    >>> test_create_hand()
    Is player hand same as mock_hand? True

    >>> test_game_setup()
    Number of players: 2
    Player turn: 0
    Size of discard pile: 1
    Size of stock pile: 37

    >>> test_mock_game()
    Game player 1 has same hand as mock_player 1? True
    Game player 2 has same hand as mock_player 2? True
    Player turn: 0
    Size of discard pile: 18
    Size of stock pile: 20

    >>> test_mock_game_play()
"""
from player import Player
from game import Game
from state import State
from node import Node


def mock_game_setup(hand_p1, hand_p2, game, discard_pile_size):
    mock_players = [Player() for _ in range(2)]
    mock_players[0].create_hand(hand_p1)
    mock_players[1].create_hand(hand_p2)
    game.set_players(mock_players)
    game.create_stock_pile()
    for i in range(discard_pile_size):
        game.discard_pile.add_to_pile(game.stock_pile.get_top_card())
    # initial_state = State(game.get_game_state(), True)
    game.create_game_ai(Node(game.get_game_state(), 0, True))


def test_create_hand():
    mock_hand = [[0, 1], [1, 1], [2, 1], [3, 1], [0, 2], [0, 3], [0, 4]]
    player = Player()
    player.create_hand(mock_hand)
    print("Is player hand same as mock_hand?", mock_hand == player.get_hand())


def test_game_setup():
    game = Game()
    game.setup()
    game_state = game.get_game_state()
    the_players = game_state["players"]
    print("Number of players:", len(the_players))
    print("Player turn:", game_state["playerTurn"])
    print("Size of discard pile:", game_state["discardPile"].size())
    print("Size of stock pile:", game_state["stockPile"].size())


def test_mock_game():
    mock_hand_p1 = [[0, 1], [1, 1], [2, 1], [3, 1], [0, 2], [1, 3], [2, 4]]
    mock_hand_p2 = [[0, 4], [0, 5], [0, 6], [3, 3], [0, 7], [2, 3], [1, 4]]
    game = Game()
    pile_size_discard = 18
    mock_game_setup(mock_hand_p1, mock_hand_p2, game, pile_size_discard)
    mock_game_state = game.get_game_state()
    mock_players = mock_game_state["players"]
    print("Game player 1 has same hand as mock_player 1?", mock_players[0].get_hand() == mock_players[0].get_hand())
    print("Game player 2 has same hand as mock_player 2?", mock_players[1].get_hand() == mock_players[1].get_hand())
    print("Player turn:", mock_game_state["playerTurn"])
    print("Size of discard pile:", mock_game_state["discardPile"].size())
    print("Size of stock pile:", mock_game_state["stockPile"].size())


def test_mock_game_play():
    mock_hand_p1 = [[0, 1], [1, 1], [2, 1], [3, 1], [0, 2], [1, 3], [2, 4]]
    mock_hand_p2 = [[0, 4], [0, 5], [0, 6], [3, 3], [0, 7], [2, 3], [1, 4]]
    game = Game()
    pile_size_discard = 18
    mock_game_setup(mock_hand_p1, mock_hand_p2, game, pile_size_discard)
    game.game_loop()
