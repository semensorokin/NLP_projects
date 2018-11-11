import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unit_test_examples as ex
import unittest


class TestMultiplication(unittest.TestCase):
    def test_simple_multiplication(self):
        self.assertEqual(2, ex.multiply(1, 2))
        self.assertEqual(8, ex.multiply(4, 2))
        self.assertEqual(0, ex.multiply(1, 0))
        self.assertEqual(-2, ex.multiply(-1, 2))
        self.assertEqual(15, ex.multiply(3, 5))
        self.assertEqual(1000000000000, ex.multiply(1000000, 1000000))

    def test_float_multipication(self):
        self.assertEqual(2.5, ex.multiply(5, 0.5))


class TestInCircle(unittest.TestCase):
    def test_positive(self):
        self.assertTrue(ex.is_in_circle(0.0, 0.0))
        self.assertTrue(ex.is_in_circle(0.7, 0.0))
        self.assertTrue(ex.is_in_circle(0.0, 0.7))
        self.assertTrue(ex.is_in_circle(-0.7, 0.0))
        self.assertTrue(ex.is_in_circle(0.0, -0.7))
        self.assertTrue(ex.is_in_circle(0.7, 0.7))
        self.assertTrue(ex.is_in_circle(-0.7, -0.7))

    def test_negative(self):
        self.assertFalse(ex.is_in_circle(0.7, 0.8))
        self.assertFalse(ex.is_in_circle(0.8, 0.7))
        self.assertFalse(ex.is_in_circle(0.7, -0.8))
        self.assertFalse(ex.is_in_circle(-0.8, 0.7))
        self.assertFalse(ex.is_in_circle(-0.7, -0.8))
        self.assertFalse(ex.is_in_circle(-0.8, -0.7))

    def test_border(self):
        self.assertTrue(ex.is_in_circle(1.0, 0.0))
        self.assertTrue(ex.is_in_circle(-1.0, 0.0))
        self.assertTrue(ex.is_in_circle(0.0, -1.0))
        self.assertTrue(ex.is_in_circle(0.0, -1.0))
        self.assertTrue(ex.is_in_circle(0.707106781, 0.707106781))
        self.assertTrue(ex.is_in_circle(0.707106781, -0.707106781))
        self.assertTrue(ex.is_in_circle(-0.707106781, 0.707106781))
        self.assertTrue(ex.is_in_circle(-0.707106781, -0.707106781))



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMultiplication)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInCircle)
    unittest.TextTestRunner(verbosity=2).run(suite)

