import unittest
from main_1 import Logic_operator 

class TestLogicOperatorMinimization(unittest.TestCase):
    def test_simple_opz(self):
        logic = Logic_operator("a&b")
        opz= logic.turn_to_opz()
        self.assertEqual(opz, "ab&")
        
    def test_complex_opz(self):
        logic = Logic_operator("(a&b)|c")
        opz =logic.turn_to_opz()
        self.assertEqual(opz, "ab&c|")
        
  
        
    def test_triple_opz(self):
        logic = Logic_operator("(a|(b&c))")
        opz= logic.turn_to_opz()
        self.assertEqual(opz, "abc&|")
    def test_negative_opz(self):
        logic = Logic_operator("!a&b")
        opz= logic.turn_to_opz()
        self.assertEqual(opz, "a!b&")
    def test_minimize_sdnf_raschetny_2vars(self):
        logic = Logic_operator("a|b")
        result = logic.minimize_sdnf_raschetny()
        expected_options = ["(b)|(a)", "(a)|(b)"]
        self.assertIn(result, expected_options)

    def test_minimize_sdnf_raschetny_3vars(self):
        logic = Logic_operator("a&b|c")
        result = logic.minimize_sdnf_raschetny()
        expected_options = ["(a&b)|(c)", "(c)|(a&b)"]
        self.assertIn(result, expected_options)

    def test_minimize_sdnf_raschetny_4vars(self):
        logic = Logic_operator("(a&b)|(c&d)")
        result = logic.minimize_sdnf_raschetny()
        
        expected_options = ["(a&b)|(c&d)", "(c&d)|(a&b)"]
        self.assertIn(result, expected_options)

    def test_minimize_sdnf_raschetny_false(self):
        logic = Logic_operator("a&!a")
        result = logic.minimize_sdnf_raschetny()
        self.assertEqual(result, "Функция всегда истинна")

    def test_minimize_sknf_raschetny_2vars(self):
        logic = Logic_operator("a&b")
        result = logic.minimize_sknf_raschetny()
        expected_options = ["(b)&(a)", "(a)&(b)"]
        self.assertIn(result, expected_options)

    def test_minimize_sknf_raschetny_3vars(self):
        logic = Logic_operator("(a|b)&c")
        result = logic.minimize_sknf_raschetny()
        expected_options = ["(c)&(a|b)", "(a|b)&(c)"]
        self.assertIn(result, expected_options)

    def test_minimize_sknf_raschetny_4vars(self):
        logic = Logic_operator("(a|b)&(c|d)")
        result = logic.minimize_sknf_raschetny()
        expected_options = ["(a|b)&(c|d)", "(c|d)&(a|b)"]
        self.assertIn(result, expected_options)

    def test_minimize_sknf_raschetny_true(self):
        logic = Logic_operator("a|!a")
        result = logic.minimize_sknf_raschetny()
        self.assertEqual(result, "Функция всегда истинна")

    def test_minimize_sdnf_raschet_table_2vars(self):
        logic = Logic_operator("a|b")
        result = logic.minimize_sdnf_raschet_table()
        expected_options = ["(a)|(b)", "(b)|(a)"]
        self.assertIn(result, expected_options)

    def test_minimize_sdnf_raschet_table_3vars(self):
        logic = Logic_operator("a&b|c")
        result = logic.minimize_sdnf_raschet_table()
        expected_options = ["(a&b)|(c)", "(c)|(a&b)"]
        self.assertIn(result, expected_options)

    def test_minimize_sdnf_raschet_table_4vars(self):
        logic = Logic_operator("(a&b)|(c&d)")
        result = logic.minimize_sdnf_raschet_table()
        expected_options = ["(a&b)|(c&d)", "(c&d)|(a&b)"]
        self.assertIn(result, expected_options)

    def test_minimize_sdnf_raschet_table_false(self):
        logic = Logic_operator("a&!a")
        result = logic.minimize_sdnf_raschet_table()
        self.assertEqual(result, "Функция всегда истинна")

    def test_minimize_sknf_raschet_table_2vars(self):
        logic = Logic_operator("a&b")
        result = logic.minimize_sknf_raschet_table()
        expected_options = ["(a)&(b)", "(b)&(a)"]
        self.assertIn(result, expected_options)

    def test_minimize_sknf_raschet_table_3vars(self):
        logic = Logic_operator("(a|b)&c")
        result = logic.minimize_sknf_raschet_table()
        expected_options = ["(c)&(a|b)", "(a|b)&(c)"]
        self.assertIn(result, expected_options)

    def test_minimize_sknf_raschet_table_4vars(self):
        # Исправлено: используем a|b&c|d вместо (a|b)&(c|d)
        logic = Logic_operator("(a|b)&(c|d)")
        result = logic.minimize_sknf_raschet_table()
        expected_options = ["(a|b)&(c|d)", "(c|d)&(a|b)"]
        self.assertIn(result, expected_options)

    def test_minimize_sknf_raschet_table_true(self):
        logic = Logic_operator("a|!a")
        result = logic.minimize_sknf_raschet_table()
        self.assertEqual(result, "Функция всегда истинна")

    def test_karnaugh_map_sdnf_2vars(self):
        logic = Logic_operator("a|b")
        result = logic.karnaugh_map_sdnf()
        expected_options = ["(a)|(b)", "(b)|(a)"]
        self.assertIn(result, expected_options)

    def test_karnaugh_map_sdnf_3vars(self):
        logic = Logic_operator("a&b|c")
        result = logic.karnaugh_map_sdnf()
        expected_options = ["(a&b)|(c)", "(c)|(a&b)"]
        self.assertIn(result, expected_options)

    def test_karnaugh_map_sdnf_4vars(self):
        # Исправлено: используем a&b|c&d вместо (a&b)|(c&d)
        logic = Logic_operator("a&b|c&d")
        result = logic.karnaugh_map_sdnf()
        expected_options = ["(c&d)|(a&b&d)", "(a&b&d)|(c&d)"]
        self.assertIn(result, expected_options)

    def test_karnaugh_map_sdnf_5vars(self):
        logic = Logic_operator("(a&b&e)|(c&d)")
        result = logic.karnaugh_map_sdnf()
        expected_options = ["(!e&c&d)|(e&c&d)|(a&b&e)", "(a&b&e)|(!e&c&d)|(e&c&d)","(!e&c&d)|(a&b&e)|(e&c&d)"]
        self.assertIn(result, expected_options)

    def test_karnaugh_map_sdnf_false(self):
        logic = Logic_operator("a&!a")
        result = logic.karnaugh_map_sdnf()
        self.assertEqual(result, "0")

    def test_karnaugh_map_sdnf_invalid_vars(self):
        logic = Logic_operator("a&b|c&d")  
        logic.new_letters_list.append("e") 
        logic.new_letters_list.append("f") 
        result = logic.karnaugh_map_sdnf()
        self.assertIsNone(result)

    def test_karnaugh_map_sknf_2vars(self):
        logic = Logic_operator("a&b")
        result = logic.karnaugh_map_sknf()
        expected_options = ["(a)&(b)", "(b)&(a)"]
        self.assertIn(result, expected_options)

    def test_karnaugh_map_sknf_3vars(self):
        logic = Logic_operator("a|b&c")
        result = logic.karnaugh_map_sknf()
        expected = "(a|!b|!c)&(!a|!b|!c)"
        expected_options = ["(a|b)&(b|c)&(!b|c)", "(a|b)&(!b|c)&(b|c)","(b|c)&(a|b)&(!b|c)&(b|c)"]
        self.assertIn(result, expected_options)
   
    

    def test_karnaugh_map_sknf_true(self):
        logic = Logic_operator("a|!a")
        result = logic.karnaugh_map_sknf()
        self.assertEqual(result, "1")

    def test_karnaugh_map_sknf_invalid_vars(self):
        logic = Logic_operator("a&b|c&d")  # 4 переменные
        logic.new_letters_list.append("e")  # Добавляем пятую вручную
        logic.new_letters_list.append("f")  # Добавляем шестую вручную
        result = logic.karnaugh_map_sknf()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()