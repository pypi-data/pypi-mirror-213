import unittest
from tcCalc3.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def tearDown(self):
        super().tearDown()

    def test_add(self):
        self.assertEqual(self.calculator.add(2), 2, "Should be 2")

    def test_add_negative(self):
        self.assertEqual(self.calculator.add(-2), -2, "Should be -2")

    def test_subtract(self):
        self.assertEqual(self.calculator.subtract(2), -2, "Should be -2")

    def test_subtract_negative(self):
        self.assertEqual(self.calculator.subtract(-2), 2, "Should be 2")

    def test_multiply_zero_by_number(self):
        self.assertEqual(self.calculator.multiply(0), 0, "Should be 0")

    def test_multiply_two_positive_numbers(self):
        self.calculator.value = 5
        self.assertEqual(self.calculator.multiply(5), 25, "Should be 25")

    def test_multiply_positive_negative_number(self):
        self.calculator.value = 5
        self.assertEqual(self.calculator.multiply(-5), -25, "Should be -25")

    def test_multiply_two_negative_numbers(self):
        self.calculator.value = -5
        self.assertEqual(self.calculator.multiply(-5), 25, "Should be 25")

    def test_divide_0_by_number(self):
        self.assertEqual(self.calculator.divide(10), 0, "Should be 0")

    def test_divide_2_positive_numbers(self):
        self.calculator.value = 100
        self.assertEqual(self.calculator.divide(10), 10, "Should be 10")

    def test_divide_positive_negative_numbers(self):
        self.calculator.value = 100
        self.assertEqual(self.calculator.divide(-10), -10, "Should be -10")

    def test_divide_two_negative_numbers(self):
        self.calculator.value = -100
        self.assertEqual(self.calculator.divide(-10), 10, "Should be 10")

    def test_nroot(self):
        self.assertEqual(self.calculator.nroot(81, 2), 9.0, "Should be 9.0")
  
    def test_nroot_negative(self):
        with self.assertRaises(ValueError) as cm:
            self.calculator.nroot(-81,2)
        the_exception = cm.exception
        self.assertIn("Cannot calculate even root of a negative number", str(the_exception))

    def test_reset(self):
        self.calculator.value = 10
        self.assertEqual(self.calculator.reset(), 0, "Should be 0")

    def test_memory(self):
        self.assertEqual(self.calculator.memory(), 0, "Should be zero")
        self.calculator.value = 15
        self.assertEqual(self.calculator.memory(), 15, "Should be 15")


if __name__ == '__main__':
    unittest.main()