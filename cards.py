import random

"""library = {
    properties: 39,
    action: 47,
    money: 20
}"""

colors = {
    'brown': 2,
    'sky blue': 3,
    'pink': 3,
    'orange': 3,
    'red': 3,
    'yellow': 3,
    'green': 3,
    'blue': 2,
    'railroad': 4,
    'utility': 2
}

denominations = (1, 2, 3, 4, 5, 10)

## CARDS ##
class Card:
    can_no = False
    can_house = False

    def __init__(self, number, color=None):
        self.number = number

    def __repr__(self):
        return 'Card {0}'.format(self.number)

    def action(self, player):
        return self.number

class Money(Card):

    def __init__(self, amount):
        assert amount in denominations
        self.amount = amount

    def __repr__(self):
        return 'Money: ' + str(self.amount) + 'M'

    def action(self, player):
        player.bank[self.amount] += 1

def construct_deck():
    deck = []
    for _ in range(6):
        deck.append(Money(1))
    for _ in range(5):
        deck.append(Money(2))
    for _ in range(3):
        deck.append(Money(3))
    for _ in range(3):
        deck.append(Money(4))
    for _ in range(2):
        deck.append(Money(5))
    deck.append(Money(10))
    return deck

deck = construct_deck() + [Card(i) for i in range(86)]
