from __future__ import annotations
from enum import Enum
from typing import Dict, List, TypeVar, Generic, Optional
import random
T = TypeVar("T")

# Establish Card Primitives
CARD_VALUES = [str(i) for i in range(2, 11)] + ['J', 'Q', 'K', 'A']


class Suit(Enum):
    HEARTS: Suit = '♥'
    DIAMONDS: Suit = '♦'
    CLUBS: Suit = '♣'
    SPADES: Suit = '♠'


class Card:
    # =========== Constructors ===========
    def __init__(self, value: str, suit: Suit, visible: bool = False) -> None:
        # TODO: refactor card.value to be card.rank
        self.value: str = value
        self.suit: Suit = suit
        self.visible: bool = visible

    # =========== Helper Methods ===========
    @property
    def name(self) -> str:
        """This property wraps to_string but forces complete visibility"""
        return self.to_string(visible=True)

    def to_string(self, visible: bool = False) -> str:
        if visible:
            return self.__str__()
        else:
            return '[??]'

    def __str__(self) -> str:
        card_str: str = '[' + self.value + self.suit.value + ']'
        if self.suit == Suit.HEARTS or self.suit == Suit.DIAMONDS:
            return '\033[31m' + card_str + '\033[0m'
        else:
            return '\033[47m\033[30m' + card_str + '\033[0m'


class CardHand:
    # =========== Constructors ===========
    def __init__(self, card_list: Optional[List[Card]] = None):
        if card_list is None:
            card_list = []
        self.hand: List[Card] = card_list

    # =========== Helper Methods ===========
    def get_card_index(self, card_name: str) -> int:
        """Performs a linear search for a card with matching card name or throws error if not found"""
        for i, card in enumerate(self.hand):
            if card.name == card_name:
                return i
        # if card_name not found, raise index error
        raise IndexError('No card with name "{}" was found in the hand'.format(card_name))

    def to_string(self, all_visible: bool = False) -> str:
        """
        This returns a joined string of the cards, printed with their respective visibility status
        unless all_visible = True, in which case all of the cards will show their face-up value
        """
        if len(self.hand) == 0:
            return '<empty hand>'
        return ''.join([card.to_string(visible=(all_visible or card.visible)) for card in self.hand])

    # =========== Hand Operations ===========
    def add_card(self, card: Card) -> None:
        self.hand.append(card)

    def remove_card(self, card_name: str) -> Card:
        index = self.get_card_index(card_name)
        return self.hand.pop(index)

    def transfer_cards(self, card_names: List[str], other_hand: CardHand) -> None:
        for name in card_names:
            other_hand.add_card(self.remove_card(name))

class Stack(Generic[T]):
    # =========== Constructors ===========
    def __init__(self, item_list: Optional[List[T]] = None) -> None:
        if item_list is None:
            self.stack: Optional[List[T]] = []
        else:
            self.stack: Optional[List[T]] = item_list

    # =========== Stack Operations ===========
    def pop(self) -> T:
        return self.stack.pop()

    def push(self, item: T) -> None:
        self.stack.append(item)

    def peak(self) -> T:
        return self.stack[-1]

    @property
    def n_items(self) -> int:
        return len(self.stack)


class CardPile(Stack[Card]):
    # =========== Constructors ===========
    def __init__(self, item_list: Optional[List[T]] = None) -> None:
        super(CardPile, self).__init__(item_list)

    @classmethod
    def from_standard_deck(cls) -> CardPile:
        deck: List[Card] = []
        for s in Suit:
            for v in CARD_VALUES:
                deck.append(Card(v, s, visible=False))
        return cls(deck)

    # =========== Helper Methods ===========
    def __str__(self):
        return self.peak().__str__().ljust(self.n_items - 1, ']')

    # =========== Pile Operations ===========
    def draw(self) -> Card:
        return self.pop()

    def add(self, card: Card, to_bottom: bool = False) -> None:
        if to_bottom:
            self.stack.insert(0, card)
        else:
            self.push(card)

    def shuffle(self) -> None:
        random.shuffle(self.stack)  # self.stack is a list of cards


if __name__ == '__main__':
    main_hand = CardHand()
    print(main_hand.to_string())
    hand = CardHand([Card('2', Suit.DIAMONDS, True), Card('J', Suit.CLUBS, True), Card('4', Suit.SPADES)])
    print('Printing a hand of cards: ')
    print(hand.to_string())
    pile = CardPile.from_standard_deck()
    print('\n\nPrinting a standard pile: ')
    print(pile)
    print('Drawing a few times into hand...')
    for _ in range(1, 15):
        hand.add_card(pile.draw())
    print('\n\nPrinting the new pile: ')
    print(pile)
    print('Printing a hand of cards: ')
    print(hand.to_string(all_visible=True))
