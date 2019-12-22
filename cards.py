import random

"""library = {
    properties: 39,
    action: 47,
    money: 20
}"""

denominations = (1, 2, 3, 4, 5, 10)

colors = {
    'Brown': 2,
    'Sky Blue': 3,
    'Pink': 3,
    'Orange': 3,
    'Red': 3,
    'Yellow': 3,
    'Green': 3,
    'Blue': 2,
    'Railroad': 4,
    'Utility': 2
}

## CARDS ##
class Card:
    can_no = False
    can_house = False

    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return 'Card: {0}'.format(self.number)

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

class Property(Card):
    can_house = True

    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return 'Property: {0}'.format(self.color)

    def action(self, player):
        player.field[self.color] += 1

def construct_money():
    money = []
    for _ in range(6):
        money.append(Money(1))
    for _ in range(5):
        money.append(Money(2))
    for _ in range(3):
        money.append(Money(3))
    for _ in range(3):
        money.append(Money(4))
    for _ in range(2):
        money.append(Money(5))
    money.append(Money(10))
    return money

def construct_props():
    properties = []
    for color in colors.keys():
        for _ in range(colors[color]):
            properties.append(Property(color))
    return properties

deck = construct_props() + construct_money() + [Card(i) for i in range(47)]
