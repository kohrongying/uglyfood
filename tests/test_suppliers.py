import unittest
from suppliers import build_supply, sort_supply


class TestSuppliers(unittest.TestCase):
    def test_build_supply(self):
        lines = ['BC\n', 'Fruit A\n', 'Fruit B\n', '\n', 'SF\n', 'Veg 1\n', 'Veg 2\n', '\n', '\n', 'RM\n', 'Fruit Z\n',
                 'Veg X\n']
        outcome = build_supply(lines)
        self.assertEqual(outcome, {'Fruit A': {'qty': 0, 'supplier': 'BC'},
                                   'Fruit B': {'qty': 0, 'supplier': 'BC'},
                                   'Fruit Z': {'qty': 0, 'supplier': 'RM'},
                                   'Veg 1': {'qty': 0, 'supplier': 'SF'},
                                   'Veg 2': {'qty': 0, 'supplier': 'SF'},
                                   'Veg X': {'qty': 0, 'supplier': 'RM'}})


    def test_sort_supply(self):
        SUPPLY = {'Fruit A': {'qty': 0, 'supplier': 'BC'},
                                   'Fruit B': {'qty': 0, 'supplier': 'BC'},
                                   'Fruit Z': {'qty': 0, 'supplier': 'RM'},
                                   'Veg 1': {'qty': 0, 'supplier': 'SF'},
                                   'Veg 2': {'qty': 0, 'supplier': 'SF'},
                                   'Veg X': {'qty': 0, 'supplier': 'RM'}}
        outcome = sort_supply(SUPPLY)
        self.assertEqual(outcome, {'BC': [{'product': 'Fruit A', 'qty': 0}, {'product': 'Fruit B', 'qty': 0}],
                                'RM': [{'product': 'Fruit Z', 'qty': 0}, {'product': 'Veg X', 'qty': 0}],
                                'SF': [{'product': 'Veg 1', 'qty': 0}, {'product': 'Veg 2', 'qty': 0}]})

if __name__ == '__main__':
    unittest.main()
