"""Not Monopoly Deal by Bryan Ngo
Repo: https://github.com/bdngo/not-monopoly-deal
"""

# GLOBALS #
from random import shuffle

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


# HELPER FUNCTIONS #
def draw_cards(player, number):
    """Draws NUMBER cards into PLAYER's hand."""
    assert isinstance(player, Player)
    for _ in range(number):
        player.draw()


def empty_deck_check(deck):
    """Checks if DECK is empty and reshuffles DISCARDS if it is."""
    if len(deck) == 0:
        for _ in discards:
            deck.append(discards.pop())
        shuffle(deck)


def not_full_set(field_item):
    """Checks if all FIELD_ITEMs are not members of a full set."""
    color, amount = field_item[0], field_item[1]
    return amount < colors[color] and amount > 0


def full_set(field_item):
    """Checks if all FIELD_ITEMs are members of a full set."""
    color, amount = field_item[0], field_item[1]
    return amount >= colors[color]


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


def fs_input(statement, error, assertions=lambda x: True):
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


# GAME FUNCTIONALITY #
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
        while subtotal < amount:
            if sum(self.field.values()) + sum(self.bank.values()) == 0:
                print('Player {0} has nothing, skipping...'.format(self.order))
                return
            try:
                if not sum(self.bank.values()):
                    print_dict(self.field)
                    curr_property = input('No more money! Please select a property to give up: ')
                    assert curr_property in colors.keys() and self.field[curr_property] > 0
                    self.field[curr_property] -= 1
                    payee.field[curr_property] += 1
                    return
                print("Player {0}'s current bank: ".format(self.order))
                print_dict(self.bank)
                curr_amount = int(fs_input(
                    'Please select an amount to withdraw ({0}M remaining): '.format(amount - subtotal),
                    'Choose money you actually have',
                    lambda x: self.bank[int(x)] > 0 and int(x) in denominations
                ))
                self.bank[curr_amount] -= 1
                payee.bank[curr_amount] += 1
                subtotal += curr_amount
            except ValueError:
                pass


def turn(player):
    """Draws 2 from DECK, then asks PLAYER to play CARD no more than 3 times."""
    assert isinstance(player, Player), 'Not an instance of Player class'
    empty_deck_check(deck)
    draw_cards(player, 2)
    actions = 0
    while actions < 3:
        if not len(player.hand):
            draw_cards(player, 5)
        print('--------------------------------------------------------------------------------')
        print("It is now Player {0}'s turn\n".format(player.order))
        print(player)
        try:
            curr_card = input(
                'Player {0} has {1} action(s) remaining.\n'
                'Select a card to play (type "end" to end turn): '.format(player.order, 3 - actions)
            )
            if curr_card == 'end' or not len(player.hand):
                break
            else:
                curr_card = int(curr_card)
            player.play(curr_card)
            actions += 1
        except (ValueError, IndexError):
            pass
    if win(player):
        print('Player {0} wins!'.format(player.order))
        game_over()
        return
    while len(player.hand) > 7:
        print(player)
        dis_card = int(input('Too many cards! Select a card to discard: \n'))
        discards.append(player.hand.pop(dis_card))


def win(player):
    full_sets = 0
    for property in player.field.keys():
        if player.field[property] == colors[property]:
            full_sets += 1
    return full_sets >= 3


def game_over():
    print('Game Over!')


# CARDS #
class Card:
    """Card superclass."""
    can_no = False
    can_house = False

    def __repr__(self):
        return 'Card'

    def action(self, player):
        return self.number


class Money(Card):
    """Used to pay off rents and the like.
    Comes in denoominations of 1, 2, 3, 4, 5, 10.
    """

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
        tapped = fs_input(
            'Select a color to tap: ',
            'Select a property that exists',
            lambda x: x in [self.color1, self.color2]
        )
        player.field[tapped] += 1


