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

def not_full_set(field_item):
    color, amount = field_item[0], field_item[1]
    return amount < colors[color] and amount > 0

def full_set(field_item):
    color, amount = field_item[0], field_item[1]
    return amount >= colors[color]

def print_dict(dictionary):
    for key, value in dictionary.items():
        print('{0}: {1}'.format(key, value))

## GAME FUNCTIONALITY ##
class Player:
    """Player class."""
    def __init__(self, order):
        self.order = order
        self.hand = []
        self.field = {color: 0 for color in colors.keys()}
        self.bank = {i: 0 for i in denominations}
        self.housed, self.hoteled = [], []

    def __repr__(self):
        print('Current cards on field: ')
        print_dict(self.field)
        print('\nCurrent bank: ')
        print_dict(self.bank)
        print('\nCurrent hand: ')
        for i in range(len(self.hand)):
            print('[{0}]: {1}'.format(i, self.hand[i]))
        return ''

    def draw(self):
        self.hand.append(deck.pop(0))

    def play(self, index):
        card = self.hand.pop(index)
        card.action(self)
        field_cards = [Property, WildCard, UberWildCard, House, Hotel]
        if not any([isinstance(card, i) for i in field_cards]): 
            discards.append(card)

    def pay(self, payee, amount):
        subtotal = 0
        print('\nPay up!')
        if sum(self.field.values()) + sum(self.bank.values()) == 0:
            print('Player {0} has nothing, skipping...'.format(self.order))
            return
        while subtotal < amount:
            try:
                if not sum(self.bank.values()):
                    print_dict(self.field)
                    curr_property = input('No more money! Please select a property to give up: ')
                    assert curr_property in colors.keys()
                    self.field[curr_property] -= 1
                    payee.field[curr_property] += 1
                    return
                print("Player {0}'s current bank: ".format(self.order))
                print_dict(self.bank)
                while True:
                    try:
                        curr_amount = int(input('Please select an amount to withdraw ({0}M remaining): '.format(amount - subtotal)))
                        assert self.bank[curr_amount] > 0 and curr_amount in denominations
                        break
                    except AssertionError:
                        pass
                    print('Choose money you actually have')
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
        print('------------------------------------------------------------------------------------------------')
        print("It is now Player {0}'s turn\n".format(player.order))
        print(player)
        try:
            curr_card = input('Select a card to play (type "skip" to skip turn): \n')
            if curr_card == 'skip':
                break
            else:
                curr_card = int(curr_card)
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

    def __repr__(self):
        return 'Card'

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

class WildCard(Property):
    """Can act as one of two properties. Takes 1 turn to tap."""

    def __init__(self, color1, color2):
        self.color1 = color1
        self.color2 = color2

    def __repr__(self):
        return 'Wild Card: {0}/{1}'.format(self.color1, self.color2)

    def action(self, player):
        while True:
            try:
                tapped = input('Select a color to tap: ')
                assert tapped in [self.color1, self.color2]
                break
            except (ValueError, AssertionError):
                pass
            print('Select a property that exists')
        player.field[tapped] += 1

class UberWildCard(Card):
    """Can act as any property."""

    def __repr__(self):
        return 'Über Wild Card: Can act as any property.'

    def action(self, player):
        while True:
            try:
                chosen = input('Select a color to tap: ')
                assert chosen in colors 
                break
            except (ValueError, AssertionError):
                pass
            print('Select a property that exists')
        player.field[chosen] += 1

class House(Card):
    """Adds 3M to its applied full set."""

    def __repr__(self):
        return 'House: Adds 3M to the rent of any full set.'

    def action(self, player):
        print("Player {0}'s current full sets): ".format(player.order))
        full_sets = filter(full_set, player.field.items())
        for color, amount in full_sets: 
            print('{0}: {1}'.format(color, amount))
        while True:
            try:
                applied = input('Select a property to house: ')
                assert player.field[applied] > 0 and applied in [i[0] for i in full_sets]
                break
            except (ValueError, AssertionError):
                pass
            print('Select a full set')
        player.housed.append(applied)

class Hotel(Card):
    """Adds 4M to its applied housed full set."""

    def __repr__(self):
        return 'Hotel: Adds 4M to the rent of a housed full set.'

    def action(self, player):
        print("Player {0}'s current housed full sets: ".format(player.order))
        def housed(field_item):
            color = field_item[0]
            return player.field[color] in player.housed
        for color, amount in filter(housed, filter(full_set, player.field.items())):
            print('{0}: {1}'.format(color, amount))
        applied = input('Select a property to house: ')
        player.hoteled.append(applied)

class PassGo(Card):
    """Draws 2 cards."""

    def __repr__(self):
        return 'Pass GO: Draw 2 cards.'

    def action(self, player):
        draw_cards(player, 2)

class Rent(Card):
    """Applies rent to all players."""
    can_no = True
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
        print_dict(player.field)
        while True:
            try:
                chosen_color = input('Select a property to apply rent to: ({0}/{1}) '.format(self.color1, self.color2))
                assert player.field[chosen_color] > 0 and chosen_color in [self.color1, self.color2]
                break
            except (ValueError, AssertionError):
                pass
            print('Please select a property you have')
        house_tax = 0
        if chosen_color in player.housed and chosen_color in player.hoteled:
            house_tax += 7
        elif chosen_color in player.housed:
            house_tax += 3
        total_properties = player.field[chosen_color]
        payers = players[:]
        payers.remove(player)
        for i in payers:
            i.pay(player, self.rents[chosen_color][total_properties - 1] + house_tax)

