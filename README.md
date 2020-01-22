Python program simulating the game _Monopoly Deal_ by Hasbro and sold by Cartamundi.

# Modifications from original game:

* All properties are worth the same amount of cash.
* Properties of the same color are equal (i.e. no names for properties).
* Priority for rent goes money first, then property.
* Giving up 1 property ends the rent.
* Wild cards are treated as normal properties as soon as they are played (i.e. tapping WCs not possible).

# How to Download and Play:

1. Download `nmd.py`.
2. Run the command
```bash
python3 [-i] nmd.py
```
in your terminal. The `-i` flag can be used for testing.

3. Enjoy!

# Cards

Card Name | Function | Notes
--------- | -------- | -----
Money | Works as a buffer for Rent and the like.
Property | Comes in many different colors, 3 full sets are required to win. | There are no names for the properties, only colors.
Wild Card | Can be "tapped" as any color as described on the set. | Can not be tapped after played once as of late.
Über Wild Card | Can be set as any color card. | Once played, color cannot be changed.
House | Adds 3M to the rent of any _full_ set.
Hotel | Adds 4M to the rent of any _full, housed_ set.
Pass GO | Draws 2 cards to your hand.
Rent | Forces all player to pay you the amount specified on the color. | Money is prioritized over properties, and giving up 1 property ends the rent.
Targeted Rent | Same as Rent, but can be applied as any color and is targeted.
Debt Collector | Forces any player to pay you 5M.
It's My Birthday | Forces all players to pay you 2M.
Sly Deal | Allows you to take a property _not_ part of a full set from another player.
Forced Deal | Allows you to trade a property with another player.
Deal Breaker | Allows you to steal a full set from another player.

# Rules:

1. Each player draws 5 cards from the pile.
2. On their turn, a player draws 2 cards. They can then play up to 3 cards, whether it be money or a property.
3. The goal is to get 3 fulls sets of properties.

# TODO:

- [ ] add Just Say No's
- [ ] have a cleaner win condition
- [ ] allow tapping of wild cards
- [x] allow "selling" of properties and actions

