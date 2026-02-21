from dataclasses import dataclass, field
from typing import Self

from cards import Card, Color, Denomination

DRAW_SIZE = 2


@dataclass
class PropertySet:
    """Represents a group of colors placed on the field."""

    num_properties: int = 0
    is_housed: bool = False
    is_hoteled: bool = False


@dataclass
class Player:
    """Player class."""

    hand: list[Card] = field(default_factory=list)
    properties: dict[Color, PropertySet] = field(
        default_factory=lambda: {c: PropertySet() for c in Color}
    )
    bank: dict[Denomination, int] = field(
        default_factory=lambda: {d: 0 for d in Denomination}
    )

    def draw(self, deck: list[Card]) -> None:
        for _ in range(DRAW_SIZE):
            self.hand.append(deck.pop())

    def play(self) -> None:
        raise NotImplementedError

    def pay(self, payee: Self, amount: int) -> None:
        raise NotImplementedError
        # subtotal = 0
        # print("\nPay up!")
        # while subtotal < amount:
        #     if sum(self.field.values()) + sum(self.bank.values()) == 0:
        #         print(f"Player {self.order} has nothing, skipping...")
        #         return
        #     if not sum(self.bank.values()):
        #         print_dict(self.field)
        #         curr_property = fs_input(
        #             "No more money! Please select a property to give up: ",
        #             "Choose a property you have",
        #             lambda x: x in COLORS.keys() and self.field[x] > 0,
        #         )
        #         self.field[curr_property] -= 1
        #         payee.field[curr_property] += 1
        #         return
        #     print(f"Player {self.order}'s current bank: ")
        #     print_dict(self.bank)
        #     curr_amount = int(
        #         fs_input(
        #             f"Please select an amount to withdraw ({amount - subtotal}M remaining): ",
        #             "Choose money you actually have",
        #             lambda x: self.bank[int(x)] > 0 and int(x) in DENOMINATIONS,
        #         )
        #     )
        #     self.bank[curr_amount] -= 1
        #     payee.bank[curr_amount] += 1
        #     subtotal += curr_amount
