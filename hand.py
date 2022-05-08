import copy


class Hand:
    def __init__(self, list_of_cards):
        self.num_suits = 4
        self.num_ranks = 13
        self.rank_offset = 1
        self.cards = copy.deepcopy(list_of_cards)
        self.rankings = {}
        self.create_rankings()

    def all_cards_are_matched(self):
        all_sets = self.find_sets()
        cards_remaining = []
        num_matched_cards = 0
        for single_set in all_sets:
            if len(single_set) < 3:
                return False
            num_matched_cards += len(single_set)
            cards_remaining = [card for card in self.cards if card not in single_set]

        all_runs = self.find_runs(cards_remaining)
        for run in all_runs:
            if len(run) < 3:
                return False
            num_matched_cards += len(run)

        if num_matched_cards == 7:
            return True

    def least_valued_card_index(self):
        prev_value = 10000000000
        card_index = 0
        for (index, card) in enumerate(self.cards):
            if self.rankings[f"{card}"] < prev_value:
                prev_value = self.rankings[f"{card}"]
                card_index = index
        return card_index

    def remove_from_cards(self, card_index):
        del self.rankings[f"{self.cards[card_index]}"]
        return self.cards.pop(card_index)

    def add_to_cards(self, card):
        self.cards.append(card)
        self.rankings.update({f"{card}": 0})
        self.update_rankings()

    def get_rankings(self):
        return self.rankings

    def get_cards(self):
        return self.cards

    def create_rankings(self):
        for card in self.cards:
            self.rankings.update({f"{card}": 0})
        all_sets = self.find_sets()
        all_runs = self.find_runs()
        self.score_hand(all_sets, all_runs)

    def add_to_rankings(self, card):
        self.rankings.update({f"{card}": 0})

    def update_rankings(self):
        # print("rankings (before scoring):\n", self.rankings)
        self.rankings = self.rankings.fromkeys(self.rankings, 0)
        all_sets = self.find_sets()
        all_runs = self.find_runs()
        self.score_hand(all_sets, all_runs)
        # print("rankings (after scoring):\n", self.rankings)

    def score_hand(self, sets, runs):
        if sets is not None:
            for card_set in sets:
                self.score_cards(card_set)

        if runs is not None:
            for run in runs:
                self.score_cards(run)

    def score_cards(self, cards):
        if len(cards) > 2:
            for card in cards:
                self.rankings[f"{card}"] += 100000
        elif len(cards) < 3:
            for card in cards:
                self.rankings[f"{card}"] += 500

    def find_sets(self, card_list=None):
        cards: []
        if card_list is None:
            cards = self.cards
        else:
            cards = card_list
        all_sets = []
        for rank_index in range(1, self.num_ranks+self.rank_offset):
            possible_set = [card for card in cards if card[1] == rank_index]
            if 1 < len(possible_set) <= 4:
                all_sets.append(possible_set)
        return all_sets

    def find_runs(self, card_list=None):
        cards: []
        if card_list is None:
            cards = self.cards
        else:
            cards = card_list
        hand = sorted(cards, key=lambda card: card[1])
        all_runs = []
        for suit_index in range(self.num_suits):
            possible_run = [card for card in hand if card[0] == suit_index]
            if len(possible_run) == 0:
                continue
            first_index = 0
            while first_index < len(possible_run):
                second_index = first_index
                key = possible_run[second_index][1]
                run = [possible_run[second_index]]
                while second_index < len(possible_run):
                    if possible_run[second_index][1] - key == 1:
                        run.append(possible_run[second_index])
                        key = possible_run[second_index][1]
                    elif possible_run[second_index][1] - key != 0:
                        break
                    second_index += 1
                first_index = second_index
                if 1 < len(run) <= 4 or len(run) == 7:
                    all_runs.append(run)
                elif len(run) > 4:
                    all_runs.append(run[:4])

        return all_runs
