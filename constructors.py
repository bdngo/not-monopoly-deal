from typing import Sequence

from cards import (
    Birthday,
    Card,
    Color,
    DealBreaker,
    DebtCollector,
    Denomination,
    ForcedDeal,
    Hotel,
    House,
    Money,
    PassGo,
    Property,
    Rent,
    SlyDeal,
    TargetedRent,
    UberWildCard,
    WildCard,
)


def construct_money() -> Sequence[Card]:
    """Return a list of Money instances."""
    money = (
        [Money(Denomination.ONE)] * 6
        + [Money(Denomination.TWO)] * 5
        + [Money(Denomination.THREE)] * 3
        + [Money(Denomination.FOUR)] * 3
        + [Money(Denomination.FIVE)] * 2
        + [Money(Denomination.TEN)]
    )
    return money


def construct_properties() -> Sequence[Card]:
    """Return a list of Property instances."""
    color_amount_lookup = {
        Color.BROWN: ["Baltic Avenue", "Mediterranean Avenue"],
        Color.LIGHT_BLUE: ["Connecticut Avenue", "Oriental Avenue", "Vermont Avenue"],
        Color.PURPLE: ["St. Charles Avenue", "Virginia Avenue", "States Avenue"],
        Color.ORANGE: ["New York Avenue", "St. James Place", "Tennessee Avenue"],
        Color.RED: ["Kentucky Avenue", "Indiana Avenue", "Illinois Avenue"],
        Color.YELLOW: ["Ventnor Avenue", "Marvin Gardens", "Atlantic Avenue"],
        Color.GREEN: ["North Carolina Avenue", "Pacific Avenue", "Pennsylvania Avenue"],
        Color.BLUE: ["Boardwalk", "Park Place"],
        Color.RAILROAD: [
            "Short Line",
            "B. & O. Railroad",
            "Reading Railroad",
            "Pennsylvania Railroad",
        ],
        Color.UTILITY: ["Water Works", "Electric Company"],
    }

    properties = []
    for color, names in color_amount_lookup.items():
        properties.extend([Property(color, n) for n in names])
    properties.extend(
        [
            WildCard((Color.YELLOW, Color.RED)),
            WildCard((Color.ORANGE, Color.PURPLE)),
            UberWildCard(),
            UberWildCard(),
        ]
        * 2
    )
    properties.extend(
        [
            WildCard((Color.GREEN, Color.BLUE)),
            WildCard((Color.BROWN, Color.LIGHT_BLUE)),
            WildCard((Color.RAILROAD, Color.GREEN)),
            WildCard((Color.RAILROAD, Color.LIGHT_BLUE)),
            WildCard((Color.RAILROAD, Color.UTILITY)),
        ]
    )
    return properties


def construct_rents() -> Sequence[Card]:
    """Return a list of Rent instances."""
    rents = [
        Rent((Color.GREEN, Color.BLUE)),
        Rent((Color.BROWN, Color.LIGHT_BLUE)),
        Rent((Color.PURPLE, Color.ORANGE)),
        Rent((Color.RAILROAD, Color.UTILITY)),
        Rent((Color.YELLOW, Color.RED)),
    ] * 2 + [TargetedRent()] * 3
    return rents


def construct_actions() -> Sequence[Card]:
    """Return a list of action cards."""
    actions = []
    actions.extend([PassGo()] * 10 + [DealBreaker()] * 2)
    actions.extend(
        [
            DebtCollector(),
            Birthday(),
            SlyDeal(),
            ForcedDeal(),
            House(),
            Hotel(),
        ]
        * 3
    )
    return actions


def construct_deck() -> list[Card]:
    """Combine all sub-constructors to create a full deck."""
    return (
        construct_money()
        + construct_properties()
        + construct_rents()
        + construct_actions()
    )
