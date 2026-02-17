from cards import *

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
    for color in COLORS.keys():
        for _ in range(COLORS[color]):
            properties.append(Property(color))
    for _ in range(2):
        properties.extend([
            WildCard("Yellow", "Red"),
            WildCard("Orange", "Purple"),
            UberWildCard(),
            UberWildCard()
        ])
    properties.extend([
        WildCard("Green", "Blue"),
        WildCard("Brown", "Light Blue"),
        WildCard("Railroad", "Green"),
        WildCard("Railroad", "Light Blue"),
        WildCard("Railroad", "Utility"),
    ])
    return properties


def construct_rents():
    """Returns a list of Rent instances."""
    rents = []
    for _ in range(2):
        rents.extend([
            Rent("Green", "Blue"),
            Rent("Brown", "Light Blue"),
            Rent("Purple", "Orange"),
            Rent("Railroad", "Utility"),
            Rent("Yellow", "Red")
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