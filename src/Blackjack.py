import random
from src.class_defs.chip_stack import ChipStack
from src.class_defs.cards import Card, CardPile, CardHand
from src.class_defs.players import Player, get_valid_input
from typing import Dict, List, Optional


class BlackJack:
    # =========== Constructors ===========
    def __init__(self):
        self.dealer = Player(name='dealer', chips=ChipStack.from_dealer_stack())
        self.dealer.chips.view_stack()

    # =========== Helper Methods ===========

    # =========== Game Actions ===========

    # =========== Control Flow Actions ===========


if __name__ == '__main__':
    game = BlackJack()