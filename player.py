import os
import json

from utils import *
from cards import *


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
        with open(DECK_PATH, 'r') as f:
            deck = json.load(f)

        self.hand.append(deck.pop(0))

        with open(DECK_PATH, 'w') as f:
            json.dump(deck, f)

    def play(self, index):
        with open(DISCARD_PATH, 'r') as f:
            discards = json.load(f)

        card = self.hand.pop(index)
        card.action(self)
        field_cards = [Property, WildCard, UberWildCard, House, Hotel]
        if not any([isinstance(card, i) for i in field_cards]):
            discards.append(card)

        with open(DISCARD_PATH, 'w') as f:
            json.dump(discards, f)

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
