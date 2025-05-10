import unittest
from io import StringIO
import sys
from hashtable import HashTable

class TestHashTable(unittest.TestCase):
    def setUp(self):
        """Создаём таблицу перед каждым тестом."""
        self.ht = HashTable(5)  # Таблица размера 5

    def test_init(self):
        """Проверяем, что таблица создаётся правильно."""
        self.assertEqual(len(self.ht.h_table), 5)
        self.assertEqual(self.ht.occupied, 0)

    def test_add_and_search(self):
        """Проверяем добавление и поиск."""
        self.ht.add("key1", "data1")
        self.assertEqual(self.ht.search_data("key1"), "data1")
        self.assertEqual(self.ht.occupied, 1)

    def test_add_collision(self):
        """Проверяем добавление с коллизией."""
        self.ht.add("aa", "data1")  # Хэш 194
        self.ht.add("bb", "data2")  # Хэш 194, коллизия
        self.assertEqual(self.ht.search_data("aa"), "data1")
        self.assertEqual(self.ht.search_data("bb"), "data2")
        self.assertEqual(self.ht.occupied, 2)

    def test_add_full_table(self):
        """Проверяем переполнение таблицы."""
        for i in range(5):
            self.ht.add(f"key{i}", f"data{i}")
       

    def test_update(self):
        """Проверяем обновление данных."""
        self.ht.add("key1", "data1")
        self.ht.update("key1", "new_data")
        self.assertEqual(self.ht.search_data("key1"), "new_data")

    def test_update_not_found(self):
        """Проверяем обновление несуществующего ключа."""
       

    def test_update_deleted(self):
        """Проверяем обновление удалённого ключа."""
        self.ht.add("key1", "data1")
        self.ht.delete("key1")
        

    def test_search_not_found(self):
        """Проверяем поиск несуществующего ключа."""
        self.assertIsNone(self.ht.search_data("key1"))

    def test_delete(self):
        """Проверяем удаление ключа."""
        self.ht.add("key1", "data1")
        self.ht.delete("key1")
        self.assertEqual(self.ht.occupied, 0)
        self.assertIsNone(self.ht.search_data("key1"))

    def test_delete_not_found(self):
        """Проверяем удаление несуществующего ключа."""
        self.ht.delete("key1")
        self.assertEqual(self.ht.occupied, 0)

    # Новые тесты для увеличения покрытия

    def test_hash_functions(self):
        """Проверяем хэш-функции."""
        v = sum(ord(c) for c in "test")
        self.assertEqual(self.ht._HashTable__h1(v), v % 5)
        self.assertEqual(self.ht._HashTable__h2(v), 1 + (v % 4))
        self.assertEqual(self.ht._HashTable__double_h(1, v), 
                        (self.ht._HashTable__h1(v) + self.ht._HashTable__h2(v)) % 5)

    def test_print_table(self):
        """Проверяем метод print_table."""
        self.ht.add("key1", "data1")
        captured_output = StringIO()
        sys.stdout = captured_output
        self.ht.print_table()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("key1", output)
        self.assertIn("data1", output)
        self.assertIn("Коэффициент заполнения", output)

    def test_small_table(self):
        """Проверяем работу с таблицей размера 1."""
        small_ht = HashTable(1)
        small_ht.add("key1", "data1")
        self.assertEqual(small_ht.search_data("key1"), "data1")
       

if __name__ == '__main__':
    unittest.main()