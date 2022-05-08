"""

    >>> test_state()
    Number of players in state same as game? True
    Player turn in state is same as game? True
    Discard pile in state is same as game? True
    Stock pile in state is same as game? True

    >>> test_node()
    Node state is equal to mock_game_state? True

    >>> test_best_card_to_add()
    The best move is to pick stock
    The best move is to pick discard

    >>> test_player2_win()
    1
"""
from game import Game
from player import Player
from state import State
from node import Node
from pile import Pile


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


def second_mock_game_setup(hand_p1, hand_p2, card1, card2, game):
    mock_players = [Player() for _ in range(2)]
    mock_players[0].create_hand(hand_p1)
    mock_players[1].create_hand(hand_p2)
    game.set_players(mock_players)
    unused_cards = []
    for row in range(4):
        for column in range(1, 13):
            if ([row, column] not in mock_players[0].get_hand() and
                    [row, column] not in mock_players[1].get_hand() and
                    [row, column] != card1 and [row, column] != card2):
                unused_cards.append([row, column])

    game.stock_pile = Pile(unused_cards)
    game.stock_pile.add_to_pile(card1)
    game.discard_pile.add_to_pile(card2)
    # initial_state = State(game.get_game_state(), True)
    game.create_game_ai(Node(game.get_game_state(), 0, True))


def are_lists_equal(list1, list2):
    if list1.size() != list2.size():
        return False
    for index in range(0, list1.size()):
        if list1.pile[index] != list2.pile[index]:
            return False
    return True


def test_state():
    mock_hand_p1 = [[0, 1], [1, 1], [2, 1], [3, 1], [0, 2], [1, 3], [2, 4]]
    mock_hand_p2 = [[0, 4], [0, 5], [0, 6], [3, 3], [0, 7], [2, 3], [1, 4]]
    game = Game()
    mock_game_setup(mock_hand_p1, mock_hand_p2, game, 1)
    initial_state = State(game.get_game_state(), True, 0)
    print("Number of players in state same as game?", len(initial_state.players) == len(game.players))
    print("Player turn in state is same as game?", game.players_turn == initial_state.players_turn)
    print("Discard pile in state is same as game?", are_lists_equal(game.discard_pile, initial_state.discard_pile))
    print("Stock pile in state is same as game?", are_lists_equal(game.stock_pile, initial_state.stock_pile))


def are_states_equal(state, stateN):  # state is test state, stateN is node state
    are_equal = True
    if len(state.players) != len(stateN.players):
        are_equal = False

    if state.players_turn != stateN.players_turn:
        are_equal = False

    if not are_lists_equal(state.discard_pile, stateN.discard_pile):
        are_equal = False

    if not are_lists_equal(state.stock_pile, stateN.stock_pile):
        are_equal = False

    return are_equal


def test_node():
    mock_hand_p1 = [[0, 1], [1, 1], [2, 1], [3, 1], [0, 2], [1, 3], [2, 4]]
    mock_hand_p2 = [[0, 4], [0, 5], [0, 6], [3, 3], [0, 7], [2, 3], [1, 4]]
    game = Game()
    mock_game_setup(mock_hand_p1, mock_hand_p2, game, 1)
    initial_state = State(game.get_game_state(), True, 0)
    game_ai = Node(game.get_game_state(), 0, True)
    print("Node state is equal to mock_game_state?", are_states_equal(initial_state, game_ai.state))


def test_best_card_to_add():
    mock_hand_p1 = [[0, 1], [1, 1], [2, 1], [3, 1], [3, 2], [3, 3], [2, 4]]
    mock_hand_p2 = [[0, 4], [0, 5], [0, 6], [0, 7], [1, 7], [2, 7], [1, 4]]
    card_1 = [3, 4]
    card_2 = [0, 3]
    game = Game()
    second_mock_game_setup(mock_hand_p1, mock_hand_p2, card_1, card_2, game)
    game_ai = Node(game.get_game_state(), 0, True)
    best_move = game_ai.best_action()

    game2 = Game()
    second_mock_game_setup(mock_hand_p1, mock_hand_p2, card_2, card_1, game2)
    second_game_ai = Node(game2.get_game_state(), 0, True)
    best_move2 = second_game_ai.best_action()
    print("The best move is to", "pick stock" if best_move == 1 else "pick discard")
    print("The best move is to", "pick stock" if best_move2 == 1 else "pick discard")


def test_player2_win():
    mock_hand_p1 = [[0, 4], [0, 5], [0, 6], [0, 7], [1, 7], [2, 7], [1, 4]]
    mock_hand_p2 = [[0, 1], [1, 1], [2, 1], [3, 1], [3, 2], [3, 3], [2, 4]]
    card_1 = [3, 4]
    card_2 = [0, 3]
    game = Game()
    second_mock_game_setup(mock_hand_p1, mock_hand_p2, card_1, card_2, game)
    game_ai = Node(game.get_game_state(), 1, True)
    game.players_turn = 1 if game.players_turn == 0 else 0
    game.players[game.players_turn].do_add_action(0, game.stock_pile, game.discard_pile)
    least_valuable_card_index = game.players[game.players_turn].get_least_valued_card_index()
    game.players[game.players_turn].do_remove_action(least_valuable_card_index, game.discard_pile)
    best_move = game_ai.best_action()
    print(best_move)

