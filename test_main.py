from unittest import TestCase, main
from run import load_bundles, addOrder

class TestMain(TestCase):
  def test_load_bundles(self):
    BUNDLES = load_bundles('test_bundle.txt')
    self.assertEqual(len(BUNDLES.keys()), 2)
    self.assertEqual(BUNDLES['Juicing Lovers'], ['1 pc Lemon', '1 pc Ginger', '1 bunch Cavendish Banana'])
    self.assertEqual(BUNDLES['Smoothie & Salad Bundle'], ['20g Organic Pumpkin Seeds', '20g Organic Chia Seeds', "2 bunch Cavendish Banana", "4 pc Ya Pear"])

  def test_add_order(self):
    order = "Cavendish Bananas*1,500g Red Seedless Grapes*1,5 pc Fuji Apples*1,200g Honey Cherry Tomato*4,5 pc Fuji Apples*2"
    products = {}
    products = addOrder(order, products)
    self.assertEqual(products['Cavendish Bananas'], 1)
    self.assertEqual(products['500g Red Seedless Grapes'], 1)
    self.assertEqual(products['5 pc Fuji Apples'], 3)
    self.assertEqual(products['200g Honey Cherry Tomato'], 4)


if __name__ == '__main__':
  main()