'Not Monopoly Deal by Bryan Ngo'

## GLOBALS ##
import random

discards = []
denominations = (1, 2, 3, 4, 5, 10)
colors = {
    'Brown': 2,
    'Light Blue': 3,
    'Pink': 3,
    'Orange': 3,
    'Red': 3,
    'Yellow': 3,
    'Green': 3,
    'Blue': 2,
    'Railroad': 4,
    'Utility': 2
}

## HELPER FUNCTIONS ##
def draw_cards(player, number):
    assert isinstance(player, Player)
    for _ in range(number):
        player.draw()

def empty_deck_check(deck):
    if len(deck) == 0:
        for _ in discards:
            deck.append(discards.pop())
        random.shuffle(deck)

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
        print('\nPay up!')
        while subtotal < amount:
            try:
                if not sum(self.bank.values()):
                    for color, count in self.field.items():
                        print('{0}: {1}'.format(color, count))
                    curr_property = input('No more money! Please select a property to give up: ')
                    assert curr_property in colors.keys()
                    self.field[curr_property] -= 1
                    payee.field[curr_property] += 1
                    return
                print("Player {0}'s current bank: ".format(self.order))
                for denom, count in self.bank.items():
                    print('{0}: {1}'.format(denom, count))
                curr_amount = int(input('Please select an amount to withdraw ({0} remaining): '.format(amount - subtotal)))
                try:
                    assert self.bank[curr_amount] > 0 and curr_amount in denominations
                except AssertionError:
                    print('Choose money you actually have')
                    pass
                self.bank[curr_amount] -= 1
                payee.bank[curr_amount] += 1
                subtotal += curr_amount
            except ValueError:
                pass

def turn(player):
    """Draws 2 from DECK, then asks player to play CARD no more than 3 times."""
    assert isinstance(player, Player), 'Not an instance of Player class'
    empty_deck_check(deck)
    draw_cards(player, 2)
    actions = 0
    while actions < 3:
        if not len(player.hand):
            draw_cards(player, 5)
        print("It is now Player {0}'s turn\n".format(player.order))
        print(player)
        try:
            curr_card = int(input('Select a card to play: \n'))
            player.play(curr_card)
            actions += 1
            end_turn = input('Player {0} has {1} action(s) remaining. Continue? (y/n): '.format(player.order, 3 - actions))
            if end_turn == 'n' or not len(player.hand):
                break
        except ValueError:
            pass
    if win(player):
        print('Player {0} wins!'.format(player.order))
        game_over()
        return
    while len(player.hand) > 7:
        print(player)
        dis_card = int(input('Too many cards! Select a card to discard: \n'))
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
    print('Game Over!')

## CARDS ##
class Card:
    can_no = False
    can_house = False
    can_steal = False

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
    can_steal = True

    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return 'Property: {0}'.format(self.color)

    def action(self, player):
        player.field[self.color] += 1

class Rent(Card):
    rents = {
        'Brown': (1, 2),
        'Light Blue': (2, 4, 7),
        'Pink': (1, 2, 4),
        'Orange': (1, 3, 5),
        'Red': (2, 3, 6),
        'Yellow': (2, 4, 6),
        'Green': (2, 4, 7),
        'Blue': (3, 8),
        'Railroad': (1, 2, 3, 4),
        'Utility': (1, 2)
    }

    def __init__(self, color1, color2):
        self.color1 = color1
        self.color2 = color2

    def __repr__(self):
        return 'Rent: {0}/{1}'.format(self.color1, self.color2)

    def action(self, player):
        print("Player {0}'s current cards on field: ".format(player.order))
        for color, amount in player.field.items():
            print('{0}: {1}'.format(color, amount))
        chosen_color = input('Select a property to apply rent to: ({0}/{1}) '.format(self.color1, self.color2))
        try:
            assert player.field[chosen_color] > 0, 'Please pick a property you have'
        except AssertionError as e:
            print(e)
            pass
        total_properties = player.field[chosen_color]
        payers = players[:]
        payers.remove(player)
        for i in payers:
            i.pay(player, self.rents[chosen_color][total_properties - 1])

## CONSTRUCTORS ##
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

def construct_rents():
    rents, i = [], 0
    for _ in range(2):
        rents.extend([
            Rent('Green', 'Blue'),
            Rent('Brown', 'Light Blue'),
            Rent('Purple', 'Orange'),
            Rent('Railroad', 'Utility'),
            Rent('Red', 'Yellow')
        ])
    return rents

## INITIALIZATION ##
deck = construct_money() + construct_props() + construct_rents()

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
