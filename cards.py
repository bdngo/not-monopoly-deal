import json
from utils import *

# CARDS #
class Card:
    """Card superclass."""
    can_no = False
    can_house = False

    def __repr__(self):
        return "Card"

    def action(self):
        return "This is a placeholder."


class Money(Card):
    """Used to pay off rents and the like.
    Comes in denominations of 1, 2, 3, 4, 5, 10.
    """

    def __init__(self, amount):
        assert amount in DENOMINATIONS
        self.amount = amount

    def __repr__(self):
        return f"Money: {self.amount}M"

    def action(self, player):
        player.bank[self.amount] += 1


class Property(Card):
    can_house = True
    worths = {
        "Brown": 1,
        "Light Blue": 1,
        "Purple": 2,
        "Orange": 2,
        "Red": 3,
        "Yellow": 3,
        "Green": 4,
        "Blue": 4,
        "Railroad": 2,
        "Utility": 2
    }
    def __init__(self, color):
        self.color = color
        self.worth = self.worths[color]

    def __repr__(self):
        return f"Property: {self.color} ({self.worth})"

    def action(self, player):
        player.field[self.color] += 1


class WildCard(Property):
    """Can act as one of two properties. Takes 1 turn to tap."""

    def __init__(self, color1, color2):
        self.color1 = color1
        self.color2 = color2
        self.worth = max(Property.worths[color1], Property.worths[color2])

    def __repr__(self):
        return f"Wild Card: {self.color1}/{self.color2} ({self.worth})"

    def action(self, player):
        tapped = fs_input(
            "Select a color to tap: ",
            "Select a property that exists",
            lambda x: x in [self.color1, self.color2]
        )
        player.field[tapped] += 1


class UberWildCard(Card):
    """Can act as any property."""
    worth = float("inf")

    def __repr__(self):
        return "Über Wild Card: Can act as any property."

    def action(self, player):
        chosen = fs_input(
            "Select a color to tap: ",
            "Select a property that exists",
            lambda x: x in COLORS
        )
        player.field[chosen] += 1
        self.worth = Property.worths[chosen]


class House(Card):
    """Adds 3M to its applied full set."""
    worth = 3

    def __repr__(self):
        return f"House: Adds 3M to the rent of any full set. ({self.worth})"

    def action(self, player):
        print(f"Player {player.order}'s current full sets): ")
        full_sets = filter(full_set, player.field.items())
        for color, amount in full_sets:
            print(f"{color}: {amount}")
        applied = fs_input(
            "Select a property to house: ",
            "Select a full set",
            lambda x: x in [i[0] for i in full_sets]
        )
        player.housed.append(applied)


class Hotel(Card):
    """Adds 4M to its applied housed full set."""
    worth = 4

    def __repr__(self):
        return f"Hotel: Adds 4M to the rent of a housed full set. ({self.worth})"

    def action(self, player):
        print(f"Player {player.order}'s current housed full sets: ")
        full_housed = [i for i in player.field.items
            if player.field(i[0]) in player.housed and full_set(i)]
        for color, amount in full_housed:
            print(f"{color}: {amount}")
        applied = fs_input(
            "Select a property to hotel: ",
            "Select a full set",
            lambda x: player.field[x] > 0 and x in [i[0] for i in full_housed]
        )
        player.hoteled.append(applied)


class PassGo(Card):
    """Draws 2 cards."""
    worth = 1

    def __repr__(self):
        return f"Pass GO: Draw 2 cards. ({self.worth})"

    def action(self, player):
        draw_cards(player, 2)


class Rent(Card):
    """Applies rent to all players."""
    can_no = True
    rents = {
        "Brown": (1, 2),
        "Light Blue": (2, 4, 7),
        "Purple": (1, 2, 4),
        "Orange": (1, 3, 5),
        "Red": (2, 3, 6),
        "Yellow": (2, 4, 6),
        "Green": (2, 4, 7),
        "Blue": (3, 8),
        "Railroad": (1, 2, 3, 4),
        "Utility": (1, 2)
    }
    worth = 1

    def __init__(self, color1, color2):
        self.color1 = color1
        self.color2 = color2

    def __repr__(self):
        return f"Rent: {self.color1}/{self.color2} ({self.worth})"

    def action(self, player):
        with open(PLAYER_PATH, 'r') as f:
            players = json.load(f)

        print(f"Player {player.order}'s current cards on field: ")
        print_dict(player.field)
        chosen_color = fs_input(
            f"Select a property to apply rent to: ({self.color1}/{self.color2})",
            "Please select a property you have",
            lambda x: player.field[x] > 0 and x in [self.color1, self.color2]
        )
        house_tax = 0
        if chosen_color in player.housed and chosen_color in player.hoteled:
            house_tax += 7
        elif chosen_color in player.housed:
            house_tax += 3
        total_properties = player.field[chosen_color]
        payers = [i for i in players if i != player]
        for i in payers:
            i.pay(player, self.rents[chosen_color][total_properties - 1] + house_tax)


