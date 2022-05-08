from hand import Hand


class Player:
    def __init__(self):
        self.hand = None
        self.num_ranks = 14
        self.num_suits = 4
        self.rank_offset = 1

    def get_hand(self):
        return self.hand.get_cards()

    def assign_hand(self, cards):
        self.hand = Hand(cards)

    def is_already_in_hand(self, card):
        if card not in self.hand:
            return False
        else:
            return True

    def create_hand(self, hand):
        self.hand = Hand(hand)

    def add_to_hand(self, card):
        self.hand.add_to_cards(card)

    def remove_from_hand(self, card_index):
        self.hand.remove_from_cards(card_index)

    def has_winning_hand(self):
        return self.hand.all_cards_are_matched()

    def get_least_valued_card_index(self):
        return self.hand.least_valued_card_index()

    def test_get_hand_rankings(self):
        return self.hand.get_rankings()

    def do_add_action(self, choice, stock_pile, discard_pile):
        if choice == 1:  # They chose the stock
            if stock_pile.size() == 0:
                new_stock_cards = discard_pile.reverse_pile()
                stock_pile.reset_pile(new_stock_cards)
                discard_pile.reset_pile()
                discard_pile.add_to_pile(stock_pile.get_top_card())

            self.add_to_hand(stock_pile.get_top_card())  # might rename these to take_from_pile
        elif choice == 0:
            self.add_to_hand(discard_pile.get_top_card())

    def do_remove_action(self, card_index, discard_pile):
        card_to_discard = self.hand.remove_from_cards(card_index)
        discard_pile.add_to_pile(card_to_discard)