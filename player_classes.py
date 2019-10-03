from __future__ import annotations
from typing import Dict, List, Callable, Optional


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


class ChipStack:
    CHIP_COLORS: Dict[str, str] = {'$1': '', '$5': '\033[31m', '$10': '\033[34m', '$20': '\033[37m',
                                   '$25': '\033[32m', '$50': '\033[33m', '$100': '\033[30m'}

    def __init__(self) -> None:
        self.stack: Dict[str, int] = {'$1': 0, '$5': 0, '$10': 0, '$20': 0, '$25': 0, '$50': 0, '$100': 0}

    @classmethod
    def from_standard_stack(cls) -> ChipStack:
        x: ChipStack = cls.__init__()
        x.stack = {'$1': 25, '$5': 5, '$10': 3, '$20': 1, '$25': 0, '$50': 2, '$100': 1}
        return x

    # =========== Visualization ===========
    @property
    def stack_value(self) -> int:
        """This property gets the total value of the chips in the stack"""
        chip_sum = 0
        for denomination, quantity in self.stack.items():
            chip_sum += int(denomination.strip('$')) * quantity
        return chip_sum

    def view_stack(self, tabular: bool = False) -> None:
        if not tabular:
            print(self)
        else:
            pass

    def __str__(self) -> str:
        pass

    # =========== Chip Operations ===========
    def _add_chips(self, added_stack: Dict[str, int]) -> None:
        """
        This adds all of the quantities of valid denominations from added_stack to self.stack
        Valid denominations are handled by iterating over self.stack keys and using .get(key, 0) to make sure its valid
        """
        for denomination, quantity in self.stack.items():
            # for every chip value $1 to $100, check if that is in the added_stack.
            # if so add its quantity, if not add 0
            self.stack[denomination] += added_stack.get(denomination, 0)

    def __add__(self, other):
        """This overloads the add function for adding two ChipStack objects to each other"""
        self._add_chips(other.stack)

    def _remove_chips(self, removed_stack: Dict[str, int]) -> None:
        """
        This removes all of the quantities of valid denominations from added_stack to self.stack
        Valid denominations are handled by iterating over self.stack keys and using .get(key, 0) to make sure its valid
        """
        for denomination, quantity in self.stack.items():
            # for every chip value $1 to $100, check if that is in the added_stack.
            # if so add its quantity, if not add 0
            self.stack[denomination] -= removed_stack.get(denomination, 0)

    def __sub__(self, other):
        """This overloads the add function for subtracting two ChipStack objects to each other"""
        self._remove_chips(other.stack)

    def exchange_chips(self, denom1: str, denom2: str, quantity: int = -1) -> bool:
        """This function exchanges a quantity of denom1 for the exchange_rate*quantity of denom2 """
        denom1_value, denom2_value = int(denom1.strip('$')), int(denom2.strip('$'))
        if denom2_value > denom1_value:
            print('You cannot exchange "{0}" for fractional "{1}"'.format(denom1, denom2))
            return False
        exchange_rate: int = denom2_value / denom1_value  # ratio of denom2:denom1
        if quantity == -1:
            # exchange ALL chips of denom1 for denom2
            quantity = self.stack[denom1]  # get number of denom1 chips
        add_stack: Dict[str, int] = {denom2: int(exchange_rate * quantity)}
        remove_stack: Dict[str, int] = {denom1: quantity}
        self._add_chips(add_stack)
        self._remove_chips(remove_stack)
        return True

class Player:
    def __init__(self) -> None:
        self.chips: ChipStack = ChipStack()

