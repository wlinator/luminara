import random
from collections import Counter


def blackjack_get_new_deck():
    suits = ['♠', '♡', '♢', '♣']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
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


def calculate_slots_results(bet, results):
    type = None
    multiplier = None

    # count occurrences of each item in the list
    counts = Counter(results)

    # no icons match
    if len(counts) == 3:
        type = "lost"
        multiplier = -1

    # pairs
    elif len(counts) == 2:
        type = "pair"
        multiplier = 1

    # 3 of a kind
    elif len(counts) == 1:
        if results[0] == 5:
            type = "three_diamonds"
            multiplier = 4
        elif results[0] == 6:
            type = "jackpot"
            multiplier = 5
        else:
            type = "three_of_a_kind"
            multiplier = 3

    payout = bet * multiplier
    return type, payout, multiplier
