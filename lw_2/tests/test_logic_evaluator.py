import unittest
import sys
import os
from io import StringIO
from unittest.mock import patch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logic_evaluator import LogicProcessor, LogicInterface, Operator

class TestLogicEvaluator(unittest.TestCase):
    def setUp(self):
        self.simple_expr = "a&b"
        self.complex_expr = "(a&b)|c"
        self.not_expr = "!a"
        self.implies_expr = "a>b"
        self.equiv_expr = "a~b"
        self.single_var_expr = "a"
        self.all_true_expr = "a|a"
        self.all_false_expr = "a&!a"

    # Tests for LogicProcessor
    def test_init_simple_expression(self):
        proc = LogicProcessor(self.simple_expr)
        self.assertEqual(proc.var_list, ["a", "b"])
        self.assertEqual(len(proc.table), 3)  # 2 vars + result row
        self.assertEqual(len(proc.table[0]), 5)  # 2^2 + 1 columns
        self.assertEqual(proc.table[0][0], "a")
        self.assertEqual(proc.table[1][0], "b")
        self.assertEqual(proc.table[2][0], self.simple_expr)

    def test_init_complex_expression(self):
        proc = LogicProcessor(self.complex_expr)
        self.assertEqual(proc.var_list, ["a", "b", "c"])
        self.assertEqual(len(proc.table), 4)  # 3 vars + result
        self.assertEqual(len(proc.table[0]), 9)  # 2^3 + 1 columns

    def test_init_single_variable(self):
        proc = LogicProcessor(self.single_var_expr)
        self.assertEqual(proc.var_list, ["a"])
        self.assertEqual(len(proc.table), 2)  # 1 var + result
        self.assertEqual(len(proc.table[0]), 3)  # 2^1 + 1 columns

    def test_init_invalid_expression(self):
        with self.assertRaises(Exception):
            LogicProcessor("a&&b")  # Invalid operator

    def test_to_binary(self):
        proc = LogicProcessor(self.simple_expr)
        self.assertEqual(proc._to_binary(0, 2), "00")
        self.assertEqual(proc._to_binary(1, 2), "01")
        self.assertEqual(proc._to_binary(3, 2), "11")
        self.assertEqual(proc._to_binary(0, 3), "000")

    def test_build_rpn_simple(self):
        proc = LogicProcessor(self.simple_expr)
        self.assertEqual(proc.rpn, "ab&")

    def test_build_rpn_complex(self):
        proc = LogicProcessor(self.complex_expr)
        self.assertEqual(proc.rpn, "ab&c|")

    def test_build_rpn_not(self):
        proc = LogicProcessor(self.not_expr)
        self.assertEqual(proc.rpn, "a!")

    def test_build_rpn_implies(self):
        proc = LogicProcessor(self.implies_expr)
        self.assertEqual(proc.rpn, "ab>")

    def test_build_rpn_equiv(self):
        proc = LogicProcessor(self.equiv_expr)
        self.assertEqual(proc.rpn, "ab~")

    def test_evaluate_rpn_and(self):
        proc = LogicProcessor(self.simple_expr)
        values = {"a": 1, "b": 1}
        self.assertEqual(proc._evaluate_rpn(values), 1)
        values = {"a": 1, "b": 0}
        self.assertEqual(proc._evaluate_rpn(values), 0)

    def test_evaluate_rpn_or(self):
        proc = LogicProcessor("a|b")
        values = {"a": 0, "b": 1}
        self.assertEqual(proc._evaluate_rpn(values), 1)
        values = {"a": 0, "b": 0}
        self.assertEqual(proc._evaluate_rpn(values), 0)

    def test_evaluate_rpn_not(self):
        proc = LogicProcessor(self.not_expr)
        values = {"a": 1}
        self.assertEqual(proc._evaluate_rpn(values), 0)
        values = {"a": 0}
        self.assertEqual(proc._evaluate_rpn(values), 1)

    def test_evaluate_rpn_implies(self):
        proc = LogicProcessor(self.implies_expr)
        values = {"a": 1, "b": 0}
        self.assertEqual(proc._evaluate_rpn(values), 0)
        values = {"a": 0, "b": 0}
        self.assertEqual(proc._evaluate_rpn(values), 1)

    def test_evaluate_rpn_equiv(self):
        proc = LogicProcessor(self.equiv_expr)
        values = {"a": 1, "b": 1}
        self.assertEqual(proc._evaluate_rpn(values), 1)
        values = {"a": 1, "b": 0}
        self.assertEqual(proc._evaluate_rpn(values), 0)

    def test_populate_table_simple(self):
        proc = LogicProcessor(self.simple_expr)
        self.assertEqual(proc.table[2][1], "0")  # 00 -> 0
        self.assertEqual(proc.table[2][2], "0")  # 01 -> 0
        self.assertEqual(proc.table[2][3], "0")  # 10 -> 0
        self.assertEqual(proc.table[2][4], "1")  # 11 -> 1

    def test_populate_table_complex(self):
        proc = LogicProcessor(self.complex_expr)
        self.assertEqual(proc.table[3][1], "0")  # 000 -> 0
        self.assertEqual(proc.table[3][5], "1")  # 100 -> 1

    def test_get_sdnf(self):
        proc = LogicProcessor(self.simple_expr)
        sdnf = proc.get_sdnf()
        self.assertIn("(a&b)", sdnf)
        self.assertEqual(sdnf.count("("), 1)  # One term

    def test_get_sdnf_all_true(self):
        proc = LogicProcessor(self.all_true_expr)
        sdnf = proc.get_sdnf()
        self.assertEqual(sdnf.count("("), 2)  # Two terms: a or !a

    def test_get_sdnf_all_false(self):
        proc = LogicProcessor(self.all_false_expr)
        sdnf = proc.get_sdnf()
        self.assertEqual(sdnf, "()")  # No terms

    def test_get_sknf(self):
        proc = LogicProcessor(self.simple_expr)
        sknf = proc.get_sknf()
        self.assertIn("(a|!b)", sknf)
        self.assertEqual(sknf.count("("), 3)  # Three terms

    def test_get_sknf_all_true(self):
        proc = LogicProcessor(self.all_true_expr)
        sknf = proc.get_sknf()
        self.assertEqual(sknf, "()")  # No terms

    def test_get_sknf_all_false(self):
        proc = LogicProcessor(self.all_false_expr)
        sknf = proc.get_sknf()
        self.assertEqual(sknf.count("("), 2)  # Two terms

    def test_get_index_form(self):
        proc = LogicProcessor(self.simple_expr)
        self.assertEqual(proc.get_index_form(), 8)  # 1000 in binary
        proc = LogicProcessor(self.all_true_expr)
        self.assertEqual(proc.get_index_form(), 3)  # 11 in binary
        proc = LogicProcessor(self.all_false_expr)
        self.assertEqual(proc.get_index_form(), 0)  # 00 in binary

    def test_display_table_output(self):
        proc = LogicProcessor(self.simple_expr)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            proc._display_table()
            output = fake_out.getvalue()
            self.assertIn("Variables: ab", output)
            self.assertIn("00", output)
            self.assertIn("a b a&b", output)
            self.assertIn("1 1 1", output)

    # Tests for LogicInterface
    def test_interface_init(self):
        interface = LogicInterface()
        self.assertIsNone(interface.processor)
        self.assertIsInstance(interface, LogicInterface)

    def test_display_menu_output(self):
        interface = LogicInterface()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            interface.display_menu()
            output = fake_out.getvalue()
            self.assertIn("Logic Evaluator", output)
            self.assertIn("1. Enter expression", output)
            self.assertIn("5. Exit", output)

    @patch('builtins.input', side_effect=["1", "a&b", "5"])
    def test_run_create_expression(self, mock_input):
        interface = LogicInterface()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            interface.run()
            output = fake_out.getvalue()
            self.assertIn("Truth table generated!", output)
            self.assertIn("Exiting...", output)

    @patch('builtins.input', side_effect=["2", "5"])
    def test_run_sdnf_no_processor(self, mock_input):
        interface = LogicInterface()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            interface.run()
            output = fake_out.getvalue()
            self.assertIn("Please enter an expression first.", output)

    @patch('builtins.input', side_effect=["1", "a&b", "2", "5"])
    def test_run_sdnf(self, mock_input):
        interface = LogicInterface()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            interface.run()
            output = fake_out.getvalue()
            self.assertIn("SDNF: (a&b)", output)

    @patch('builtins.input', side_effect=["1", "a&b", "3", "5"])
    def test_run_sknf(self, mock_input):
        interface = LogicInterface()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            interface.run()
            output = fake_out.getvalue()
            self.assertIn("SKNF: ", output)
            self.assertIn("(a|!b)", output)

    @patch('builtins.input', side_effect=["1", "a&b", "4", "5"])
    def test_run_index_form(self, mock_input):
        interface = LogicInterface()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            interface.run()
            output = fake_out.getvalue()
            self.assertIn("Index form: 8", output)

    @patch('builtins.input', side_effect=["6", "5"])
    def test_run_invalid_choice(self, mock_input):
        interface = LogicInterface()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            interface.run()
            output = fake_out.getvalue()
            self.assertIn("Invalid option. Choose 1-5.", output)

if __name__ == '__main__':
    unittest.main()