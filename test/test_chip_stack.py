import unittest
import sys

sys.path.insert(1, '../src/class_defs')
from chip_stack import ChipStack


class MyTestCase(unittest.TestCase):
    def test_empty_init(self):
        cs = ChipStack(stack=None)
        for key in cs.stack.keys():
            self.assertEqual(cs.stack[key], 0)

    def test_standard_stack_init(self):
        std = {'$1': 25, '$5': 5, '$10': 3, '$20': 1, '$25': 0, '$50': 2, '$100': 1}
        cs = ChipStack.from_standard_stack()
        for key in cs.stack.keys():
            self.assertEqual(cs.stack[key], std[key])

    def test_get_stack_value(self):
        cs = ChipStack.from_standard_stack()
        self.assertEqual(300, cs.stack_value)

    def test_get_chip_value(self):
        self.assertEqual(5, ChipStack._get_chip_value('$5'))

    def test_get_empty_stack(self):
        empty = {'$1': 0, '$5': 0, '$10': 0, '$20': 0, '$25': 0, '$50': 0, '$100': 0}
        self.assertEqual(ChipStack.get_empty_stack(), empty)

    def test_add_chips(self):
        # create an empty stack and add another empty stack
        cs = ChipStack()
        empty = {'$1': 0, '$5': 0, '$10': 0, '$20': 0, '$25': 0, '$50': 0, '$100': 0}
        stack = cs.stack
        cs._add_chips(empty)
        self.assertEqual(cs.stack, stack)
        self.assertEqual(cs.stack, empty)
        # create an standard stack and add its stack to
        cs2 = ChipStack.from_standard_stack()
        empty = {'$1': 0, '$5': 0, '$10': 0, '$20': 0, '$25': 0, '$50': 0, '$100': 0}
        stack = cs.stack
        cs._add_chips(empty)
        self.assertEqual(cs.stack, stack)
        self.assertEqual(cs.stack, empty)


if __name__ == '__main__':
    unittest.main()
