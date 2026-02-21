import random
from queue import SimpleQueue

from statemachine import State, StateMachine

from cards import Card
from constructors import construct_deck
from player import Player

INITIAL_HAND_SIZE = 5


class Game(StateMachine):
    """NMD game engine."""

    idle = State(initial=True)
    waiting_for_player = State()
    done = State(final=True)

    start_game = idle.to(waiting_for_player)
    player_turn_end = waiting_for_player.to.itself()
    player_wins = waiting_for_player.to(done)

    def __init__(self, players: list[Player]) -> None:
        self.players = players
        self.deck = construct_deck()
        self.discards: list[Card] = []

        self.player_queue: SimpleQueue[Player] = SimpleQueue()
        self.current_player: Player | None = None
        super().__init__()

    def on_start_game(self) -> None:
        """Deal out the initial hands."""
        random.shuffle(self.deck)
        for _ in range(INITIAL_HAND_SIZE):
            for p in self.players:
                card = self.deck.pop()
                p.hand.append(card)

        for p in self.players:
            self.player_queue.put(p)

    def on_enter_waiting_for_player(self) -> None:
        """Proceed to the next player."""

        self.current_player = self.player_queue.get()
        self.current_player.draw(self.deck)

    def on_player_turn_end(self) -> None:
        """End the current player's turn."""

        if self.current_player is not None:
            self.player_queue.put(self.current_player)
