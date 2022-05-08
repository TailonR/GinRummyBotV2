import random


class Pile:
    def __init__(self, pile=None):
        if pile is not None:
            self.shuffle(pile)
        self.pile = pile

    def shuffle(self, cards):
        random.shuffle(cards)

    def get_top_card(self):
        card = self.pile.pop()
        return card

    def display_top_card(self):
        card = self.pile[-1]
        return card

    def reset_pile(self, cards=None):
        if cards is None:
            self.pile = []
        else:
            self.pile = cards

    def reverse_pile(self):
        self.pile.reverse()
        return self.pile

    def add_to_pile(self, card):
        if self.pile is None:
            self.pile = [card]
        else:
            self.pile.append(card)

    def size(self):
        return len(self.pile)