class TargetedRent(Rent):
    """Applies rent to a specific player."""
    worth = 3

    def __init__(self):
        return

    def __repr__(self):
        return f"Targeted Rent: Force a player to pay rent on a property. ({self.worth})"

    def action(self, player):
        with open(PLAYER_PATH, 'r') as f:
            players = json.load(f)

        target = players[int(fs_input(
            "Select a player to target: ",
            "Do not select yourself",
            lambda x: int(x) != player.order
        ))]
        print_dict(player.field)
        chosen_color = fs_input(
            "Select a property to apply rent to: ",
            "Please select a property you have",
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
    worth = 3

    def __repr__(self):
        return f"Debt Collector: Force any player to pay you 5M. ({self.worth})"

    def action(self, player):
        with open(PLAYER_PATH, 'r') as f:
            players = json.load(f)

        target = players[int(fs_input(
            "Select a player to target: ",
            "Do not select yourself",
            lambda x: x != player.order
        ))]
        target.pay(player, 5)


class Birthday(Card):
    """Forces all players to pay you 2M."""
    can_no = True
    worth = 2

    def __repr__(self):
        return f"It's My Birthday: Force all players to pay you 2M. ({self.worth})"

    def action(self, player):
        with open(PLAYER_PATH, 'r') as f:
            players = json.load(f)

        payers = [i for i in players if i != player]
        for i in payers:
            i.pay(player, 2)


class SlyDeal(Card):
    """Forces a player to give you one of their properties."""
    can_no = True
    worth = 3

    def __repr__(self):
        return f"Sly Deal: Force any player to give you a property *not* part of a full set. ({self.worth})"

    def action(self, player):
        with open(PLAYER_PATH, 'r') as f:
            players = json.load(f)

        target = players[int(fs_input(
            "Select a player to target: ",
            "Do not select yourself",
            lambda x: int(x) != player.order
        ))]
        not_full = filter(not_full_set, target.field.items())
        print(f"Player {target.order}'s current non-full sets: ")
        for color, amount in not_full:
            print(f"{color}: {amount}")
        stolen_prop = fs_input(
            "Select a property to sly deal: ",
            "Select from the above list",
            lambda x: x in [i[0] for i in not_full]
        )
        target.field[stolen_prop] -= 1
        player.field[stolen_prop] += 1


class ForcedDeal(Card):
    """Forces a player to trade a property with you."""
    can_no = True
    worth = 3

    def __repr__(self):
        return f"Forced Deal: Force any player to trade a property *not* part of a full set with you. ({self.worth})"

    def action(self, player):
        with open(PLAYER_PATH, 'r') as f:
            players = json.load(f)

        target = players[int(fs_input(
            "Select a player to target: ",
            "Do not select yourself",
            lambda x: int(x) != player.order
        ))]
        self_nfull = filter(not_full_set, player.field.items())
        target_nfull = filter(not_full_set, target.field.items())
        print("Your current non-full sets: ")
        for color, amount in self_nfull:
            print(f"{color}: {amount}")
        give_prop = fs_input(
            "Select a property to give: ",
            "Select from the above list",
            lambda x: x in [i[0] for i in self_nfull]
        )
        print(f"Player {target.order}'s non-full sets: ")
        for color, amount in target_nfull:
            print(f"{color}: {amount}")
        take_prop = fs_input(
            "Select a property to take: ",
            "Select from the above list",
            lambda x: x in [i[0] for i in target_nfull]
        )
        player.field[give_prop] -= 1
        target.field[take_prop] -= 1
        player.field[take_prop] += 1
        target.field[give_prop] += 1


class DealBreaker(Card):
    """Takes a full set from a player."""
    can_no = True
    worth = 5

    def __repr__(self):
        return f"Deal Breaker: Steal a full set. ({self.worth})"

    def action(self, player):
        with open(PLAYER_PATH, 'r') as f:
            players = json.load(f)

        target = players[int(fs_input(
            "Select a player to target: ",
            "Do not select yourself",
            lambda x: int(x) != player.order
        ))]
        print(f"Player {target.order}'s full sets: ")
        target_full = filter(full_set, target.field.items())
        for color, amount in target_full:
            print('{0}: {1}'.format(color, amount))
        chosen_set = fs_input(
            "Select a full set: ",
            "Select a *full* set that actually exists",
            lambda x: x in [i[0] for i in target_full]
        )
        player.field[chosen_set] += target.field[chosen_set]
        target.field[chosen_set] = 0
