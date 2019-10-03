from typing import Dict, List, Callable, Optional

CHIP_COLORS: Dict[str, str] = {'$1': '', '$5': '\033[31m', '$10': '\033[34m', '$20': '\033[37m',
                               '$25': '\033[32m', '$50': '\033[33m', '$100': '\033[30m'}


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
    def __init__(self) -> None:
        self.chips: Dict[str, int] = {'$1': 0, '$5': 0, '$10': 0, '$20': 0, '$25': 0, '$50': 0, '$100': 0}

    @property
    def chip_value(self) -> int:
        chip_sum = 0
        for denomination, quantity in self.chips.items():
            chip_sum += int(denomination.strip('$')) * quantity
        return chip_sum