class HashTable():
    def __init__(self, size):
        self.size = size
        self.h_table = [
            (None, None,
             {'C': 0,          # Флаг коллизии
              'U': 0,          # Занята ли ячейка
              'T': 0,          # Терминальный флажок
              'L': 0,          # Данные или указатель в Pi
              'D': 0,          # Удалённая ячейка
              'Po': None})     # Указатель при коллизии
            for _ in range(size)
        ]
        self.occupied = 0 

    def __h1(self, v):
        return v % self.size

    def __h2(self, v):
        return 1 + (v % (self.size - 1))

    def __double_h(self, i, v):
        return (self.__h1(v) + i * self.__h2(v)) % self.size

    def add(self, key, data):
        v = sum(ord(i) for i in key)
        main_index = self.__h1(v)
        prev_index = None
        i = 0
        index = main_index
        
        while i < self.size:
            current = self.h_table[index]
            if current[2]['U'] == 0 or current[2]['D'] == 1:
                break    
            if current[0] == key:
                break
                
            prev_index = index  
            i += 1
            index = self.__double_h(i, v)
        else:
            raise Exception("Таблица полна")

        if prev_index is not None:
           
            prev_entry = list(self.h_table[prev_index])
            prev_entry[2]['Po'] = index  
            prev_entry[2]['T'] = 0       
            self.h_table[prev_index] = tuple(prev_entry)

        new_flags = {
            'C': i > 0,
            'U': 1,
            'T': 1, 
            'L': 0,
            'D': 0,
            'Po': None
        }

        if self.h_table[index][2]['U'] == 0:
            self.occupied += 1

        self.h_table[index] = (key, data, new_flags)


    def update(self,key,data):
        index = self.__search_index(key)
        if index is None:
          raise KeyError(f"Ключ '{key}' не найден в таблице")
        if self.h_table[index][2]['D'] == 1:
          raise ValueError("Невозможно обновить удаленный узел")
        new_tuple = (self.h_table[index][0],data,self.h_table[index][2])
        self.h_table[index] = new_tuple
    
    def search_data(self, key):
        v = sum(ord(i) for i in key)
        index = self.__h1(v)
        for i in range(self.size):
            current = self.h_table[index]
            if current[2]['U'] == 1 and current[0] == key:
                return current[1]
            if current[2]['U'] == 0 and current[2]['D'] == 0:
                break
            index = self.__double_h(i + 1, v)
        return None
  
    def __search_index(self, key):
        v = sum(ord(i) for i in key)
        index = self.__h1(v)
        for i in range(self.size):
            current = self.h_table[index]
            if current[2]['U'] == 1 and current[0] == key:
                return index
            if current[2]['U'] == 0 and current[2]['D'] == 0:
                break
            index = self.__double_h(i + 1, v)
        return None

    def delete(self, key):
        index = self.__search_index(key)
        if index is not None:
            if self.h_table[index][2]['U'] == 1:
                self.occupied -= 1
            self.h_table[index] = (
                self.h_table[index][0],
                self.h_table[index][1],
                {
                    'C': self.h_table[index][2]['C'],
                    'U': 0,
                    'T': self.h_table[index][2]['T'],
                    'L': self.h_table[index][2]['L'],
                    'D': 1,
                    'Po': self.h_table[index][2]['Po']
                }
            )

    def print_table(self):
        print(f"{'№':<3} {'ID':<15} {'C':<3} {'U':<3} {'T':<3} {'L':<3} {'D':<3} {'Po':<5} {'Pi':<20}")
        print("-" * 70)
        for i, (key, data, flags) in enumerate(self.h_table):
            if flags['U'] == 1 or flags['D'] == 1:
                print(
                    f"{i:<3} {str(key):<15} {flags['C']:<3} {flags['U']:<3} {flags['T']:<3} {flags['L']:<3} "
                    f"{flags['D']:<3} {str(flags['Po']):<5} {str(data):<20}"
                )
        print(f"Коэффициент заполнения: {self.occupied / self.size:.2f}")