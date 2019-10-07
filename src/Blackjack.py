import random
from src.class_defs.chip_stack import ChipStack
from src.class_defs.cards import Card, CardPile, CardHand
from src.class_defs.players import Player, get_valid_input
from typing import Dict, List, Optional


class BlackJack:
    # =========== Constructors ===========
    def __init__(self):
        # Setup the Players
        self.dealer: Player = Player(name='dealer', chips=ChipStack.from_dealer_stack())
        self.dealer.chips.view_stack()
        self.players: Dict[str, Player] = {'human': Player('human', ChipStack.from_standard_stack())}
        # Setup the Decks
        self.draw_pile: CardPile = CardPile.from_standard_deck()
        self.discard_pile: CardPile = CardPile()

    # =========== Helper Methods ===========
    @staticmethod
    def get_hand_value(player: Player) -> int:
        pass

    @staticmethod
    def is_bust(player: Player) -> bool:
        pass

    @staticmethod
    def is_blackjack(player: Player) -> bool:
        pass

    # =========== Game Actions ===========
    # These are the fundamental operations of a game
    def init_hand(self, buy_in: int=1):
        """This initializes a hand of blackjack with a minimum buy-in of :param buy_in dollars."""
        # zeroth check to make sure buy_in denom is in the standard chip denoms
        buy_in_key = ChipStack.get_chip_string(buy_in)
        if buy_in_key not in ChipStack.get_empty_stack().keys():
            raise KeyError('The buy-in value of \'{}\' is not in the standard denominations'.format(buy_in_key))
        # first check if all players want to buy-in to the hand
        for player_name, player_obj in self.players.items():
            pass

    # =========== Control Flow Actions ===========
    # These are the functions that solicit user input and control the order of game operations

if __name__ == '__main__':
    game = BlackJack()