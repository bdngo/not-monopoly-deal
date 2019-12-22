'Not Monopoly Deal by Bryan Ngo'

from cards import *

deck = test_list
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
        self.field = {}

    def __repr__(self):
        return str(['[{0}]: {1}'.format(i, self.hand[i]) for i in range(len(self.hand))])

    def draw(self):
        self.hand.append(deck.pop(0))

    def play(self, index):
        card = self.hand.pop(index)
        card.action()

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
    print("It is now Player {0}'s turn".format(player.order))
    draw_cards(player, 2)
    actions = 0
    while actions < 3:
        print(player)
        curr_card = int(input('Select a card to play: '))
        player.play(curr_card)
        actions += 1
        end_turn = input('Continue? (y/n): ')
        while len(player.hand) > 7:
            print(player)
            dis_card = int(input('Too many cards! Select a card to discard: '))
            discards.append(player.hand.pop(dis_card))
        if end_turn == 'n' or len(player.hand) == 0:
            break
    return

players = [Player(i) for i in range(size)]
game_init(players)

for i in players:
    turn(i)
