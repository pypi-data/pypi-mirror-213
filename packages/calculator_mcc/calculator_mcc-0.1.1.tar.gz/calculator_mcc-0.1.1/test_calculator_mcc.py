from calculator_mcc import calculator_mcc as calculator
import unittest


class TestCalculator(unittest.TestCase):
    # add
    def test_add(self):
        calc = calculator.Calculator()
        result = calc.add(10)
        self.assertEqual(result, 10, 'Result should be 10')

    # substract
    def test_substract(self):
        calc = calculator.Calculator()
        result = calc.substract(3)
        self.assertEqual(result, -3, 'Result should be -3')

    # multiply
    def test_multiplication(self):
        calc = calculator.Calculator(2)
        result = calc.multiply(3)
        self.assertEqual(result, 6, 'Result should be 6')

    # division
    def test_division(self):
        calc = calculator.Calculator(2)
        result = calc.divide(2)
        self.assertEqual(result, 1, 'Result should be 1')

        # divide by 0
        with self.assertRaises(ZeroDivisionError):
            calc.divide(0)

    # take nth root
    def test_root(self):
        calc = calculator.Calculator(4)
        result = calc.root(2)
        self.assertEqual(result, 2, 'Result should be 2')

        # take the 0th root
        with self.assertRaises(ZeroDivisionError):
            calc.root(0)

    # remove decimal and fraction if fraction is 0
    def test_remove_integer_decimal(self):
        calc = calculator.Calculator(5.5)  # starts with 5.5
        result = calc.add(5.5)

        self.assertEqual(result, 11, 'Result should be 11')
        self.assertIsInstance(result, int)  # result type is int not float

    # reset calculator to 0
    def test_reset(self):
        calc = calculator.Calculator()
        result = calc.add(10)
        self.assertEqual(result, 10, 'Result should be 10')
        result = calc.reset()
        self.assertEqual(result, 0, 'Result should be 0')
