"""Not Monopoly Deal by Bryan Ngo
Repo: https://github.com/bdngo/not-monopoly-deal
"""

import json
from random import shuffle

from cards import *
from constructors import *
from utils import *
from player import Player


def turn(player):
    """Draws 2 from DECK, then asks PLAYER to play CARD no more than 3 times."""
    assert isinstance(player, Player), "Not an instance of Player class"

    with open(DECK_PATH, 'r') as f:
        deck = json.load(f)
    with open(DISCARD_PATH, 'r') as f:
        discards = json.load(f)

    empty_deck_check(deck)
    draw_cards(player, 2)
    actions = 0
    while actions < 3:
        if not len(player.hand):
            draw_cards(player, 5)
        print('-' * 80)
        print(f"It is now Player {player.order}'s turn\n")
        print(player)
        try:
            curr_card = input(
                f"Player {player.order} has {3 - actions} action(s) remaining.\nSelect a card to play (type 'end' to end turn, 'sell' to sell card): "
            )
            if curr_card == "end" or not len(player.hand):
                break
            elif curr_card == "sell":
                print("\nCurrent hand: ")
                for i in range(len(player.hand)):
                    print(f"[{i}]: {player.hand[i]}")
                sold = int(fs_input(
                    "Select a card to sell: ",
                    "Select a non-money card in your hand",
                    lambda x: not isinstance(x, Money)
                ))
                sold_card = player.hand.pop(sold)
                player.bank[sold_card.worth] += 1
                discards.append(sold_card)
            else:
                curr_card = int(curr_card)
                player.play(curr_card)
            actions += 1
        except (ValueError, IndexError):
            pass
    if win(player):
        print(f"Player {player.order} wins!")
        game_over()
        return
    while len(player.hand) > 7:
        print(player)
        dis_card = int(fs_input("Too many cards! Select a card to discard: \n"))
        discards.append(player.hand.pop(dis_card))

    with open(DECK_PATH, 'w') as f:
        json.dump(deck, f)
    with open(DISCARD_PATH, 'w') as f:
        json.dump(discards, f)



def win(player):
    full_sets = 0
    for property in player.field.keys():
        if player.field[property] == COLORS[property]:
            full_sets += 1
    return full_sets >= 3


def game_over():
    print("Game Over!")


# INITIALIZATION #
def main():
    deck = construct_money() + construct_props() + construct_rents() + construct_actions()
    discards = []

    size = int(fs_input(
        "Number of players: ",
        "Too few or too many players",
        lambda x: int(x) >= 2 and int(x) <= 5
    ))

    players = [Player(i) for i in range(size)]
    print(f"Game started with {len(players)} players")
    shuffle(deck)

    with open(DECK_PATH, 'w') as f:
        json.dump(deck, f)
    with open(DISCARD_PATH, 'w') as f:
        json.dump(discards, f)

    for i in players:
        draw_cards(i, 5)

    turn_count = 0
    while True:
        turn(players[turn_count])
        turn_count = (turn_count + 1) % len(players)

if __name__ == "__main__":
    main()

