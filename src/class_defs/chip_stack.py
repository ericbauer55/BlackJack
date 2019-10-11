from __future__ import annotations
from typing import Dict, Optional, List
from math import floor, ceil


class ChipStack:
    # =========== Class Attributes ===========
    CHIP_COLORS: Dict[str, str] = {'$1': '', '$5': '\033[31m', '$10': '\033[34m', '$20': '\033[37m',
                                   '$25': '\033[32m', '$50': '\033[33m', '$100': '\033[30m'}
    CHIP_CHAR = '▐'

    CHIP_VALUES: Dict[str, int] = {'$1': 1, '$5': 5, '$10': 10, '$20': 20, '$25': 25, '$50': 50, '$100': 100}

    # =========== Constructors ===========
    def __init__(self, stack: Optional[Dict[str, int]] = None, name: str = '') -> None:
        self.name = name  # name of the stack
        self.stack: Dict[str, int] = {'$1': 0, '$5': 0, '$10': 0, '$20': 0, '$25': 0, '$50': 0, '$100': 0}
        if stack is not None:
            self._add_chips(stack)

    @classmethod
    def from_amount(cls, amount: int = 211) -> ChipStack:
        return cls(stack=ChipStack.get_chips_from_amount(amount))

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
        return ChipStack.get_stack_value(self.stack)

    @staticmethod
    def get_stack_value(stack_dict: Dict[str, int]) -> int:
        """This returns the value of all chip denoms and quantities in an input stack dictionary"""
        chip_sum = 0
        for denom, quantity in stack_dict.items():
            chip_sum += ChipStack.get_chip_value(denom) * quantity
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
                         '${}'.format(qty * ChipStack.get_chip_value(denom)).center(col_widths[2]-1), '|'])
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
    def get_chip_value(denom: str) -> int:
        """returns the integer value associated with a chip denomination"""
        # TODO: definitely refactor into dictionary lookup?
        return int(denom.strip('$'))

    @staticmethod
    def get_chip_string(denom_value: int) -> str:
        """returns the denomination value string associated with a chip integer value"""
        return '${}'.format(denom_value)

    @staticmethod
    def get_empty_stack() -> Dict[str, int]:
        """
        This helper function helps the caller see the expected chip dictionary.
        Accordingly, it can be used first to create the chip stack dictionary to later initialize a ChipStack object
        """
        return {'$1': 0, '$5': 0, '$10': 0, '$20': 0, '$25': 0, '$50': 0, '$100': 0}

    @staticmethod
    def get_chips_from_amount(amount: int, denom_pref: str = 'high') -> Dict[str, int]:
        """
        This function returns a dictionary of chip denoms and their quantities based on an input dollar amount.
        NOTE: this might be a knapsack problem
        :param amount: the dollar amount to convert into chips
        :param denom_pref: either 'high' or 'low'. If 'high' the chips returned will be as high of
        denominations as possible. If 'low', all chips will be converted in $1 chips.
        :return: dictionary of denomination keys and chip quantities as values
        """
        # TODO: consider changing name to get_chips_from_payout or add_chips_from_amount
        temp = ChipStack()  # get an empty chipstack
        if amount == 0:
            return temp.stack

        temp._add_chips({'$1': amount})
        if denom_pref == 'low':
            return temp.stack
        denoms = list(temp.stack.keys())
        for i in range(1, len(denoms)):
            try:
                # exchange all of a lower denom for the next higher denom
                temp.exchange_chips(denom1=denoms[i-1], denom2=denoms[i])
            except ValueError:
                # do nothing since should only occur when converting from $50: 1 to $100: 0
                pass
        return temp.stack

    def get_chips_for_amount(self, amount: int) -> Dict[str, int]:
        """
        This function is typically used to return a stack dictionary needed to place a bet of :param amount

        If the amount requires chips of lower denoms than is available, higher denom chips will be exchanged for lower
        """
        # TODO: consider changing name remove_chips_for_bet or remove_chips_for_amount
        output_dict: Dict[str, int] = ChipStack.get_empty_stack()

        for denom, qty in self.stack.items():
            # determine number of "denom" chips to put towards reducing amount to 0
            N = min(floor(amount/ChipStack.get_chip_value(denom)), qty)
            output_dict[denom] += N
            amount -= N * ChipStack.get_chip_value(denom)  # reduce amount left to consider
        if amount > 0:  # if there is still some amount left, exchange some higher denom chips for $1 to cover it
            # find the first lowest chip that can cover the remainder AND has uncommitted chips
            exchange_exists: int = False
            for denom, value in self.CHIP_VALUES:
                uncommitted_quantity: int = self.stack[denom] - output_dict[denom]
                if uncommitted_quantity > 0 and value > amount:
                    self.exchange_chips(denom, '$1')
                    exchange_exists = True
                    # finish the transfer
                    N = amount
                    output_dict['$1'] += N
                    amount -= N  # reduce amount left to consider
            # if there is no exchange available to cover the remainder, throw error
            if not exchange_exists:
                raise ValueError('The remaining amount {} cannot be exchanged for.'.format(amount))

        return output_dict

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

    def exchange_chips(self, denom1: str, denom2: str, N1: int = -1) -> None:
        """
        This function exchanges a quantity of denom1 for denom2. Sometimes, the exchange rate and N1 quantity will not
        exchange without a remainder. For example, 2x $25 chips converts to 2x $20 chips with $10 remainder. Both of
        the $25 chips must be exchanged for the maximum number of $20 chips, but the remainder will be converted to a
        set of chips with the highest denominations using the get_chips_from_amount function.
        -The amount of denom2 chips gained is N2 = floor((denom1/denom2) * N1)
        -The required denom1 chips is    deltaN1 = ceiling((denom2/denom1) * N2)
        -The amount of denom1 chips left is   N1' = N1 - deltaN1
        -The remainder amount afterwards is    R = floor(((denom1/denom2)*deltaN1 - N2) * denom2)

        Example 1: denom1=$25, N1=3 exchanged for denom2=$10 gets N2 chips
            N2 = floor(($25/$10) * 3) = floor(7.5) =  7 chips of denom2 gained
            deltaN1 = ceiling(($10/$25) * 7) = ceiling(2.8) = 3 chips of denom1 used
            N1' = 3 - 3 = 0 chips of denom1 left
            R = floor((($25/$10)*3 - 7) * $10) = floor((7.5 - 7) * $10) = floor(0.5 * $10) = $5
                This remainder is first converted to $1 and then exchanged upwards for 1 of the $5 chips

        NOTE: Transaction occurs within a single ChipStack object, and doesn't transfer between stacks
        """
        denom1_value, denom2_value = ChipStack.get_chip_value(denom1), ChipStack.get_chip_value(denom2)
        # compute the quantities of exchanged chips and remainder value
        if N1 == -1:
            # exchange ALL chips of denom1 for denom2
            N1 = self.stack[denom1]  # get number of denom1 chips
        N2: int = floor((denom1_value/denom2_value) * N1)  # number of denom2 chips gained
        deltaN1: int = ceil((denom2_value/denom1_value) * N2)  # number of denom1 chips used
        R: int = floor(((denom1_value/denom2_value) * deltaN1 - N2) * denom2_value)  # remainder value
        if N2 < 1.0:
            raise ValueError('You cannot exchange "{0}" for fractional "{1}"'.format(denom1, denom2))
        # add and remove the exchanged quantities
        add_stack: Dict[str, int] = {denom2: N2}
        remainder_stack: Dict[str, int] = ChipStack.get_chips_from_amount(R)
        remove_stack: Dict[str, int] = {denom1: deltaN1}
        self._add_chips(add_stack)
        self._add_chips(remainder_stack)
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
    cs = ChipStack.from_amount()
    cs.view_stack(tabular=True)
    print('-' * 50)
    cs.exchange_chips('$10', '$1')
    cs.view_stack(tabular=False)
    print('-' * 50)
