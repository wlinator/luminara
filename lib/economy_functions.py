import random

from config.parser import JsonCache

resources = JsonCache.read_json("resources")


def blackjack_get_new_deck():
    suits = resources["blackjack"]["deck_suits"]
    ranks = resources["blackjack"]["deck_ranks"]
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(rank + suit)
    random.shuffle(deck)
    return deck


def blackjack_deal_card(deck):
    return deck.pop()


def blackjack_calculate_hand_value(hand):
    value = 0
    has_ace = False
    aces_count = 0

    for card in hand:
        if card is None:
            continue

        rank = card[:-1]

        if rank.isdigit():
            value += int(rank)

        elif rank in ['J', 'Q', 'K']:
            value += 10

        elif rank == 'A':
            value += 11
            has_ace = True
            aces_count += 1

    """
    An Ace will have a value of 11 unless that would give a player 
    or the dealer a score in excess of 21; in which case, it has a value of 1
    """
    if value > 21 and has_ace:
        value -= 10 * aces_count

    return value
