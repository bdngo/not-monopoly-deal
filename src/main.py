"""Not Monopoly Deal by Bryan Ngo
Repo: https://github.com/bdngo/not-monopoly-deal
"""

from random import shuffle
from utils import *
from cards import *
from constructors import *

discards = []

# GAME FUNCTIONALITY #
class Player:
    """Player class."""

    def __init__(self, order):
        self.order = order
        self.hand = []
        self.field = {color: 0 for color in COLORS.keys()}
        self.bank = {i: 0 for i in DENOMINATIONS}
        self.housed, self.hoteled = [], []

    def __repr__(self):
        print("Current cards on field: ")
        print_dict(self.field)
        print("\nCurrent bank: ")
        for denom, amount in self.bank.items():
            print(f"{denom}M: {amount}")
        print("\nCurrent hand: ")
        for i in range(len(self.hand)):
            print(f"[{i}]: {self.hand[i]}")
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
                print(f"Player {self.order} has nothing, skipping...")
                return
            if not sum(self.bank.values()):
                print_dict(self.field)
                curr_property = fs_input(
                    "No more money! Please select a property to give up: ",
                    "Choose a property you have",
                    lambda x: x in COLORS.keys() and self.field[x] > 0
                )
                self.field[curr_property] -= 1
                payee.field[curr_property] += 1
                return
            print(f"Player {self.order}'s current bank: ")
            print_dict(self.bank)
            curr_amount = int(fs_input(
                f"Please select an amount to withdraw ({amount - subtotal}M remaining): ",
                "Choose money you actually have",
                lambda x: self.bank[int(x)] > 0 and int(x) in DENOMINATIONS
            ))
            self.bank[curr_amount] -= 1
            payee.bank[curr_amount] += 1
            subtotal += curr_amount


def turn(player):
    """Draws 2 from DECK, then asks PLAYER to play CARD no more than 3 times."""
    assert isinstance(player, Player), "Not an instance of Player class"
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

    size = int(fs_input(
        "Number of players: ",
        "Too few or too many players",
        lambda x: int(x) >= 2 and int(x) <= 5
    ))

    players = [Player(i) for i in range(size)]
    print(f"Game started with {len(players)} players")
    shuffle(deck)
    for i in players:
        draw_cards(i, 5)

    turn_count = 1
    while True:
        turn(players[turn_count - 1])
        turn_count = (turn_count + 1) % len(players)

if __name__ == "__main__":
    main()

