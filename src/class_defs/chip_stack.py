from __future__ import annotations
from typing import Dict, Optional, List


class ChipStack:
    # =========== Class Attributes ===========
    CHIP_COLORS: Dict[str, str] = {'$1': '', '$5': '\033[31m', '$10': '\033[34m', '$20': '\033[37m',
                                   '$25': '\033[32m', '$50': '\033[33m', '$100': '\033[30m'}
    CHIP_CHAR = '▐'

    # =========== Constructors ===========
    def __init__(self, stack: Optional[Dict[str, int]] = None, name: str = '') -> None:
        self.name = name  # name of the stack
        self.stack: Dict[str, int] = {'$1': 0, '$5': 0, '$10': 0, '$20': 0, '$25': 0, '$50': 0, '$100': 0}
        if stack is not None:
            self._add_chips(stack)

    @classmethod
    def from_standard_stack(cls) -> ChipStack:
        """Initializes the chip stack for a $300 starting value"""
        return cls({'$1': 25, '$5': 5, '$10': 3, '$20': 1, '$25': 0, '$50': 2, '$100': 1})

    @classmethod
    def from_dealer_stack(cls) -> ChipStack:
        """Initializes the chip stack for a high number of chips to act at the House"""
        return cls({'$1': 1000, '$5': 1000, '$10': 1000, '$20': 1000, '$25': 1000, '$50': 1000, '$100': 1000}, 'dealer')

    # =========== Helper Methods ===========
    @property
    def stack_value(self) -> int:
        """This property gets the total value of the chips in the stack"""
        chip_sum = 0
        for denom, quantity in self.stack.items():
            chip_sum += ChipStack._get_chip_value(denom) * quantity
        return chip_sum

    def view_stack(self, tabular: bool = False) -> None:
        if not tabular and self.name != 'dealer':  # dealer should always be printed tabularly
            output: List[str] = []
            for denom, qty in self.stack.items():
                temp = '{0} :{1}'.format(denom.rjust(4), ChipStack.CHIP_COLORS[denom]) + \
                       ChipStack.CHIP_CHAR * qty + '\033[00m' + ' ({} chips)'.format(qty)
                output.append(temp)
            print('\n'.join(output))
        else:
            print(self)

    def __str__(self) -> str:
        # Create a column header row first in order to format the others with real column widths
        rows: List[List[str]] = [['| Denom ', '| Quantity ', '| Subtotal ', '|']]
        col_widths: List[int] = [len(col) for col in rows[0]]
        h_line = ['+', '-' * (col_widths[0] - 1), '+', '-' * (col_widths[1] - 1), '+', '-' * (col_widths[2] - 1), '+']
        hb_line = ['+', '=' * (col_widths[0] - 1), '+', '=' * (col_widths[1] - 1), '+', '=' * (col_widths[2] - 1), '+']
        # Create the real data rows
        for denom, qty in self.stack.items():
            rows.append(h_line) # insert a filler horizontal line between each data row
            rows.append(['|', denom.center(col_widths[0]-1), '|', '{}'.format(qty).center(col_widths[1]-1), '|',
                         '${}'.format(qty * ChipStack._get_chip_value(denom)).center(col_widths[2]-1), '|'])
        # finish wrapping the table in good formatting & give it a label
        rows[1] = hb_line
        rows.append(hb_line)
        rows.insert(0, hb_line)
        #title = 'ChipStack{0}'.format(' ' + self.name if self.name != '' else self.name)
        #rows.insert(0, ['|\033[01m', title.center(len(h_line)-2), '\033[00m|'])
        #rows.insert(0, hb_line)
        # join all of the row elements together and return it
        return '\n'.join(["".join(row) for row in rows])

    @staticmethod
    def _get_chip_value(denom: str) -> int:
        """returns the integer value associated with a chip denomination"""
        return int(denom.strip('$'))

    @staticmethod
    def _get_chip_string(denom: str) -> int:
        """returns the denomination value string associated with a chip integer value"""
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

    def exchange_chips(self, denom1: str, denom2: str, quantity: int = -1) -> None:
        """
        This function exchanges a quantity of denom1 for denom2
        Transaction occurs within a single ChipStack object
        """
        denom1_value, denom2_value = ChipStack._get_chip_value(denom1), ChipStack._get_chip_value(denom2)

        if quantity == -1:
            # exchange ALL chips of denom1 for denom2
            quantity = self.stack[denom1]  # get number of denom1 chips
        # quantity * denom1 = chip_num * denom2
        chip_num = (denom1_value / denom2_value) * quantity
        if chip_num < 1.0:
            raise ValueError('You cannot exchange "{0}" for fractional "{1}"'.format(denom1, denom2))

        add_stack: Dict[str, int] = {denom2: int(chip_num)}
        remove_stack: Dict[str, int] = {denom1: int(chip_num) * denom2_value // denom1_value}
        self._add_chips(add_stack)
        self._remove_chips(remove_stack)

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
    cs = ChipStack.from_standard_stack()
    cs.view_stack(tabular=True)
    print('-' * 50)
    cs.exchange_chips('$10', '$1')
    cs.view_stack(tabular=False)
    print('-' * 50)
