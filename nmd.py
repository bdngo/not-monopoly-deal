'Not Monopoly Deal by Bryan Ngo'

from cards import *

discards = []

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
        self.field = {color: 0 for color in colors.keys()}
        self.bank = {i: 0 for i in denominations}

    def __repr__(self):
        print('Current cards on field: ')
        for color, amount in self.field.items():
            print('{0}: {1}'.format(color, amount))
        print('\nCurrent bank: ')
        for denom, count in self.bank.items():
            print('{0}: {1}'.format(denom, count))
        print('\nCurrent hand: ')
        for i in range(len(self.hand)):
            print('[{0}]: {1}'.format(i, self.hand[i]))
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
            if not sum(self.bank):
                for color, count in self.field.items():
                    print('{0}: {1}'.format(color, count))
                curr_property = input('Please select a property to give up: ')
                assert curr_property in colors.keys()
                self.bank[color] -= 1
                payee.bank[curr_amount] += 1
                return
        return

def turn(player):
    """Draws 2 from DECK, then asks player to play CARD no more than 3 times."""
    assert isinstance(player, Player), 'Not an instance of Player class'
    empty_deck_check(deck)
    draw_cards(player, 2)
    actions = 0
    while actions < 3:
        print("It is now Player {0}'s turn\n".format(player.order))
        print(player)
        curr_card = int(input('Select a card to play: '))
        player.play(curr_card)
        actions += 1
        end_turn = input('{0} actions remaining. Continue? (y/n): '.format(3 - actions))
        if end_turn == 'n' or len(player.hand) == 0:
            break
    if win(player):
        print('Player {0} wins!'.format(player.order))
        game_over()
        return
    while len(player.hand) > 7:
        print(player)
        dis_card = int(input('Too many cards! Select a card to discard: '))
        discards.append(player.hand.pop(dis_card))
    return

def win(player):
    full_sets = 0
    for property in player.field.keys():
        if player.field[property] == colors[property]:
            full_sets += 1
    if full_sets >= 3:
        return True
    return False

def game_over():
    # again = input('Game Over! Play again? (y/n): ')
    # if again == 'y':
    #     return
    print('Game Over!')

## INITIALIZATION ##

size = int(input('Number of players: '))
assert size >= 2 and size <= 5, 'Too few or too little players!'

players = [Player(i) for i in range(size)]
print('Game started with {0} players'.format(len(players)))
random.shuffle(deck)
for i in players:
    draw_cards(i, 5)

turn_count = 1
while True: # TODO: replace with win condition
    turn(players[turn_count - 1])
    turn_count = (turn_count + 1) % len(players)
