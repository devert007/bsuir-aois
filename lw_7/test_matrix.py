import unittest
from main import (
    read_bit_column,
    read_word_by_index,
    f6, f9, f4, f11,
    apply_functions_to_columns,
    find_extremum,
    ordered_selection,
    add_fields
)

class TestReadBitColumn(unittest.TestCase):
    def test_diagonal_addressing(self):
        matrix = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ]
        self.assertEqual(read_bit_column(matrix, 0, 3, 3), [0, 4, 8])
        self.assertEqual(read_bit_column(matrix, 1, 3, 3), [3, 7, 2])
        self.assertEqual(read_bit_column(matrix, 2, 3, 3), [6, 1, 5])

class TestReadWordByIndex(unittest.TestCase):
    def test_cyclic_shift(self):
        matrix = [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [8, 9, 10, 11]
        ]
        self.assertEqual(read_word_by_index(matrix, 0, 3, 4), '048')
        self.assertEqual(read_word_by_index(matrix, 1, 3, 4), '591')
        self.assertEqual(read_word_by_index(matrix, 2, 3, 4), '1026')

class TestLogicalFunctions(unittest.TestCase):
    def test_f6(self):
        self.assertEqual(f6(0, 0), False)
        self.assertEqual(f6(0, 1), True)
        self.assertEqual(f6(1, 0), True)
        self.assertEqual(f6(1, 1), False)
    
    def test_f9(self):
        self.assertEqual(f9(0, 0), True)
        self.assertEqual(f9(0, 1), False)
        self.assertEqual(f9(1, 0), False)
        self.assertEqual(f9(1, 1), True)
    
    def test_f4(self):
        self.assertEqual(f4(0, 0), False)
        self.assertEqual(f4(0, 1), True)
        self.assertEqual(f4(1, 0), False)
        self.assertEqual(f4(1, 1), False)
    
    def test_f11(self):
        self.assertEqual(f11(0, 0), True)
        self.assertEqual(f11(0, 1), False)
        self.assertEqual(f11(1, 0), True)
        self.assertEqual(f11(1, 1), True)

class TestApplyFunctionsToColumns(unittest.TestCase):
    def test_function_applications(self):
        col1 = [0, 1, 0, 1]
        col2 = [1, 0, 1, 0]
        results = apply_functions_to_columns(col1, col2)
        
        self.assertEqual(results['f6'], [True, True, True, True])
        self.assertEqual(results['f9'], [False, False, False, False])
        self.assertEqual(results['f4'], [True, False, True, False])
        self.assertEqual(results['f11'], [False, True, False, True])

class TestFindExtremum(unittest.TestCase):
    def setUp(self):
        self.matrix = [
            [1, 0, 0],  # Row 0: 4 (100)
            [0, 1, 0],  # Row 1: 2 (010)
            [1, 1, 0]   # Row 2: 6 (110)
        ]
        self.rows = 3
        self.cols = 3

    def test_find_max(self):
        max_indices = find_extremum(self.matrix, self.rows, self.cols, find_max=True)
        self.assertEqual(max_indices, [2])
    
    def test_find_min(self):
        min_indices = find_extremum(self.matrix, self.rows, self.cols, find_max=False)
        self.assertEqual(min_indices, [1])
    
    def test_masked_search(self):
        active = [0, 2]
        max_indices = find_extremum(self.matrix, self.rows, self.cols, True, active)
        self.assertEqual(max_indices, [2])

class TestOrderedSelection(unittest.TestCase):
    def test_ordered_max(self):
        matrix = [
            [0, 0, 0],  # 0
            [1, 0, 0],  # 4
            [0, 1, 0]   # 2
        ]
        sorted_idx = ordered_selection(matrix, 3, 3, find_max=True)
        self.assertEqual(sorted_idx, [1, 2, 0])
    
    def test_ordered_min(self):
        matrix = [
            [1, 0, 0],  # 4
            [0, 1, 0],  # 2
            [0, 0, 1]   # 1
        ]
        sorted_idx = ordered_selection(matrix, 3, 3, find_max=False)
        self.assertEqual(sorted_idx, [2, 1, 0])

class TestAddFields(unittest.TestCase):
    def test_add_matching_key(self):
        matrix = [
            [1,1,1, 1,0,0,0, 0,1,1,0, 0,0,0,0,0]  # V=111, A=8, B=6 → Sum=14 (01110)
        ]
        add_fields(matrix, '111', 1)
        self.assertEqual(matrix[0][11:], [0,1,1,1,0])
    
    def test_no_key_match(self):
        matrix = [
            [1,0,1, 1,0,0,0, 0,1,1,0, 0,0,0,0,0]  # V=101
        ]
        original = matrix[0].copy()
        add_fields(matrix, '111', 1)
        self.assertEqual(matrix[0], original)

if __name__ == '__main__':
    unittest.main()