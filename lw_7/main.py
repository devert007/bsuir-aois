# Программа для работы с диагональной адресацией двумерной матрицы и выполнения операций

def read_bit_column(matrix, index, rows, cols):
    """Считывание разрядного столбца по индексу с диагональной адресацией"""
    result = []
    for j in range(cols):
        row_idx = (index + j) % rows
        result.append(matrix[row_idx][j])
    return result

def read_word_by_index(matrix, index, rows, cols):
    """Считывание слова по индексу с циклическим сдвигом"""
    col = [matrix[i][index] for i in range(rows)]
    lower_part = col[index:]
    upper_part = col[:index]
    result = lower_part + upper_part
    return ''.join(str(x) for x in result)

def f6(x1, x2):
    """Логическая функция f6 = !x1*x2 + x1*!x2"""
    return (not x1 and x2) or (x1 and not x2)

def f9(x1, x2):
    """Логическая функция f9 = x1*x2 + !x1*!x2"""
    return (x1 and x2) or (not x1 and not x2)

def f4(x1, x2):
    """Логическая функция f4 = !x1*x2"""
    return not x1 and x2

def f11(x1, x2):
    """Логическая функция f11 = x1 + !x2"""
    return x1 or not x2

def apply_functions_to_columns(col1, col2):
    """Применение функций f6, f9, f4, f11 к двум разрядным столбцам"""
    result = {
        'f6': [f6(col1[i], col2[i]) for i in range(len(col1))],
        'f9': [f9(col1[i], col2[i]) for i in range(len(col1))],
        'f4': [f4(col1[i], col2[i]) for i in range(len(col1))],
        'f11': [f11(col1[i], col2[i]) for i in range(len(col1))]
    }
    return result

def find_extremum(matrix, rows, cols, find_max=True, active_indices=None):
    """Поиск максимального или минимального значения с маскированным поиском"""
    if active_indices is None:
        active_indices = list(range(rows))
    result_flags = [0] * rows
    for idx in active_indices:
        result_flags[idx] = 1
    for bit_pos in range(cols):
        has_one = False
        temp_flags = result_flags.copy()
        for i in range(rows):
            if result_flags[i]:
                bit = matrix[i][bit_pos]
                if (find_max and bit == 1) or (not find_max and bit == 0):
                    has_one = True
                else:
                    temp_flags[i] = 0
        if has_one:
            result_flags = temp_flags
    return [i for i in range(rows) if result_flags[i]]

def ordered_selection(matrix, rows, cols, find_max=True):
    """Упорядоченная выборка (сортировка) строк матрицы"""
    sorted_indices = []
    active_indices = list(range(rows))
    while active_indices:
        extremum_indices = find_extremum(matrix, rows, cols, find_max, active_indices)
        sorted_indices.extend(extremum_indices)
        active_indices = [idx for idx in active_indices if idx not in extremum_indices]
    return sorted_indices

def add_fields(matrix, key, rows):
    """Сложение полей A и B в словах, где V совпадает с ключом"""
    key_bits = [int(c) for c in key]
    for i in range(rows):
        v_bits = matrix[i][:3]
        if v_bits == key_bits:
            a_bits = matrix[i][3:7]
            b_bits = matrix[i][7:11]
            a_num = sum(a_bits[j] * (2 ** (3-j)) for j in range(4))
            b_num = sum(b_bits[j] * (2 ** (3-j)) for j in range(4))
            sum_result = a_num + b_num
            sum_bits = [0] * 5
            for j in range(4, -1, -1):
                sum_bits[j] = sum_result % 2
                sum_result //= 2
            matrix[i][11:] = sum_bits
    return matrix

def print_matrix(matrix):
    """Вывод матрицы"""
    for row in matrix:
        print(''.join(str(x) for x in row))

if __name__ == "__main__":
    matrix = [
        [1,1,1,1,1,0,0,0,0,1,1,0,0,0,0,0],  
        [0,0,0,1,0,1,0,1,1,0,0,1,0,0,0,0],  
        [1,0,1,0,1,1,0,0,1,0,1,0,0,0,0,0], 
        [0,1,0,0,0,1,1,0,0,1,0,0,0,0,0,0]   
    ]
    rows, cols = len(matrix), len(matrix[0])

    print("Исходная матрица:")
    print_matrix(matrix)

    print("\nСчитывание разрядного столбца с индексом 0:")
    bit_col = read_bit_column(matrix, 0, rows, cols)
    print(bit_col)

    print("\nСчитывание слова по индексу 1:")
    word = read_word_by_index(matrix, 1, rows, cols)
    print(word)

    # print("\nПрименение функций к столбцам 0 и 1:")
    # col1 = read_bit_column(matrix, 0, rows, cols)
    # col2 = read_bit_column(matrix, 1, rows, cols)
    # results = apply_functions_to_columns(col1, col2)
    # for func_name, result in results.items():
    #     print(f"{func_name}: {result}")

    # print("\nИндексы строк с максимальным значением:")
    # max_indices = find_extremum(matrix, rows, cols, find_max=True)
    # print(max_indices)

    # print("\nИндексы строк с минимальным значением:")
    # min_indices = find_extremum(matrix, rows, cols, find_max=False)
    # print(min_indices)

    # print("\nСложение полей A и B для V=111:")
    # matrix = add_fields(matrix, "111", rows)
    # print_matrix(matrix)

    # print("\nМатрица после упорядоченной выборки (по убыванию):")
    # sorted_indices = ordered_selection(matrix, rows, cols, find_max=True)
    # sorted_matrix = [matrix[i] for i in sorted_indices]
    # print_matrix(sorted_matrix)

    # print("\nМатрица после упорядоченной выборки (по возрастанию):")
    # sorted_indices = ordered_selection(matrix, rows, cols, find_max=False)
    # sorted_matrix = [matrix[i] for i in sorted_indices]
    # print_matrix(sorted_matrix)