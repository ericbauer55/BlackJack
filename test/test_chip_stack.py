import unittest
import sys

sys.path.insert(1, '../src/class_defs')
from src.class_defs.chip_stack import ChipStack


class MyTestCase(unittest.TestCase):
    # =========== Constructors ===========
    def test_empty_init(self):
        cs = ChipStack(stack=None)
        for key in cs.stack.keys():
            self.assertEqual(cs.stack[key], 0)

    def test_standard_stack_init(self):
        std = {'$1': 25, '$5': 5, '$10': 3, '$20': 1, '$25': 0, '$50': 2, '$100': 1}
        cs = ChipStack.from_standard_stack()
        for key in cs.stack.keys():
            self.assertEqual(cs.stack[key], std[key])

    def test_stack_init_sample(self):
        sample = {'$1': 0, '$5': 5, '$10': 3}
        cs = ChipStack(sample)
        for key in cs.stack.keys():
            self.assertEqual(cs.stack[key], sample.get(key, 0))

    def test_init_from_dealer(self):
        dealer = {'$1': 1000, '$5': 1000, '$10': 1000, '$20': 1000, '$25': 1000, '$50': 1000, '$100': 1000}
        cs = ChipStack.from_dealer_stack()
        self.assertEqual(cs.name, 'dealer')
        for key in cs.stack.keys():
            self.assertEqual(cs.stack[key], dealer[key])

    def test_init_from_amount(self):
        target = {'$1': 1, '$5': 1, '$10': 1, '$20': 0, '$25': 1, '$50': 1, '$100': 1}
        cs = ChipStack.from_amount(amount=191)
        for key in cs.stack.keys():
            self.assertEqual(cs.stack[key], target[key])

    # =========== Helper Methods ===========
    def test_stack_value(self):
        cs = ChipStack.from_standard_stack()
        self.assertEqual(300, cs.stack_value)

    def test_get_stack_value(self):
        cs = ChipStack.from_standard_stack()
        self.assertEqual(300, ChipStack.get_stack_value(cs.stack))

    def test_get_chip_value(self):
        self.assertEqual(5, ChipStack.get_chip_value('$5'))
        self.assertRaises(KeyError, ChipStack.get_chip_value, '##20$')

    def test_get_chip_string(self):
        self.assertEqual('$20', ChipStack.get_chip_string(20))
        self.assertRaises(ValueError, ChipStack.get_chip_string, 11)

    def test_get_empty_stack(self):
        empty = {'$1': 0, '$5': 0, '$10': 0, '$20': 0, '$25': 0, '$50': 0, '$100': 0}
        self.assertEqual(ChipStack.get_empty_stack(), empty)

    def test_filled_stack_from_amount(self):
        target = {'$1': 1, '$5': 1, '$10': 1, '$20': 0, '$25': 1, '$50': 1, '$100': 1}
        temp = ChipStack.filled_stack_from_amount(ChipStack.get_stack_value(target))
        for key in temp.keys():
            self.assertEqual(temp[key], target[key])

    # =========== Chip Operations ===========
    def test_add_chips(self):
        # create an empty stack and add another empty stack
        cs = ChipStack()
        empty_stack = {'$1': 0, '$5': 0, '$10': 0, '$20': 0, '$25': 0, '$50': 0, '$100': 0}
        stack = cs.stack.copy()
        cs._add_chips(empty_stack)
        self.assertEqual(cs.stack, stack)
        self.assertEqual(cs.stack, empty_stack)
        # create an standard stack and add its stack to
        cs2 = ChipStack.from_standard_stack()
        cs._add_chips(cs2.stack)
        self.assertEqual(cs.stack, cs2.stack)

    def test_remove_chips(self):
        # create a std stack and remove another empty stack
        cs = ChipStack.from_standard_stack()
        empty_stack = {'$1': 0, '$5': 0, '$10': 0, '$20': 0, '$25': 0, '$50': 0, '$100': 0}
        std_stack = cs.stack.copy()
        cs._remove_chips(empty_stack)
        self.assertEqual(cs.stack, std_stack)
        self.assertNotEqual(cs.stack, empty_stack)
        # remove a std stack from the std stack to see if empty
        cs._remove_chips(std_stack)
        self.assertEqual(cs.stack, empty_stack)
        # prevent chip quantities from going negative
        # see https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        self.assertRaises(ValueError, cs._remove_chips, std_stack)

    def test_exchange_chips(self):
        cs = ChipStack.from_standard_stack()
        # exchange all 3 $10 chips for 30 $1 chips (all chips)
        cs.exchange_chips('$10', '$1')
        self.assertEqual(cs.stack['$10'], 0)
        self.assertEqual(cs.stack['$1'], 55)
        # exchange all 3 $10 chips for 30 $1 chips (all chips)
        cs.exchange_chips('$50', '$10', 1)
        self.assertEqual(cs.stack['$50'], 1)
        self.assertEqual(cs.stack['$10'], 5)
        # try to exchange 25 $1 chips for 1 $50 and get error
        self.assertRaises(ValueError, cs.exchange_chips, '$1', '$50', 25)
        # exchange all 55 $1 chips for 1 $50 chips (all chips)
        cs.exchange_chips('$1', '$50')
        self.assertEqual(cs.stack['$50'], 2)
        self.assertEqual(cs.stack['$1'], 5)
        # try to exchange chips for bad denominations
        self.assertRaises(KeyError, cs.exchange_chips, '$1', '#50')
        self.assertRaises(KeyError, cs.exchange_chips, '#1', '$50')

    def test_exchange_chips_with_remainders(self):
        cs = ChipStack()
        cs._add_chips({'$25': 3})
        cs.exchange_chips('$25', '$10')
        self.assertEqual(cs.stack['$10'], 7)
        self.assertEqual(cs.stack['$5'], 1)
        cs.stack = ChipStack.get_empty_stack()
        cs._add_chips({'$20': 6})
        cs.exchange_chips('$20', '$50')
        self.assertEqual(cs.stack['$50'], 2)
        self.assertEqual(cs.stack['$20'], 1)

    def test_transfer_chips_all(self):
        cs1 = ChipStack.from_standard_stack()
        cs2 = ChipStack()
        std_stack = cs1.stack.copy()
        empty_stack = cs2.stack.copy()
        # transfer everything from cs1 to cs2
        cs1.transfer_chips(cs2, cs1.stack)
        self.assertEqual(cs1.stack, empty_stack)
        self.assertEqual(cs2.stack, std_stack)
        # transfer emptied stack to cs2 again
        cs1.transfer_chips(cs2, cs1.stack)
        self.assertEqual(cs1.stack, empty_stack)
        self.assertEqual(cs2.stack, std_stack)
        # try to transfer a standard_stack from cs1 to cs2 again
        self.assertRaises(ValueError, cs1.transfer_chips, cs2, std_stack)

    def test_transfer_chips_sample(self):
        sample = {'$1': 0, '$5': 5, '$10': 3}
        cs1 = ChipStack(sample)
        cs2 = ChipStack()
        sample_stack = cs1.stack.copy()
        empty_stack = cs2.stack.copy()
        # transfer everything from cs1 to cs2
        cs1.transfer_chips(cs2, cs1.stack)
        self.assertEqual(cs1.stack, empty_stack)
        self.assertEqual(cs2.stack, sample_stack)
        # transfer everything back
        cs2.transfer_chips(cs1, cs2.stack)
        self.assertEqual(cs1.stack, sample_stack)
        self.assertEqual(cs2.stack, empty_stack)

    def test_add_amount_of_chips(self):
        # Test a simple case
        cs = ChipStack()
        cs.add_amount_of_chips(amount=201)  # sum of all the keys
        self.assertEqual(cs.stack['$1'], 1)  # 201 -> $1: 1 and $5: 40
        self.assertEqual(cs.stack['$5'], 0)  # 200 -> $5: 0 and $10: 20
        self.assertEqual(cs.stack['$10'], 0)  # 200 -> $10: 0 and $20: 10
        self.assertEqual(cs.stack['$20'], 0)  # 200 -> $20: 0 and $25: 8
        self.assertEqual(cs.stack['$25'], 0)  # 200 -> $25: 0 and $50: 4
        self.assertEqual(cs.stack['$50'], 0)  # 200 -> $50: 0 and $100: 2
        self.assertEqual(cs.stack['$100'], 2)
        # Test a case when adding the remainder of an exchange
        # NOTE: once the amount has been deposited into the lowest chip denoms, do not sort into higher as side effect
        cs = ChipStack({'$5': 0, '$10': 7, '$25': 0})
        remainder = 5
        cs.add_amount_of_chips(remainder)
        self.assertEqual(cs.stack['$1'], 0)  # 5 of $1 goes to 1 of $5
        self.assertEqual(cs.stack['$5'], 1)  # stays
        self.assertEqual(cs.stack['$10'], 7)
        self.assertEqual(cs.stack['$20'], 0)
        self.assertEqual(cs.stack['$25'], 0)
        self.assertEqual(cs.stack['$50'], 0)
        self.assertEqual(cs.stack['$100'], 0)


    def test_transfer_amount_of_chips(self):
        pass

    def test_sort_stack(self):
        pass

if __name__ == '__main__':
    unittest.main()
