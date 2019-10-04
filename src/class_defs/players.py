from __future__ import annotations
from typing import List, Dict, Optional, Callable
from src.class_defs.chip_stack import ChipStack
from src.class_defs.cards import Card, CardPile, CardHand

ActionSet = Dict[str, Dict[str, Callable]]

def get_valid_input(input_prompt: str, valid_input_list: List[str]) -> str:
    """
    This generically prompts the user to input a string that is in the discrete valid list
    :param input_prompt: string to prompt the user to input with
    :param valid_input_list: discrete list of valid string inputs
    :return: returns a valid item from the valid_input_list parameter
    """
    x = input(input_prompt)
    if x in valid_input_list:
        return x
    else:
        print("Input {0} is invalid.".format(x))
        return get_valid_input(input_prompt, valid_input_list)  # try again


class Player:
    # =========== Constructors ===========
    def __init__(self, name: str = '', chips: Optional[ChipStack] = None, hand: Optional[CardHand] = None,
                 action_set: Optional[ActionSet] = None) -> None:
        self.name: str = name
        if chips is None:
            chips = ChipStack()
        if hand is None:
            hand = CardHand()
        self.chips: ChipStack = chips  # empty stack unless otherwise specified
        self.hand: CardHand = hand
        if action_set is None:
            action_set = {'actions_basic':  # load only a basic set of instance methods for actions
                              {'view-my-hand': self.view_hand}}
        self.action_set: ActionSet = action_set

    # =========== Player Actions ===========
    def view_hand(self, player: Optional[Player] = None, all_visible: bool = False) -> None:
        # TODO: Players manage the visibility per Card of a Hand of Cards, it shouldn't be a state of Card
        # if no player is passed to this method, assume 'self' is the player
        if player is None:
            player = self
        print('{0} viewing {1}\'s Hand:'.format(self.name, player.name))
        print(player.hand.to_string(all_visible=all_visible))

    def draw(self, card_pile: CardPile, n_cards: int = 1, all_visible: bool = False) -> None:
        for _ in range(1, n_cards + 1):
            drawn = card_pile.draw()
            drawn.visible = all_visible
            self.hand.add_card(drawn)

    def discard(self, discard_pile: CardPile, card_names: List[str]) -> None:
        for name in card_names:
            discard_pile.add(self.hand.remove_card(name))


if __name__ == '__main__':
    deck = CardPile.from_standard_deck()
    deck.shuffle()
    py1 = Player('Player 1')
    py2 = Player('Player 2')
    # print each player's hand out
    print('Initial Player Hands: ')
    py1.view_hand(all_visible=True)
    py2.view_hand(all_visible=True)
    print('\nDeck:', deck)

    # draw some cards into each Hand
    py1.draw(deck, n_cards=5)
    py2.draw(deck, n_cards=5)
    print('\nPlayer Hands After Drawing: ')
    py1.view_hand(all_visible=True)
    py2.view_hand(all_visible=True)
    print('\nDeck:', deck)
