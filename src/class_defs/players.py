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
    # =========== Constructors ===========
    def __init__(self, name: str = '', chips: ChipStack = ChipStack(), hand: Optional[Hand] = None,
                 action_set: Optional[ActionSet] = None) -> None:
        self.name: str = name
        self.chips: ChipStack = chips  # empty stack unless otherwise specified
        if hand is None:
            hand = []  # empty hand until cards drawn from a deck
        self.hand: Hand = hand
        if action_set is None:
            action_set = {'actions_basic':  # load only a basic set of instance methods for actions
                              {'view-my-hand': self.view_hand}}
        self.action_set: ActionSet = action_set

    # =========== Player Actions ===========
    def view_hand(self, player: Optional[Player] = None) -> None:
        # if no player is passed to this method, assume 'self' is the player
        # hence 'self' can see all of its cards. This is not necessarily true for 'self' viewing other players' cards
        all_visible = False
        if player is None:
            player = self
            all_visible = True
        print('{0}\'s Hand:')
        for card in player.hand:
            # TODO: Players manage the visibility per Card of a Hand of Cards, it shouldn't be a state of Card
            #if card.visible or all_visible:
            print(card)

