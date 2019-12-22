'Not Monopoly Deal by Bryan Ngo'

from cards import *

discards = []

size = int(input('Number of players: '))
assert size >= 2 and size <= 5, 'Too few or too little players!'

## HELPER FUNCTIONS ##
def draw_cards(player, number):
    assert isinstance(player, Player)
    for _ in range(number):
        player.draw()

def empty_deck_check(deck):
    if len(deck) == 0:
        for _ in discards:
            deck += discards.pop()

## GAME FUNCTIONALITY ##
class Player:
    """Player class."""
    def __init__(self, order):
        self.order = order
        self.hand = []
        self.field = {
            'brown': 0,
            'sky blue': 0,
            'pink': 0,
            'orange': 0,
            'red': 0,
            'yellow': 0,
            'green': 0,
            'blue': 0,
            'railroad': 0,
            'utility': 0,
        }
        self.bank = {i: 0 for i in denominations}

    def __repr__(self):
        print('Current hand: ')
        for i in range(len(self.hand)):
            print('[{0}]: {1}'.format(i, self.hand[i]))
        print('\nCurrent cards on field: ')
        for color, amount in self.field.items():
            print('{0}: {1}'.format(color, amount))
        print('\nCurrent bank: ')
        for denom, count in self.bank.items():
            print('{0}: {1}'.format(denom, count))
        return ''

    def draw(self):
        self.hand.append(deck.pop(0))

    def play(self, index):
        card = self.hand.pop(index)
        card.action(self)

    def pay(self, payee, amount):
        subtotal = 0
        while subtotal < amount:
            print("Player {0}'s Current bank: ".format(self.order))
            for denom, count in self.bank.items():
                print('{0}: {1}'.format(denom, count))
            curr_amount = int(input('Please select an amount to withdraw: '))
            assert self.bank[curr_amount] > 0 and curr_amount in denominations, 'Please select money that you actually have'
            self.bank[curr_amount] -= 1
            payee.bank[curr_amount] += 1
            subtotal += curr_amount

def game_init(players):
    """Initializes a game with SIZE players."""
    print('Game started with {0} players'.format(len(players)))
    random.shuffle(deck)
    for i in players:
        draw_cards(i, 5)

def turn(player):
    """Draws 2 from DECK, then asks player to play CARD no more than 3 times."""
    assert isinstance(player, Player)
    empty_deck_check(deck)
    print("It is now Player {0}'s turn\n".format(player.order))
    draw_cards(player, 2)
    actions = 0
    while actions < 3:
        print(player)
        curr_card = int(input('Select a card to play: '))
        player.play(curr_card)
        actions += 1
        end_turn = input('{0} actions remaining. Continue? (y/n): '.format(3 - actions))
        if end_turn == 'n' or len(player.hand) == 0:
            return
    while len(player.hand) > 7:
        print(player)
        dis_card = int(input('Too many cards! Select a card to discard: '))
        discards.append(player.hand.pop(dis_card))
    return

players = [Player(i) for i in range(size)]
game_init(players)

for i in players:
    turn(i)
