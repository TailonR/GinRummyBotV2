"""
    >>> test_create_rankings()
    {'[0, 1]': 100000, '[1, 1]': 100000, '[2, 1]': 100000, '[3, 1]': 100000, '[0, 13]': 0, '[0, 3]': 500, '[0, 4]': 500}
    {'[0, 1]': 100000, '[0, 2]': 100000, '[0, 3]': 200000, '[1, 3]': 200000, '[2, 3]': 100000, '[1, 4]': 100000, '[1, 5]': 100000}

    >>> test_find_runs()
    [[[0, 3], [0, 4]]]
    [[[0, 1], [0, 2], [0, 3], [0, 4]]]

    >>> test_find_sets()
    [[[0, 1], [3, 1]]]
    [[[0, 1], [1, 1], [2, 1], [3, 1]]]

    >>> test_add_card()
    {'[0, 1]': 200000, '[1, 1]': 100000, '[2, 1]': 100000, '[3, 1]': 100000, '[0, 13]': 0, '[0, 3]': 100500, '[0, 4]': 100500, '[0, 2]': 100000}
    {'[0, 1]': 100000, '[1, 1]': 100000, '[2, 1]': 100000, '[3, 1]': 100000, '[0, 13]': 0, '[0, 3]': 500, '[0, 4]': 500, '[1, 12]': 0}

    >>> test_remove_card()
    [[0, 1], [1, 1], [2, 1], [3, 1], [0, 13], [0, 3]]
    {'[0, 1]': 100000, '[1, 1]': 100000, '[2, 1]': 100000, '[3, 1]': 100000, '[0, 13]': 0, '[0, 3]': 0}
    [[0, 1], [1, 1], [3, 1], [0, 13], [0, 3]]
    {'[0, 1]': 100000, '[1, 1]': 100000, '[3, 1]': 100000, '[0, 13]': 0, '[0, 3]': 0}

    >>> test_winning_hand()
    False
    True

    >>> test_add_then_remove()
    [[0, 1], [1, 1], [3, 1], [0, 13], [0, 3], [0, 4], [0, 2]]
    {'[0, 1]': 200000, '[1, 1]': 100000, '[3, 1]': 100000, '[0, 13]': 0, '[0, 3]': 100500, '[0, 4]': 100500, '[0, 2]': 100000}
    [[0, 1], [1, 1], [2, 1], [3, 1], [0, 13], [0, 3], [0, 4]]
    {'[0, 1]': 100000, '[1, 1]': 100000, '[2, 1]': 100000, '[3, 1]': 100000, '[0, 13]': 0, '[0, 3]': 500, '[0, 4]': 500}

    >>> test_least_valued_card()
    4

"""
from hand import Hand


def test_create_rankings():
    mock_hand = [[0, 1], [1, 1], [2, 1], [3, 1], [0, 13], [0, 3], [0, 4]]
    mock_hand2 = [[0, 1], [0, 2], [0, 3], [1, 3], [2, 3], [1, 4], [1, 5]]
    hand = Hand(mock_hand)
    hand2 = Hand(mock_hand2)
    print(hand.get_rankings())
    print(hand2.get_rankings())


def test_add_card():
    mock_hand = [[0, 1], [1, 1], [2, 1], [3, 1], [0, 13], [0, 3], [0, 4]]
    hand = Hand(mock_hand)
    hand2 = Hand(mock_hand)
    card = [0, 2]
    card2 = [1, 12]
    hand.add_to_cards(card)
    hand2.add_to_cards(card2)
    print(hand.get_rankings())
    print(hand2.get_rankings())


def test_find_runs():
    mock_hand_no_run = [[0, 1], [1, 1], [2, 1], [3, 1], [0, 13], [0, 3], [0, 4]]
    hand = Hand(mock_hand_no_run)
    print(hand.find_runs())
    mock_hand_one_run = [[0, 1], [1, 1], [2, 1], [3, 1], [0, 2], [0, 3], [0, 4]]
    hand = Hand(mock_hand_one_run)
    print(hand.find_runs())


def test_find_sets():
    mock_hand_no_set = [[0, 1], [1, 7], [2, 5], [3, 1], [0, 13], [0, 3], [0, 4]]
    hand = Hand(mock_hand_no_set)
    print(hand.find_sets())
    mock_hand_one_set = [[0, 1], [1, 1], [2, 1], [3, 1], [0, 2], [0, 3], [0, 4]]
    hand = Hand(mock_hand_one_set)
    print(hand.find_sets())


def test_remove_card():
    mock_hand = [[0, 1], [1, 1], [2, 1], [3, 1], [0, 13], [0, 3], [0, 4]]
    hand = Hand(mock_hand)
    hand.remove_from_cards(len(mock_hand)-1)
    print(hand.get_cards())
    print(hand.get_rankings())
    hand.remove_from_cards(2)
    print(hand.get_cards())
    print(hand.get_rankings())


def test_winning_hand():
    mock_hand = [[0, 1], [1, 1], [2, 1], [3, 1], [0, 13], [0, 3], [0, 4]]
    mock_hand2 = [[0, 1], [1, 1], [2, 1], [3, 1], [0, 2], [0, 3], [0, 4]]
    hand = Hand(mock_hand)
    hand2 = Hand(mock_hand2)
    print(hand.all_cards_are_matched())
    print(hand2.all_cards_are_matched())


def test_add_then_remove():
    mock_hand = [[0, 1], [1, 1], [2, 1], [3, 1], [0, 13], [0, 3], [0, 4]]
    hand = Hand(mock_hand)
    hand2 = Hand(mock_hand)
    card = [0, 2]
    card2 = [1, 12]
    remove_index = 2
    remove_index2 = 7
    hand.add_to_cards(card)
    hand.remove_from_cards(remove_index)
    hand2.add_to_cards(card2)
    hand2.remove_from_cards(remove_index2)
    print(hand.get_cards())
    print(hand.get_rankings())
    print(hand2.get_cards())
    print(hand2.get_rankings())


def test_least_valued_card():
    mock_hand = [[0, 1], [1, 1], [2, 1], [3, 1], [0, 13], [0, 3], [0, 4]]
    hand = Hand(mock_hand)
    print(hand.least_valued_card_index())