from player import Player
from pile import Pile
from node import Node
from state import State
import random
import copy


class Game:
    def __init__(self, num_players=2):
        self.num_ranks = 13
        self.num_suits = 4
        self.rank_offset = 1
        self.stock_pile = None
        self.discard_pile = Pile()
        self.players = [Player() for i in range(num_players)]
        self.players_turn = 0
        self.num_moves_per_player = [0, 0]
        self.player1_ai = None
        self.player2_ai = None

    def choose_rank_and_suit(self, p1_hand, p2_hand):
        rank = random.randint(1, self.num_ranks)
        suit = random.randint(0, self.num_suits-1)
        while [suit, rank] in p1_hand or [suit, rank] in p2_hand:
            rank = random.randint(1, self.num_ranks)
            suit = random.randint(0, self.num_suits-1)

        return [suit, rank]

    def create_game_ai(self, node):
        self.player1_ai = node  # Eventually fix this

    def setup(self):
        p1_hand = []
        p2_hand = []
        for card in range(7):
            p1_chosen_card = self.choose_rank_and_suit(p1_hand, p2_hand)
            p1_hand.append(p1_chosen_card)
            p2_chosen_card = self.choose_rank_and_suit(p1_hand, p2_hand)
            p2_hand.append(p2_chosen_card)
        self.players[0].assign_hand(p1_hand)
        self.players[1].assign_hand(p2_hand)
        self.create_stock_pile()
        self.discard_pile.add_to_pile(self.stock_pile.get_top_card())
        self.player1_ai = Node(self.get_game_state(), 0, True)
        self.player2_ai = Node(self.get_game_state(), 1, True)

    def create_stock_pile(self):
        unused_cards = []
        for row in range(self.num_suits):
            for column in range(1, self.num_ranks + self.rank_offset):
                if ([row, column] not in self.players[0].get_hand() and
                        [row, column] not in self.players[1].get_hand()):
                    unused_cards.append([row, column])
        self.stock_pile = Pile(unused_cards)

    def is_game_over(self):
        return self.players[0].has_winning_hand() or self.players[1].has_winning_hand()

    def game_loop(self):
        print("Welcome to Rummy!")
        print("Here are the rules:")
        print(" Aces are low and can't end a run (e.x. QKA is not valid)")
        print(" Cards are represented as a pair of numbers:")
        print("  Suits:\n  0 -- hearts\n  1 -- spades\n  2 -- clubs\n  3 -- diamonds\n")
        print("  Ranks:\n  1 -- Ace\n  11 -- J\n  12 -- Q\n  13 -- K\n  The non-face cards have their number to "
              "represent them")
        print("  e.x. [2,2] is a 2 of Clubs")
        want_to_play = None
        while want_to_play != "y" and want_to_play != "n":
            # want_to_play = str(input("Play or watch (y = play, n = watch)>>> "))
            want_to_play = "n"

        while not self.is_game_over():
            # Showing the current player's hand and the discard and stock piles
            print("\n")
            player_turns_hand = self.players[self.players_turn].get_hand()
            print(f"Player{1 if self.players_turn == 0 else 2}'s hand:\n {player_turns_hand} \n")
            top_discard = self.discard_pile.display_top_card()
            print("Top discard:   Top Stock: \n", top_discard, "        [****]")

            # Choosing the card to add to the player's hand
            choice: int = -1
            if want_to_play == "n" or (want_to_play == "y" and self.players_turn % 2 != 0):
                if self.players_turn == 0:
                    choice = self.player1_ai.best_action()
                if self.players_turn == 1:
                    choice = self.player2_ai.best_action()
            elif want_to_play == "y" and self.players_turn % 2 == 0:  # This means the user is always has the first move
                choice = int(input("Enter 0 to take the top of the discard or 1 to take the top of the stock>>> "))

            self.num_moves_per_player[self.players_turn] += 1

            # Adding that card to the hand
            self.players[self.players_turn].do_add_action(choice, self.stock_pile, self.discard_pile)
            if choice == 1:  # if they chose the stock, show what the top card was
                print(f"Top stock card:\n {self.players[self.players_turn].get_hand()[7]}")

            # Chosing a card to discard
            discard_index: int = -1
            if want_to_play == "n" or (want_to_play == "y" and self.players_turn % 2 != 0):
                discard_index = self.players[self.players_turn].get_least_valued_card_index()
            elif want_to_play == "y" and self.players_turn % 2 == 0:
                discard_index = int(
                    input("Enter a number between 0 and 7 to pick a card to discard (7 is newest card)>>> "))

            # Discarding that card
            self.players[self.players_turn].do_remove_action(discard_index, self.discard_pile)
            print("\nYour hand:\n", self.players[self.players_turn].get_hand())

            # Switching turns
            self.players_turn = 1 if self.players_turn == 0 else 0
            print("\n")

            if self.is_game_over():
                print(self.num_moves_per_player)
                break

        if self.players[0].has_winning_hand():
            return 0
        elif self.players[1].has_winning_hand():
            return 1

    def get_players(self):
        return self.players

    def get_game_state(self):
        return {
            "players": self.players,
            "playerTurn": self.players_turn,
            "discardPile": self.discard_pile,
            "stockPile": self.stock_pile,
        }

    def set_players(self, players):
        self.players = copy.deepcopy(players)

    def set_game_ai(self, bot1, bot2):
        self.player1_ai = copy.deepcopy(bot1)
        self.player2_ai = copy.deepcopy(bot2)