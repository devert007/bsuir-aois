import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bin_converter import BinaryConverter
from bin_operations import BinaryOperations
from dec_converter import DecimalConverter
from interface import UserInterface

class TestBinaryOperations(unittest.TestCase):
    def setUp(self):
        self.bin_conv = BinaryConverter()
        self.bin_ops = BinaryOperations()
        self.dec_conv = DecimalConverter()
        self.ui = UserInterface()

    # Tests for BinaryConverter
    def test_to_binary_positive(self):
        self.assertEqual(self.bin_conv.to_binary(15), "1111")
        self.assertEqual(self.bin_conv.to_binary(1), "1")

    def test_to_binary_zero(self):
        self.assertEqual(self.bin_conv.to_binary(0), "0")

    def test_to_binary_large(self):
        self.assertEqual(self.bin_conv.to_binary(1024), "10000000000")

    def test_direct_code_positive(self):
        self.assertEqual(self.bin_conv.direct_code(15), "01111")
        self.assertEqual(self.bin_conv.direct_code(0), "00")

    def test_direct_code_negative(self):
        self.assertEqual(self.bin_conv.direct_code(-15), "11111")
        self.assertEqual(self.bin_conv.direct_code(-1), "11")

    def test_inverse_code_positive(self):
        self.assertEqual(self.bin_conv.inverse_code(15), "01111")
        self.assertEqual(self.bin_conv.inverse_code(0), "00")

    def test_inverse_code_negative(self):
        self.assertEqual(self.bin_conv.inverse_code(-15), "10000")
        self.assertEqual(self.bin_conv.inverse_code(-1), "10")

    def test_additional_code_positive(self):
        self.assertEqual(self.bin_conv.additional_code(15), "01111")
        self.assertEqual(self.bin_conv.additional_code(0), "00")

    def test_additional_code_negative(self):
        self.assertEqual(self.bin_conv.additional_code(-15), "10001")
        self.assertEqual(self.bin_conv.additional_code(-1), "11")

    def test_fixed_point_binary_integer(self):
        self.assertEqual(self.bin_conv.fixed_point_binary(10), "01010")
        self.assertEqual(self.bin_conv.fixed_point_binary(-10), "11010")

    def test_fixed_point_binary_fractional(self):
        self.assertEqual(self.bin_conv.fixed_point_binary(10.5), "01010.1")
        self.assertEqual(self.bin_conv.fixed_point_binary(-10.5), "11010.1")

    def test_fixed_point_binary_zero(self):
        self.assertEqual(self.bin_conv.fixed_point_binary(0.0), "00")

    def test_fixed_point_binary_small_fraction(self):
        result = self.bin_conv.fixed_point_binary(0.25)
        self.assertTrue(result.startswith("0"))
        self.assertIn(".01", result)

    def test_floating_point_binary_positive(self):
        result = self.bin_conv.floating_point_binary(10.5)
        self.assertEqual(len(result), 32)
        self.assertTrue(result.startswith("0"))
        self.assertAlmostEqual(self.dec_conv.floating_to_decimal(result), 10.5, places=5)

    def test_floating_point_binary_negative(self):
        result = self.bin_conv.floating_point_binary(-10.5)
        self.assertEqual(len(result), 32)
        self.assertTrue(result.startswith("1"))
        self.assertAlmostEqual(self.dec_conv.floating_to_decimal(result), -10.5, places=5)

    def test_floating_point_binary_zero(self):
        result = self.bin_conv.floating_point_binary(0.0)
        self.assertEqual(result, "0" + "0" * (self.bin_conv.EXP_BITS + self.bin_conv.MANT_BITS))

    def test_floating_point_binary_small(self):
        result = self.bin_conv.floating_point_binary(0.125)
        self.assertAlmostEqual(self.dec_conv.floating_to_decimal(result), 0.125, places=5)

    # Tests for DecimalConverter
    def test_binary_to_decimal_positive(self):
        self.assertEqual(self.dec_conv.binary_to_decimal("1111"), 15)
        self.assertEqual(self.dec_conv.binary_to_decimal("1"), 1)

    def test_binary_to_decimal_zero(self):
        self.assertEqual(self.dec_conv.binary_to_decimal("0"), 0)
        self.assertEqual(self.dec_conv.binary_to_decimal(""), 0)

    def test_fixed_to_decimal_integer(self):
        self.assertEqual(self.dec_conv.fixed_to_decimal("01010"), 10)
        self.assertEqual(self.dec_conv.fixed_to_decimal("11010"), -10)

    def test_fixed_to_decimal_fractional(self):
        self.assertAlmostEqual(self.dec_conv.fixed_to_decimal("01010.1"), 10.5, places=5)
        self.assertAlmostEqual(self.dec_conv.fixed_to_decimal("11010.1"), -10.5, places=5)

    def test_fixed_to_decimal_zero(self):
        self.assertEqual(self.dec_conv.fixed_to_decimal("00"), 0)

    def test_fixed_to_decimal_no_fraction(self):
        self.assertEqual(self.dec_conv.fixed_to_decimal("0101"), 5)

    def test_direct_to_decimal_positive(self):
        self.assertEqual(self.dec_conv.direct_to_decimal("01111"), "15")
        self.assertEqual(self.dec_conv.direct_to_decimal("00"), "0")

    def test_direct_to_decimal_negative(self):
        self.assertEqual(self.dec_conv.direct_to_decimal("11111"), "-15")
        self.assertEqual(self.dec_conv.direct_to_decimal("11"), "-1")

    def test_direct_to_decimal_empty(self):
        self.assertEqual(self.dec_conv.direct_to_decimal(""), "0")

    def test_inverse_to_decimal_positive(self):
        self.assertEqual(self.dec_conv.inverse_to_decimal("01111"), "15")
        self.assertEqual(self.dec_conv.inverse_to_decimal("00"), "0")

    def test_inverse_to_decimal_negative(self):
        self.assertEqual(self.dec_conv.inverse_to_decimal("10000"), "-15")
        self.assertEqual(self.dec_conv.inverse_to_decimal("10"), "-1")

    def test_inverse_to_decimal_empty(self):
        self.assertEqual(self.dec_conv.inverse_to_decimal(""), "0")

    def test_additional_to_decimal_positive(self):
        self.assertEqual(self.dec_conv.additional_to_decimal("01111"), "16")
        self.assertEqual(self.dec_conv.additional_to_decimal("00"), "1")

    def test_additional_to_decimal_negative(self):
        self.assertEqual(self.dec_conv.additional_to_decimal("10001"), "0")
        self.assertEqual(self.dec_conv.additional_to_decimal("11"), "2")

    def test_additional_to_decimal_empty(self):
        self.assertEqual(self.dec_conv.additional_to_decimal(""), "0")

    def test_floating_to_decimal_positive(self):
        bin_float = self.bin_conv.floating_point_binary(10.5)
        self.assertAlmostEqual(self.dec_conv.floating_to_decimal(bin_float), 10.5, places=5)

    def test_floating_to_decimal_negative(self):
        bin_float = self.bin_conv.floating_point_binary(-10.5)
        self.assertAlmostEqual(self.dec_conv.floating_to_decimal(bin_float), -10.5, places=5)

    def test_floating_to_decimal_zero(self):
        self.assertEqual(self.dec_conv.floating_to_decimal("0" * 32), 0)

    def test_floating_to_decimal_short_input(self):
        self.assertEqual(self.dec_conv.floating_to_decimal("0" * 10), 0)

    # Tests for BinaryOperations
    def test_binary_add_no_carry(self):
        self.assertEqual(self.bin_ops.binary_add("1010", "0101", 4), "1111")

    def test_binary_add_with_carry(self):
        self.assertEqual(self.bin_ops.binary_add("1111", "0001", 4), "10000")
        self.assertEqual(self.bin_ops.binary_add("1111", "1111", 4), "11110")

    def test_binary_add_zero(self):
        self.assertEqual(self.bin_ops.binary_add("0000", "0000", 4), "0000")

    def test_add_additional_codes_positive(self):
        result = self.bin_ops.add_additional_codes(10, 5)
        self.assertEqual(len(result), 8)
        self.assertEqual(self.dec_conv.additional_to_decimal(result), "16")

    def test_add_additional_codes_negative(self):
        result = self.bin_ops.add_additional_codes(-10, -5)
        self.assertEqual(len(result), 8)
        self.assertEqual(self.dec_conv.additional_to_decimal(result), "-14")

    def test_add_additional_codes_mixed(self):
        result = self.bin_ops.add_additional_codes(10, -5)
        self.assertEqual(len(result), 8)
        self.assertEqual(self.dec_conv.additional_to_decimal(result), "6")

    def test_subtract_additional_codes_positive(self):
        result = self.bin_ops.subtract_additional_codes(10, 5)
        self.assertEqual(len(result), 8)
        self.assertEqual(self.dec_conv.additional_to_decimal(result), "6")

    def test_subtract_additional_codes_negative(self):
        result = self.bin_ops.subtract_additional_codes(-10, -5)
        self.assertEqual(len(result), 8)
        self.assertEqual(self.dec_conv.additional_to_decimal(result), "-4")

    def test_subtract_additional_codes_mixed(self):
        result = self.bin_ops.subtract_additional_codes(10, -5)
        self.assertEqual(len(result), 8)
        self.assertEqual(self.dec_conv.additional_to_decimal(result), "16")

    def test_multiply_direct_codes_positive(self):
        result = self.bin_ops.multiply_direct_codes(3, 4)
        self.assertTrue(result.startswith("0"))
        self.assertEqual(self.dec_conv.direct_to_decimal(result), "12")

    def test_multiply_direct_codes_negative(self):
        result = self.bin_ops.multiply_direct_codes(-3, -4)
        self.assertTrue(result.startswith("0"))
        self.assertEqual(self.dec_conv.direct_to_decimal(result), "12")

    def test_multiply_direct_codes_mixed(self):
        result = self.bin_ops.multiply_direct_codes(3, -4)
        self.assertTrue(result.startswith("1"))
        self.assertEqual(self.dec_conv.direct_to_decimal(result), "-12")

    def test_multiply_direct_codes_zero(self):
        result = self.bin_ops.multiply_direct_codes(0, 5)
        self.assertTrue(result.startswith("0"))
        self.assertEqual(self.dec_conv.direct_to_decimal(result), "0")

    def test_divide_direct_codes_positive(self):
        result = self.bin_ops.divide_direct_codes(12, 3)
        self.assertTrue(result.startswith("0"))
        self.assertEqual(self.dec_conv.fixed_to_decimal(result), 4.0)

    def test_divide_direct_codes_negative(self):
        result = self.bin_ops.divide_direct_codes(-12, 3)
        self.assertTrue(result.startswith("1"))
        self.assertEqual(self.dec_conv.fixed_to_decimal(result), -4.0)

    def test_divide_direct_codes_fractional(self):
        result = self.bin_ops.divide_direct_codes(10, 4)
        self.assertTrue(result.startswith("0"))
        self.assertAlmostEqual(self.dec_conv.fixed_to_decimal(result), 2.5, places=5)

    def test_divide_direct_codes_zero_divisor(self):
        with self.assertRaises(ValueError):
            self.bin_ops.divide_direct_codes(10, 0)

    def test_add_floating_point_positive(self):
        result = self.bin_ops.add_floating_point(10.5, 5.5)
        self.assertTrue(result.startswith("0"))
        self.assertAlmostEqual(self.dec_conv.floating_to_decimal(result), 16.0, places=5)

    def test_add_floating_point_negative(self):
        result = self.bin_ops.add_floating_point(-10.5, -5.5)
        self.assertTrue(result.startswith("1"))
        self.assertAlmostEqual(self.dec_conv.floating_to_decimal(result), -16.0, places=5)

    def test_add_floating_point_mixed(self):
        result = self.bin_ops.add_floating_point(10.5, -5.5)
        self.assertTrue(result.startswith("0"))
        self.assertAlmostEqual(self.dec_conv.floating_to_decimal(result), 5.0, places=5)

    def test_add_floating_point_zero(self):
        result = self.bin_ops.add_floating_point(0.0, 0.0)
        self.assertEqual(result, "0" * 32)

    # Test for UserInterface
    def test_user_interface_init(self):
        self.assertIsInstance(self.ui.bin_converter, BinaryConverter)
        self.assertIsInstance(self.ui.dec_converter, DecimalConverter)
        self.assertIsInstance(self.ui.bin_ops, BinaryOperations)

if __name__ == '__main__':
    unittest.main()