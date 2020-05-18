from unittest import TestCase
from sales_details import get_subtotal, get_total, get_discount, set_coupon

row = ['completed', '20042011379', '2010-02-20T20:35:25-07:00', 'Person', 'test@gmail.com', '98765432',
               'Address Line1', 'Singapore ', '', 'Singapore', '123456',
               '200g French Bean*1,200g Xiao Bai Cai*1,200g Red Long Chilli*1,750g Purple Sweet Potato*1,3pc Traffic Light Bell Pepper*1,200g Garlic*1,1 pc Hairy Gourd*2,200g Organic Brown Button Mushroom*1,Carrots*4',
               'SGD', '$20.25', '$8.00', 'HIT50', '$0.00', '$0.00', 'false', '$28.25', 'Stripe', '']

class TestSalesDetails(TestCase):

    def test_get_subtotal(self):
        self.assertEqual(get_subtotal(row), 20.25)

    def test_get_total(self):
         self.assertEqual(get_total(row), 28.25)

    def test_get_discount(self):
        self.assertEqual(get_discount(row), 0)

    def test_set_coupon(self):
        self.assertEqual(set_coupon({}, row), { 'HIT50': 1} )
        self.assertEqual(set_coupon({'HIT50': 1}, row), { 'HIT50': 2} )



if __name__ == '__main__':
    main()

