import random

import numpy as np
from state import State
import copy


# Code taken from https://ai-boson.github.io/mcts/
class Node:
    def __init__(self, state_dict, player_index, on_first_level, parent=None, parent_action=None):
        self.state = State(state_dict, on_first_level, player_index)
        self.parent = parent
        self.parent_action = copy.deepcopy(parent_action)
        self.children = []
        self.player_index = player_index
        self.number_of_visits = 0
        self.results = {1: 0, -1: 0, 0: 0}  # games won/lost/not-finished
        self._untried_actions = [0, 1]
        self.number_of_nodes_visited = 0

    def win_loss_difference(self):
        wins = self.results[1]
        loses = self.results[-1]
        return wins - loses

    def num_visited(self):
        return self.number_of_visits

    def expand(self):
        action = self._untried_actions.pop()
        current_state = copy.deepcopy(self.state)
        next_state = current_state.do_action(action)
        child_node = Node(next_state, self.player_index, False, self, action)
        self.children.append(child_node)
        self.number_of_nodes_visited += 1
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def simulate(self):
        current_state = self.state
        while not current_state.is_game_over():
            action = self.choose_next_action([0, 1])
            current_state = State(current_state.do_action(action), False, self.player_index)
        return current_state.game_result()

    def choose_next_action(self, possible_moves):  # We are only going to do a binary decision tree, only two possible moves
        return possible_moves.pop(random.randint(0, len(possible_moves)-1))

    def update(self, result):
        parent_node = self
        while parent_node is not None:
            parent_node.number_of_visits += 1
            parent_node.results[result] += 1
            parent_node = parent_node.parent

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c=0.1):
        choices_weights = [(child.win_loss_difference() / child.number_of_visits) + c * np.sqrt((2 * np.log(self.number_of_visits) / child.number_of_visits)) for child in self.children]
        return self.children[np.argmax(choices_weights)]

    def tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()

        return current_node

    def print_tree(self, node, level_markers=None, marker_string="+-"):
        if level_markers is None:
            level_markers = []
        empty_string = " " * len(marker_string)
        level = len(level_markers)  # recursion level
        connection_string = "|" + empty_string[:-1]
        markers = "".join(map(lambda draw: connection_string if draw else empty_string, level_markers[:-1]))
        markers += marker_string if level > 0 else ""
        print(markers, node.parent_action if node.parent_action is not None else "")

        for i, child in enumerate(node.children):
            is_last = i == len(node.children) - 1
            self.print_tree(child, [*level_markers, not is_last], marker_string)

    def best_action(self):
        simulation_no = 100
        for i in range(simulation_no):
            policy = self.tree_policy()
            reward = policy.simulate()
            # self.print_tree(self)
            policy.update(reward)
        return self.best_child().get_parent_action()

    def get_parent_action(self):
        return self.parent_action