class TargetedRent(Rent):
    """Applies rent to a specific player."""

    def __init__(self):
        return

    def __repr__(self):
        return 'Targeted Rent: Force a player to pay rent on a property.'

    def action(self, player):
        while True:
            try:
                target = players[int(input('Select a player to target: '))]
                break
            except ValueError:
                pass
            print('Do not select yourself')
        print_dict(player.field)
        while True:
            try:
                chosen_color = input('Select a property to apply rent to: ')
                assert player.field[chosen_color] > 0
                break
            except (ValueError, AssertionError):
                pass
            print('Please select a property you have')
        house_tax = 0
        if chosen_color in player.housed and chosen_color in player.hoteled:
            house_tax += 7
        elif chosen_color in player.housed:
            house_tax += 3
        total_properties = player.field[chosen_color]
        target.pay(player, self.rents[chosen_color][total_properties - 1] + house_tax)

class DebtCollector(Card):
    """Forces any player to pay you 5M."""
    can_no = True

    def __repr__(self):
        return 'Debt Collector: Force any player to play you 5M.'

    def action(self, player):
        while True:
            try:
                target = players[int(input('Select a player to target: '))]
                break
            except ValueError:
                pass
            print('Do not select yourself')
        target.pay(player, 5)

class Birthday(Card):
    """Forces all players to pay you 2M."""
    can_no = True

    def __repr__(self):
        return "It's My Birthday: Force all players to pay you 2M."

    def action(self, player):
        payers = players[:]
        payers.remove(player)
        for i in payers:
            i.pay(player, 2)

class SlyDeal(Card):
    """Forces a player to give you one of their properties."""
    can_no = True

    def __repr__(self):
        return 'Sly Deal: Force any player to give you a property *not* part of a full set.'

    def action(self, player):
        while True:
            try:
                target = players[int(input('Select a player to target: '))]
                assert target is not player
                break
            except (ValueError, AssertionError):
                pass
            print('Do not select yourself')
        print("Player {0}'s current non-full sets, pick a property): ".format(target.order))
        for color, amount in filter(not_full_set, target.field.items()):
            print('{0}: {1}'.format(color, amount))
        stolen_prop = input('Select a property to sly deal: ')
        target.field[stolen_prop] -= 1
        player.field[stolen_prop] += 1

class ForcedDeal(Card):
    """Forces a player to trade a property with you."""
    can_no = True

    def __repr__(self):
        return 'Forced Deal: Force any player to trade a property *not* part of a full set with you.'

    def action(self, player):
        while True:
            try:
                target = players[int(input('Select a player to target: '))]
                break
            except ValueError:
                pass
            print('Do not select yourself')
        print("Your current field, pick a property): ".format(target.order))
        for color, amount in filter(not_full_set, player.field.items()):
            print('{0}: {1}'.format(color, amount))
        give_prop = input('Select a property to give up: ')
        print("Player {0}'s current field, pick a property): ".format(target.order))
        for color, amount in filter(not_full_set, target.field.items()):
            print('{0}: {1}'.format(color, amount))
        get_prop = input('Select a property to get: ')
        player.field[give_prop] -= 1
        target.field[get_prop] -= 1
        player.field[get_prop] += 1
        target.field[give_prop] += 1

## CONSTRUCTORS ##
def construct_money():
    money = []
    for _ in range(6):
        money.append(Money(1))
    for _ in range(5):
        money.append(Money(2))
    for _ in range(3):
        money.extend([Money(3), Money(4)])
    for _ in range(2):
        money.append(Money(5))
    money.append(Money(10))
    return money

def construct_props():
    properties = []
    for color in colors.keys():
        for _ in range(colors[color]):
            properties.append(Property(color))
    for _ in range(2):
        properties.extend([
            WildCard('Yellow', 'Red'), 
            WildCard('Orange', 'Purple')
        ]) 
    properties.extend([
        WildCard('Green', 'Blue'), 
        WildCard('Brown', 'Light Blue'), 
        WildCard('Railroad', 'Green'), 
        WildCard('Railroad', 'Light Blue'), 
        WildCard('Railroad', 'Utility'), 
    ])
    return properties

def construct_rents():
    rents = []
    for _ in range(2):
        rents.extend([
            Rent('Green', 'Blue'),
            Rent('Brown', 'Light Blue'),
            Rent('Purple', 'Orange'),
            Rent('Railroad', 'Utility'),
            Rent('Red', 'Yellow')
        ])
    for _ in range(3):
        rents.append(TargetedRent())
    return rents

def construct_actions():
    actions = []
    actions.extend([PassGo() for _ in range(10)])
    for _ in range(3):
        actions.extend([
            DebtCollector(),
            Birthday(),
            SlyDeal(),
            ForcedDeal(), 
            House(), 
            Hotel()
        ])
    return actions

## INITIALIZATION ##
deck = construct_money() + construct_props() + construct_rents() + construct_actions()

while True:
    try:
        size = int(input('Number of players: '))
        assert size >= 2 and size <= 5
        break
    except (ValueError, AssertionError):
        pass
    print('Too few or too many players')

players = [Player(i) for i in range(size)]
print('Game started with {0} players'.format(len(players)))
random.shuffle(deck)
for i in players:
    draw_cards(i, 5)

turn_count = 1
while True: # TODO: replace with win condition
    turn(players[turn_count - 1])
    turn_count = (turn_count + 1) % len(players)

