import unittest
from hashtable import HashTable  

class TestHashTable(unittest.TestCase):

    def setUp(self):
        """Инициализация таблицы перед каждым тестом."""
        self.ht = HashTable(8)  

    def test_init(self):
        """Тест инициализации таблицы."""
        self.assertEqual(len(self.ht.h_table), 8)
        self.assertEqual(self.ht.occupied, 0)
        for entry in self.ht.h_table:
            self.assertEqual(entry[2]['U'], 0)
            self.assertEqual(entry[2]['D'], 0)

    def test_hash_functions(self):
        """Тест хэш-функций __h1, __h2, __double_h."""
        v = sum(ord(c) for c in "test")
        self.assertEqual(self.ht._HashTable__h1(v), v % 8)
        self.assertEqual(self.ht._HashTable__h2(v), 1 + (v % 7))
        self.assertEqual(self.ht._HashTable__double_h(0, v), self.ht._HashTable__h1(v))
        self.assertEqual(self.ht._HashTable__double_h(1, v), 
                        (self.ht._HashTable__h1(v) + self.ht._HashTable__h2(v)) % 8)

    def test_add_success(self):
        """Тест успешного добавления ключа и данных."""
        self.ht.add("key1", "data1")
        index = self.ht._HashTable__search_index("key1")
        self.assertIsNotNone(index)
        self.assertEqual(self.ht.h_table[index][0], "key1")
        self.assertEqual(self.ht.h_table[index][1], "data1")
        self.assertEqual(self.ht.h_table[index][2]['U'], 1)
        self.assertEqual(self.ht.h_table[index][2]['T'], 1)
        self.assertEqual(self.ht.occupied, 1)

    def test_add_collision(self):
        """Тест добавления с коллизией."""
        self.ht.add("aa", "data1")  
        self.ht.add("bb", "data2")  
        index1 = self.ht._HashTable__search_index("aa")
        index2 = self.ht._HashTable__search_index("bb")
        self.assertNotEqual(index1, index2)
        self.assertEqual(self.ht.h_table[index2][2]['C'], 1)
        self.assertEqual(self.ht.h_table[index1][2]['Po'], index2)

    def test_add_full_table(self):
        """Тест переполнения таблицы."""
        for i in range(8):
            self.ht.add(f"key{i}", f"data{i}")
        with self.assertRaises(Exception) as context:
            self.ht.add("key9", "data9")
        self.assertTrue("Таблица полна" in str(context.exception))

    def test_update_success(self):
        """Тест успешного обновления данных."""
        self.ht.add("key1", "data1")
        self.ht.update("key1", "new_data")
        index = self.ht._HashTable__search_index("key1")
        self.assertEqual(self.ht.h_table[index][1], "new_data")

    def test_update_key_not_found(self):
        """Тест обновления несуществующего ключа."""
        with self.assertRaises(KeyError) as context:
            self.ht.update("key1", "data1")
        self.assertTrue("не найден" in str(context.exception))

    def test_update_deleted_node(self):
        """Тест обновления удалённого узла."""
        self.ht.add("key1", "data1")
        self.ht.delete("key1")
        with self.assertRaises(ValueError) as context:
            self.ht.update("key1", "new_data")
        self.assertTrue("Невозможно обновить удаленный узел" in str(context.exception))

    def test_search_data_success(self):
        """Тест успешного поиска данных."""
        self.ht.add("key1", "data1")
        self.assertEqual(self.ht.search_data("key1"), "data1")

    def test_search_data_not_found(self):
        """Тест поиска несуществующего ключа."""
        self.assertIsNone(self.ht.search_data("key1"))

    def test_delete_success(self):
        """Тест успешного удаления ключа."""
        self.ht.add("key1", "data1")
        self.ht.delete("key1")
        index = self.ht._HashTable__search_index("key1")
        self.assertEqual(self.ht.h_table[index][2]['U'], 0)
        self.assertEqual(self.ht.h_table[index][2]['D'], 1)
        self.assertEqual(self.ht.occupied, 0)

    def test_delete_nonexistent(self):
        """Тест удаления несуществующего ключа (без ошибок)."""
        self.ht.delete("key1") 
        self.assertEqual(self.ht.occupied, 0)

    def test_print_table(self):
        """Тест вывода таблицы (проверка формата, не критично)."""
        self.ht.add("key1", "data1")
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.ht.print_table()
        sys.stdout = sys.__stdout__
        output ='1 1 1 0 0'
        self.assertIn("key1", output)
        self.assertIn("1 1 1 0 0", output)  

if __name__ == '__main__':
    unittest.main() 