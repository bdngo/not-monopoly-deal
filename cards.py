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

class Card:
    can_no = False
    can_house = False

    def __init__(self, number, color=None):
        self.number = number

    def __repr__(self):
        return 'Card {0}'.format(self.number)

    def action(self):
        return self.number


test_list = [Card(i) for i in range(106)]
