from __future__ import annotations
from typing import List, Dict, Optional, Callable
from src.class_defs.chip_stack import ChipStack
from src.class_defs.cards import Card, StandardDeck, CardPile, CardHand

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
    def __init__(self, name: str = '', chips: ChipStack = ChipStack(), hand: CardHand = CardHand(),
                 action_set: Optional[ActionSet] = None) -> None:
        self.name: str = name
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
        print('{0}\'s Hand:')
        print(player.hand.to_string(all_visible=all_visible))

