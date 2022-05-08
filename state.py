import copy


class State:
    def __init__(self, game_state, initial, player_index):
        self.players = copy.deepcopy(game_state["players"])
        self.players_turn = copy.deepcopy(game_state["playerTurn"])
        self.discard_pile = copy.deepcopy(game_state["discardPile"])
        self.stock_pile = copy.deepcopy(game_state["stockPile"])
        self.start_state = initial
        self.player_index = player_index

    def is_free(self, gameboard_cell, row, column):
        if [row, column] not in self.players[0].get_hand() and [row, column] not in self.players[1].get_hand():
            return gameboard_cell
        else:
            return None

    def do_action(self, action):
        self.players[self.players_turn].do_add_action(action, self.stock_pile, self.discard_pile)
        least_valuable_card_index = self.players[self.players_turn].get_least_valued_card_index()
        self.players[self.players_turn].do_remove_action(least_valuable_card_index, self.discard_pile)

        next_player_turn = self.players_turn
        if not self.start_state:
            next_player_turn = 1 if self.players_turn == 0 else 0

        players = copy.deepcopy(self.players)
        new_game_state = {
            "players": players,
            "playerTurn": next_player_turn,
            "discardPile": self.discard_pile,
            "stockPile": self.stock_pile,
        }
        # new_state = State(new_game_state, False, self.player_index)
        return new_game_state

    def is_game_over(self):
        return self.players[0].has_winning_hand() or self.players[1].has_winning_hand()

    def game_result(self):  # return 1 or 2 depending on if player1 won or player2 won
        if self.players[self.player_index].has_winning_hand():
            return 1
        elif self.players[1 if self.player_index == 0 else 0].has_winning_hand():
            return -1
        else:
            return 0