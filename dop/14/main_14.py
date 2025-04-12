import math
from bitarray import bitarray


class BloomFilter(object):

    def __init__(self, size, number_expected_elements=100000):
        self.size = size
        self.number_expected_elements = number_expected_elements

        self.bloom_filter = bitarray(self.size)
        self.bloom_filter.setall(0)

        self.number_hash_functions = round((self.size / self.number_expected_elements) * math.log(2))


    def _hash_djb2(self, input_string):
        hash = 5381
        for x in input_string:
            hash = ((hash << 5) + hash) + ord(x)
        return hash % self.size


    def _hash(self, item, K):
        return self._hash_djb2(str(K) + item)


    def add_to_filter(self, item):
        for i in range(self.number_hash_functions):
            self.bloom_filter[self._hash(item, i)] = 1


    def check_is_not_in_filter(self, item):
        for i in range(self.number_hash_functions):
            if self.bloom_filter[self._hash(item, i)] == 0:
                return True
        return False

#пример использования 
bloom_filter = BloomFilter(1000, 1000)
base_ip = "trrrrt"
bloom_filter.add_to_filter(base_ip )
base_ip2 = "trr"
bloom_filter.add_to_filter(base_ip2 )

if not bloom_filter.check_is_not_in_filter(base_ip):
    print(base_ip)
if not bloom_filter.check_is_not_in_filter(base_ip2 ):
    print(base_ip2)

#фильтр Блума придуман (и реализован) для удобства поиска в некой базе элементов (например в списке IP адресов).
# Фильтр представляет собой массив битов 
#(значение 0, если индекс - не хэшированное значение, значение 1, если индексом данной ячейки является захэшированный переданный параметр (например, IP адрес или строка) )
# Главная задача фильтра определить,что элемент НЕ находится в фильтре
# Это удобно для базы IP адресов, где есть заблокированные адреса
# Заблокированные адреса помещаются в фильтр и при запросе одним IP адресом доступа к какому-либо ресурсу
# Метод фильтра проверяет не находится ли этот IP в фильтре, вместо проверки всей базы с IP  адресами