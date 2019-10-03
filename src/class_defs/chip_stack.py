from __future__ import annotations
from typing import Dict, Optional


class ChipStack:
    # =========== Class Attributes ===========
    CHIP_COLORS: Dict[str, str] = {'$1': '', '$5': '\033[31m', '$10': '\033[34m', '$20': '\033[37m',
                                   '$25': '\033[32m', '$50': '\033[33m', '$100': '\033[30m'}
    CHIP_CHAR = '▐'

    # =========== Constructors ===========
    def __init__(self, stack: Optional[Dict[str, int]] = None) -> None:
        self.stack: Dict[str, int] = {'$1': 0, '$5': 0, '$10': 0, '$20': 0, '$25': 0, '$50': 0, '$100': 0}
        if stack is not None:
            self._add_chips(stack)

    @classmethod
    def from_standard_stack(cls) -> ChipStack:
        """Initializes the chip stack for a $300 starting value"""
        return cls({'$1': 25, '$5': 5, '$10': 3, '$20': 1, '$25': 0, '$50': 2, '$100': 1})

    # =========== Helper Methods ===========
    @property
    def stack_value(self) -> int:
        """This property gets the total value of the chips in the stack"""
        chip_sum = 0
        for denom, quantity in self.stack.items():
            chip_sum += ChipStack._get_chip_value(denom) * quantity
        return chip_sum

    def view_stack(self, tabular: bool = False) -> None:
        if not tabular:
            print(self)
        else:
            for denom, qty in self.stack.items():
                x = 'Denom {0} has {1} chips worth ${2}'.format(denom, qty, ChipStack._get_chip_value(denom) * qty)
                print(x)

    def __str__(self) -> str:
        pass

    @staticmethod
    def _get_chip_value(denom: str) -> int:
        return int(denom.strip('$'))

    @staticmethod
    def get_empty_stack() -> Dict[str, int]:
        """
        This helper function helps the caller see the expected chip dictionary.
        Accordingly, it can be used first to create the chip stack dictionary to later initialize a ChipStack object
        """
        return {'$1': 0, '$5': 0, '$10': 0, '$20': 0, '$25': 0, '$50': 0, '$100': 0}

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

    def _remove_chips(self, removed_stack: Dict[str, int]) -> None:
        """
        This removes all of the quantities of valid denominations from added_stack to self.stack
        Valid denominations are handled by iterating over self.stack keys and using .get(key, 0) to make sure its valid
        """
        for denomination, quantity in self.stack.items():
            # for every chip value $1 to $100, check if that is in the added_stack.
            # if so add its quantity, if not add 0
            if self.stack[denomination] - removed_stack.get(denomination, 0) < 0:
                raise ValueError('The quantity of {0} chips cannot go negative'.format(denomination))
            self.stack[denomination] -= removed_stack.get(denomination, 0)

    def exchange_chips(self, denom1: str, denom2: str, quantity: int = -1) -> bool:
        """
        This function exchanges a quantity of denom1 for the exchange_rate*quantity of denom2
        Transaction occurs within a single ChipStack object
        """
        # TODO: if 25 $1 chips want to be exchanged for 1 $25 chip, this should be allowed
        denom1_value, denom2_value = ChipStack._get_chip_value(denom1), ChipStack._get_chip_value(denom2)
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

    def transfer_chips(self, destination: ChipStack, transfer_stack: Dict[str, int]) -> bool:
        """
        This function transfers the chip quantities specified in :param transfer_stack to the destination ChipStack
        """
        transfer_success: bool = True
        # ensure that input is a copy so that state changes during removal doesn't influence add
        transfer_stack = transfer_stack.copy()
        try:
            self._remove_chips(transfer_stack)
        except ValueError:
            raise
        else:
            destination._add_chips(transfer_stack)
        return transfer_success


if __name__ == '__main__':
    cs = ChipStack(stack=None)
    cs.stack = {'$1': 25, '$5': 5, '$10': 3, '$20': 1, '$25': 0, '$50': 2, '$100': 1}
    cs.view_stack(tabular=True)
    print('-' * 50)
    cs.exchange_chips('$10', '$1')
    cs.view_stack(tabular=True)
    print('-' * 50)
