import unittest
import sys

sys.path.insert(1, '../src/class_defs')
from chip_stack import ChipStack


class MyTestCase(unittest.TestCase):
    def test_empty_init(self):
        cs = ChipStack()
        for key in cs.stack.keys():
            self.assertEqual(cs.stack[key], 0)

    def test_standard_stack_init(self):
        std = {'$1': 25, '$5': 5, '$10': 3, '$20': 1, '$25': 0, '$50': 2, '$100': 1}
        cs = ChipStack.from_standard_stack()
        for key in cs.stack.keys():
            self.assertEqual(cs.stack[key], std[key])




if __name__ == '__main__':
    unittest.main()
