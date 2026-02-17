"""Card definitions."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum, StrEnum


class Card(ABC):
    """Card superclass."""

    @property
    @abstractmethod
    def worth(self) -> int:
        """Sell value of the card."""
        pass


class Denomination(IntEnum):
    """Possible values for money cards."""

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    TEN = 10


class Color(StrEnum):
    """Possible colors of properties."""

    BROWN = "Brown"
    LIGHT_BLUE = "Light Blue"
    PURPLE = "Purple"
    ORANGE = "Orange"
    RED = "Red"
    YELLOW = "Yellow"
    GREEN = "Green"
    BLUE = "Blue"
    RAILROAD = "Railroad"
    UTILITY = "Utility"


@dataclass(frozen=True)
class Money(Card):
    """
    Used to pay off rents and the like.
    Comes in denominations of 1, 2, 3, 4, 5, 10.
    """

    value: Denomination

    @property
    def worth(self) -> int:
        return self.value


@dataclass(frozen=True)
class Property(Card):
    """Property cards."""

    color: Color
    name: str
    rent_lookup: dict[int, int]

    @property
    def worth(self) -> int:
        match self.color:
            case Color.BROWN | Color.LIGHT_BLUE:
                return 1
            case Color.ORANGE | Color.PURPLE | Color.RAILROAD | Color.UTILITY:
                return 2
            case Color.RED | Color.YELLOW:
                return 3
            case Color.GREEN | Color.BLUE:
                return 4


@dataclass(frozen=True)
class WildCard(Card):
    """Can act as one of two properties. Takes 1 turn to tap."""

    colors: tuple[Color, Color]
    rent_lookup: dict[int, int]

    @property
    def worth(self) -> int:
        color_set = frozenset(self.colors)
        worth_lookup = {
            frozenset((Color.GREEN, Color.BLUE)): 4,
            frozenset((Color.LIGHT_BLUE, Color.BROWN)): 1,
            frozenset((Color.ORANGE, Color.PURPLE)): 2,
            frozenset((Color.GREEN, Color.RAILROAD)): 4,
            frozenset((Color.LIGHT_BLUE, Color.RAILROAD)): 4,
            frozenset((Color.UTILITY, Color.RAILROAD)): 2,
            frozenset((Color.YELLOW, Color.RED)): 3,
        }
        return worth_lookup[color_set]


@dataclass(frozen=True)
class UberWildCard(Card):
    """Can act as any property."""

    @property
    def worth(self) -> int:
        return 0


@dataclass(frozen=True)
class House(Card):
    """Adds 3M to its applied full set."""

    @property
    def worth(self) -> int:
        return 3


class Hotel(Card):
    """Adds 4M to its applied housed full set."""

    @property
    def worth(self) -> int:
        return 4


class PassGo(Card):
    """Draws 2 cards."""

    @property
    def worth(self) -> int:
        return 1


@dataclass(frozen=True)
class Rent(Card):
    """Applies rent to all players."""

    colors: tuple[Color, Color]

    @property
    def worth(self) -> int:
        return 1

    # rents = {
    #     "Brown": (1, 2),
    #     "Light Blue": (2, 4, 7),
    #     "Purple": (1, 2, 4),
    #     "Orange": (1, 3, 5),
    #     "Red": (2, 3, 6),
    #     "Yellow": (2, 4, 6),
    #     "Green": (2, 4, 7),
    #     "Blue": (3, 8),
    #     "Railroad": (1, 2, 3, 4),
    #     "Utility": (1, 2),
    # }


class TargetedRent(Rent):
    """Applies rent to a specific player."""

    @property
    def worth(self) -> int:
        return 1


class DebtCollector(Card):
    """Forces any player to pay you 5M."""

    @property
    def worth(self) -> int:
        return 3


class Birthday(Card):
    """Forces all players to pay you 2M."""

    @property
    def worth(self) -> int:
        return 2


class SlyDeal(Card):
    """Forces a player to give you one of their properties."""

    @property
    def worth(self) -> int:
        return 3


class ForcedDeal(Card):
    """Forces a player to trade a property with you."""

    @property
    def worth(self) -> int:
        return 3


class DealBreaker(Card):
    """Takes a full set from a player."""

    @property
    def worth(self) -> int:
        return 5


class JustSayNo(Card):
    """Negates the actions of any other player."""

    @property
    def worth(self) -> int:
        return 4