class UberWildCard(Card):
    """Can act as any property."""

    def __repr__(self):
        return 'Über Wild Card: Can act as any property.'

    def action(self, player):
        chosen = fs_input(
            'Select a color to tap: ',
            'Select a property that exists',
            lambda x: x in colors
        )
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
        applied = fs_input(
            'Select a property to house: ',
            'Select a full set',
            lambda x: x in map(lambda x: x[0], full_sets)
        )
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
        full_housed = filter(housed, filter(full_set, player.field.items()))
        for color, amount in full_housed:
            print('{0}: {1}'.format(color, amount))
        applied = fs_input(
            'Select a property to hotel: ',
            'Select a full set',
            lambda x: player.field[x] > 0 and x in map(lambda x: x[0], full_housed)
        )
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
        chosen_color = fs_input(
            'Select a property to apply rent to: ({0}/{1}) '.format(self.color1, self.color2),
            'Please select a property you have',
            lambda x: player.field[x] > 0 and x in [self.color1, self.color2]
        )
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
        target = players[int(fs_input(
            'Select a player to target: ',
            'Do not select yourself',
            lambda x: int(x) != player.order
        ))]
        print_dict(player.field)
        chosen_color = fs_input(
            'Select a property to apply rent to: ',
            'Please select a property you have',
            lambda x: player.field[x] > 0
        )
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
        return 'Debt Collector: Force any player to pay you 5M.'

    def action(self, player):
        target = players[int(fs_input(
            'Select a player to target: ',
            'Do not select yourself',
            lambda x: x != player.order
        ))]
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
        target = players[int(fs_input(
            'Select a player to target: ',
            'Do not select yourself',
            lambda x: int(x) != player.order
        ))]
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
        target = players[int(fs_input(
            'Select a player to target: ',
            'Do not select yourself',
            lambda x: int(x) != player.order
        ))]
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


class DealBreaker(Card):
    """Takes a full set from a player."""
    can_no = True

    def __repr__(self):
        return 'Deal Breaker: Steal a full set.'

    def action(self, player):
        target = players[int(fs_input(
            'Select a player to target: ',
            'Do not select yourself',
            lambda x: int(x) != player.order
        ))]
        print("Player {0}'s full sets: ".format(target.order))
        full_sets = filter(full_set, player.field.items())
        for color, amount in full_sets:
            print('{0}: {1}'.format(color, amount))
        chosen_set = fs_input(
            'Select a full set: ',
            'Select a *full* set that actually exists',
            lambda x: x in map(lambda x: x[0], full_sets)
        )
        player.field[chosen_set] += target.field[chosen_set]
        target.field[chosen_set] = 0


# CONSTRUCTORS #
def construct_money():
    """Returns a list of Money instances."""
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
    """Returns a list of Property instances."""
    properties = []
    for color in colors.keys():
        for _ in range(colors[color]):
            properties.append(Property(color))
    for _ in range(2):
        properties.extend([
            WildCard('Yellow', 'Red'),
            WildCard('Orange', 'Purple')
            UberWildCard(),
            UberWildCard()
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
    """Returns a list of Rent instances."""
    rents = []
    for _ in range(2):
        rents.extend([
            Rent('Green', 'Blue'),
            Rent('Brown', 'Light Blue'),
            Rent('Purple', 'Orange'),
            Rent('Railroad', 'Utility'),
            Rent('Yellow', 'Red')
        ])
    for _ in range(3):
        rents.append(TargetedRent())
    return rents


def construct_actions():
    """Returns a list of action cards."""
    actions = []
    actions.extend(
        [PassGo() for _ in range(10)]
        + [DealBreaker(), DealBreaker()]
    )
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


# INITIALIZATION #
deck = construct_money() + construct_props() + construct_rents() + construct_actions()

size = int(fs_input(
    'Number of players: ',
    'Too few or too many players',
    lambda x: int(x) >= 2 and int(x) <= 5
))

players = [Player(i) for i in range(size)]
print('Game started with {0} players'.format(len(players)))
shuffle(deck)
for i in players:
    draw_cards(i, 5)

turn_count = 1
while True:
    turn(players[turn_count - 1])
    turn_count = (turn_count + 1) % len(players)

