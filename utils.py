import os
import json
from random import shuffle

DENOMINATIONS = (1, 2, 3, 4, 5, 10)
COLORS = {
    'Brown': 2,
    'Light Blue': 3,
    'Purple': 3,
    'Orange': 3,
    'Red': 3,
    'Yellow': 3,
    'Green': 3,
    'Blue': 2,
    'Railroad': 4,
    'Utility': 2
}
STATE_PATH = os.path.join(os.getcwd(), "tmp")
DECK_PATH = os.path.join(STATE_PATH, "deck.json")
DISCARD_PATH = os.path.join(STATE_PATH, "discards.json")
PLAYER_PATH = os.path.join(STATE_PATH, "players.json")

def draw_cards(player, number):
    """Draws NUMBER cards into PLAYER's hand."""
    for _ in range(number):
        player.draw()


def empty_deck_check(deck):
    """Checks if DECK is empty and reshuffles DISCARDS if it is."""
    with open(DISCARD_PATH, 'r') as f:
        discards = json.load(f)

    if len(deck) == 0:
        for _ in discards:
            deck.append(discards.pop())
        shuffle(deck)


def not_full_set(field_item):
    """Checks if all FIELD_ITEMs are not members of a full set."""
    color, amount = field_item[0], field_item[1]
    return amount < COLORS[color] and amount > 0


def full_set(field_item):
    """Checks if all FIELD_ITEMs are members of a full set."""
    color, amount = field_item[0], field_item[1]
    return amount >= COLORS[color]


def print_dict(dictionary):
    """Prints the keys and values of a dictionary in human-readable format.

    >>> items = {1: 2, 3: 4, 5: 6}
    >>> print_dict(items)
    1: 2
    3: 4
    5: 6
    """
    for key, value in dictionary.items():
        print('{0}: {1}'.format(key, value))


def fs_input(statement, error='', assertions=lambda: True):
    """Asks for input using STATEMENT and prints ERROR until ASSERTIONS is true.
    Returns the input.

    >>> fs_input(
    ...     'Put a number greater than 2: ',
    ...     'Not a number greater than 2',
    ...     lambda x: int(x) > 2
    ... )
    Put a number greater than 2: 1
    Not a number greater than 2
    Put a number greater than 2: a
    Not a number greater than 2
    Put a number greater than 2: 4
    '4'
    """
    while True:
        try:
            output = input(statement)
            assert assertions(output)
            break
        except (ValueError, AssertionError):
            pass
        print(error)
    return output
