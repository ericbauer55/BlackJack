from __future__ import annotations
from enum import Enum
from typing import Dict, List, TypeVar, Generic
T = TypeVar("T")

# Establish Card Primitives
CARD_VALUES = [str(i) for i in range(2, 11)] + ['J', 'Q', 'K', 'A']


class Suit(Enum):
    HEARTS = '♥'
    DIAMONDS = '♦'
    CLUBS = '♣'
    SPADES = '♠'


class Card:
    def __init__(self, value: str, suit: Suit, visible: bool = False) -> None:
        self.value: str = value
        self.suit: Suit = suit
        self.visible: bool = visible

    def __str__(self) -> str:
        if self.visible:
            card_str: str = '[' + self.value + self.suit.value + ']'
            if self.suit == Suit.HEARTS or self.suit == Suit.DIAMONDS:
                return '\033[31m' + card_str + '\033[0m'
            else:
                return '\033[47m\033[30m' + card_str + '\033[0m'
        else:
            return '[??]'


class StandardDeck:
    def __init__(self, visible: bool = False) -> None:
        self.deck: List[Card] = []
        for s in Suit:
            for v in CARD_VALUES:
                self.deck.append(Card(v, s, visible=visible))

    def __str__(self) -> str:
        deck_str: List[str] = []
        for i in range(0, len(self.deck)):
            if i > 0 and i % (len(self.deck) // 4) == 0:
                deck_str.append('\n')
            deck_str.append(self.deck[i].__str__())
        return "".join(deck_str)


if __name__ == '__main__':
    hand = [Card('2', Suit.DIAMONDS, True), Card('J', Suit.CLUBS, True), Card('4', Suit.SPADES)]
    print('Printing a few cards: ')
    [print(c) for c in hand]
    deck = StandardDeck(visible=True)
    print('\n\nPrinting a standard deck: ')
    print(deck)
