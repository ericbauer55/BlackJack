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
        self.players: Dict[str, Dict[str, object]] = {'Human':
                                                          {'player': Player('human', ChipStack.from_standard_stack()),
                                                           'pot': ChipStack()}}  # pot could point to a common pot obj.
        # Setup the Decks
        self.draw_pile: CardPile = CardPile.from_standard_deck()
        self.discard_pile: CardPile = CardPile()

    # =========== Helper Methods ===========

    # =========== Game Actions ===========
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


if __name__ == '__main__':
    game = BlackJack()