from __future__ import annotations
from typing import List, Dict, Optional, Callable
from src.class_defs.chip_stack import ChipStack
from src.class_defs.cards import Card

Hand = List[Card]
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
    def __init__(self, name: str='', chips: ChipStack=ChipStack(), hand: Hand=[],
                 action_set: Optional[ActionSet]=None) -> None:
        self.name: str = name
        self.chips: ChipStack = chips  # empty stack
        self.hand: Hand = hand  # empty hand until cards drawn from a deck
        self.action_set: ActionSet = action_set



