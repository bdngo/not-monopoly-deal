'Not Monopoly Deal by Bryan Ngo'

from cards import *

deck = test_list
discards = []

players = int(input('Number of players: '))
assert players > 2 and players <= 5
hands = {i: [] for i in range(players)}

## HELPER FUNCTIONS ##
def print_hand(hand):
    for i in range(len(hand)):
        print('[{0}]: {1}'.format(i, hand[i]))

def draw_cards(hand, number):
    hand += [deck.pop(i) for i in range(number)]

## GAME FUNCTIONALITY ##
def game_init(size):
    """Initializes a game with N players."""
    print('Game started with {0} players'.format(size))
    random.shuffle(deck)
    for i in range(size):
        draw_cards(hands[i], 5)

def turn(player):
    """Draws 2 from DECK, then asks player to play CARD no more than 3 times."""
    empty_deck_check()
    player_hand, actions = hands[player], 0
    draw_cards(player_hand, 2)
    while actions < 3:
        print_hand(player_hand)
        curr_card = int(input('Select a card to play: '))
        card = player_hand.pop(curr_card)
        card.action()
        actions += 1
        end_turn = input('End Turn? (y/n): ')
        while len(player_hand) > 7:
            print_hand(player_hand)
            dis_card = int(input('Select a card to discard: '))
            discards += player_hand.pop(dis_card)
        if end_turn == 'y' or len(player_hand) == 0:
            break
    return

def empty_deck_check():
    if len(deck) == 0:
        for _ in discards:
            deck += discards.pop()

game_init(players)

for i in range(players):
    turn(i)
