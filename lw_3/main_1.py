class Logic_operator:
    def __init__(self,func_str:str):
        self.operaions_array=["&",">","|","!","~"]
        self.letters_array=["a","b","c","d","e"]
        self.func_str=func_str
        self.new_letters_list=[]

        for i in self.func_str:
            if (i not in self.operaions_array) & (i not in self.new_letters_list)&(i in self.letters_array):
                self.new_letters_list.append(i)
        self.truth_table = []
        #заполняем нулями, пример: [a, 0,0,0,0,0]
        for i in range(0,len(self.new_letters_list),1):
            self.truth_table.append([0]*(pow(2,len(self.new_letters_list))+1))
            self.truth_table[i][0]=self.new_letters_list[i]
        

        print(f"Итоговая таблица с переменными:\n{''.join(self.new_letters_list)}")

        for i in range(0,pow(2,len(self.new_letters_list)),1):
            binary_value=self.get_binary_value(i,len(self.new_letters_list))
            print(binary_value)
            for j in range(0,len(self.new_letters_list),1):
                self.truth_table[j][i+1]=binary_value[j]
        print(self.truth_table)

        #create OPZ
        self.turn_to_opz()
        print(f"OPZ:{self.opz}")
        #truth_table of all
        self.create_truth_table()
        self.print_truth_table()


  
    def get_binary_value(self,value,length)->str:
        direct_binary = ''
        abs_value= abs(value)
        while abs_value > 0 :
            direct_binary= str(abs_value % 2)+direct_binary
            abs_value = abs_value // 2 
        if len(direct_binary)<length:
            direct_binary=direct_binary.zfill(length)
        return direct_binary


    def turn_to_opz(self):
        def priority(char_el):
            match char_el:
                case '>':return 2
                case '&':return 2
                case '|':return 2
                case '~':return 2
                case '!':return 3
                case '(':return 1
            return 0
        stack_list=[]
        self.opz=""
        for char_el in self.func_str:
            if char_el =='(' :
                stack_list.append(char_el)
            if char_el==')':
                while(stack_list[-1]!='('):
                    self.opz=self.opz+stack_list[-1]
                    stack_list.pop()
                stack_list.pop()
            if char_el in self.new_letters_list:
                self.opz=self.opz+char_el
            if char_el in self.operaions_array:
                while stack_list!=[] and priority(stack_list[-1])>=priority(char_el):
                    self.opz=self.opz+stack_list[-1]
                    stack_list.pop()
                stack_list.append(char_el)
        while stack_list!=[]:
            self.opz=self.opz+stack_list[-1]
            stack_list.pop()
        return self.opz
     
    def create_truth_table(self):
        stack_list=[]
        val_dict={}
        
        for num_str in range(1,len(self.truth_table[0]),1):
            count_operaions_array=len(self.new_letters_list)-1
            for col in range(0,len(self.truth_table),1):
                val_dict[self.truth_table[col][0]]=self.truth_table[col][num_str]
            for char_el in self.opz :
                if char_el in self.new_letters_list:
                    stack_list.append(char_el)
                elif char_el=='!':
                    

                    op1=int(val_dict[stack_list[-1]])
                    if op1==1 : 
                        rez = "0" 
                    else: 
                        rez="1"
                    if num_str==1:
                        self.truth_table.append([0]*(pow(2,len(self.new_letters_list))+1))
                        self.truth_table[len(self.truth_table )-1][0]=char_el+stack_list[-1]
                    count_operaions_array+=1
                    self.truth_table[count_operaions_array][num_str]=rez
                    val_dict[self.truth_table[count_operaions_array][0]]=self.truth_table[count_operaions_array][num_str]
                    stack_list.append(char_el+stack_list[-1])
                    stack_list.pop(-2)
                    
                else:
                    op1=int(val_dict[stack_list[-2]])
                    op2=int(val_dict[stack_list[-1]])
                    match(char_el):
                        case '&': rez=str(op1 * op2)
                        case'|': rez= str(op1 | op2)
                        case'>': rez=str(int(not (bool(op1)) or bool(op2)))
                        case'~':rez=str(int(op1==op2))
                    if num_str==1:
                        self.truth_table.append([0]*(pow(2,len(self.new_letters_list))+1))
                        self.truth_table[len(self.truth_table)-1][0]=stack_list[-2]+char_el+stack_list[-1]
                    count_operaions_array+=1
                    self.truth_table[count_operaions_array][num_str]=rez
                    val_dict[self.truth_table[count_operaions_array][0]]=self.truth_table[count_operaions_array][num_str]
                    stack_list.append(stack_list[-2]+char_el+stack_list[-1])
                    stack_list.pop(-3)
                    stack_list.pop(-2)
            stack_list.clear()
            val_dict.clear()
    def print_truth_table(self):
        truth_table_head = str(self.truth_table[0][0])
        for i in range(1,len(self.truth_table),1):
            truth_table_head+=' ' +self.truth_table[i][0]
        print(truth_table_head)
        for i in range(1, len(self.truth_table[0])): 
                row_values =''  
                for row in self.truth_table:
                    row_values += row[i] + ' '  
                print(row_values.rstrip())


    def build_sdnf_str(self):
        sdnf_valueForm=["("]
        sdnf=[]
        for num_str in range(0,len(self.truth_table[0])-1,1):
            if self.truth_table[len(self.truth_table)-1][num_str+1]=="1":
                sdnf_valueForm.append(str(num_str))
                sdnf_valueForm.append(",")
                sdnf.append("(")
                for col_number in range(0,len((self.new_letters_list)),1):
                    if self.truth_table[col_number][num_str+1]== "0":
                        sdnf.append("!")
                    sdnf.append(self.truth_table[col_number][0])
                    sdnf.append("&")
                sdnf.pop()
                sdnf.append(")")
                sdnf.append("|")
        sdnf.pop()
        sdnf_valueForm.pop()
        sdnf_valueForm.append(")")
        sdnf_valueForm.append("|")
        return str(sdnf)
        # print(str(sdnf_valueForm)) 
   
    def build_sknf_str(self):
        sknf_valueForm=["("]
        sknf=[]
        for num_str in range(0,len(self.truth_table[0])-1,1):
            if self.truth_table[len(self.truth_table)-1][num_str+1]=="0":
                sknf_valueForm.append(str(num_str))
                sknf_valueForm.append(",")
                sknf.append("(")
                for col_number in range(0,len((self.new_letters_list)),1):
                    if self.truth_table[col_number][num_str+1]== "1":
                        sknf.append("!")
                    sknf.append(self.truth_table[col_number][0])
                    sknf.append("|")
                sknf.pop()
                sknf.append(")")
                sknf.append("&")
        sknf.pop()
        sknf_valueForm.pop()
        sknf_valueForm.append(")")
        sknf_valueForm.append("&")
        return str(sknf)
        # print(str(sknf_valueForm))    
    def binary_to_decimal(self,value):
        result =0
        degree=0
        for i in range(len(value)-1,-1,-1):
            result += int(value[i])*2**degree
            degree+=1
        return result
    def rez_index_form(self):
        rez=""
        for num_str in range(1,len(self.truth_table[0]),1):
            rez+=self.truth_table[len(self.truth_table)-1][num_str]

        return self.binary_to_decimal(rez)

    def get_sdnf_minterms(self):
        n = len(self.new_letters_list)
        minterms = []
        for i in range(1, len(self.truth_table[0])):
            if self.truth_table[-1][i] == "1":
                minterm = [int(self.truth_table[j][i]) for j in range(n)]
                minterms.append(minterm)
        return minterms

    def get_sknf_maxterms(self):
        n = len(self.new_letters_list)
        maxterms = []
        for i in range(1, len(self.truth_table[0])):
            if self.truth_table[-1][i] == "0":
                maxterm = [int(self.truth_table[j][i]) for j in range(n)]
                maxterms.append(maxterm)
        return maxterms

    # Расчетный метод для СДНФ
    def minimize_sdnf_raschetny(self):
        array_sdnf = self.get_sdnf_minterms()
        if not array_sdnf:
            return "Функция всегда истинна"
        
        print("\nИсходные максимумы:")
        for term in array_sdnf:
            print(''.join(str(x) for x in term))

        current_terms = array_sdnf
        step = 1

        while True:
            print(f"\nШаг {step} склеивания:")
            combined_set = set()  
            new_terms_set = set() 

            for i in range(len(current_terms)):
                for j in range(i + 1, len(current_terms)):
                    term_1 = current_terms[i]
                    term_2 = current_terms[j]
                    diff = 0
                    diff_position = -1
                    
                    for k in range(len(self.new_letters_list)):
                        if term_1[k] != term_2[k]:
                            diff += 1
                            diff_position = k
                    
                    if diff == 1:
                        new_term = term_1.copy()
                        new_term[diff_position] = 'X'
                        new_terms_set.add(tuple(new_term))
                        combined_set.add(i)
                        combined_set.add(j)

            if new_terms_set:
                print("Склеенные импликанты:")
                for term in new_terms_set:
                    print(''.join(str(x) for x in term))
            else:
                print("Больше склеиваний нет")
                break

            result_set = set(new_terms_set)
            for i in range(len(current_terms)):
                if i not in combined_set:
                    result_set.add(tuple(current_terms[i]))

            current_terms = [list(term) for term in result_set]
            step += 1

        print("\nМинимизированная СДНФ:")
        result_expr = []
        for term in current_terms:
            term_str = []
            for i in range(len(term)):
                if term[i] == 0: 
                    term_str.append(f"!{self.new_letters_list[i]}")
                elif term[i] == 1:  
                    term_str.append(f"{self.new_letters_list[i]}")
            result_expr.append("(" + "&".join(term_str) + ")")
        
        final_expression = "|".join(result_expr)
        print(final_expression)
        return final_expression
    # Расчетный метод для СКНФ
    def minimize_sknf_raschetny(self):
        array_sknf = self.get_sknf_maxterms()
        if not array_sknf:
            return "Функция всегда истинна"
        
        print("\nИсходные максимумы:")
        for term in array_sknf:
            print(''.join(str(x) for x in term))

        current_terms = array_sknf
        step = 1

        while True:
            print(f"\nШаг {step} склеивания:")
            combined_set = set()  
            new_terms_set = set() 

            for i in range(len(current_terms)):
                for j in range(i + 1, len(current_terms)):
                    term_1 = current_terms[i]
                    term_2 = current_terms[j]
                    diff = 0
                    diff_position = -1
                    
                    for k in range(len(self.new_letters_list)):
                        if term_1[k] != term_2[k]:
                            diff += 1
                            diff_position = k
                    
                    if diff == 1:
                        new_term = term_1.copy()
                        new_term[diff_position] = 'X'
                        new_terms_set.add(tuple(new_term))
                        combined_set.add(i)
                        combined_set.add(j)

            if new_terms_set:
                print("Склеенные импликанты:")
                for term in new_terms_set:
                    print(''.join(str(x) for x in term))
            else:
                print("Больше склеиваний нет")
                break

            result_set = set(new_terms_set)
            for i in range(len(current_terms)):
                if i not in combined_set:
                    result_set.add(tuple(current_terms[i]))

            current_terms = [list(term) for term in result_set]
            step += 1

        print("\nМинимизированная СКНФ:")
        result_expr = []
        for term in current_terms:
            term_str = []
            for i in range(len(term)):
                if term[i] == 0: 
                    term_str.append(self.new_letters_list[i])
                elif term[i] == 1:  
                    term_str.append(f"!{self.new_letters_list[i]}")
            result_expr.append("(" + "|".join(term_str) + ")")
        
        final_expression = "&".join(result_expr)
        print(final_expression)
        return final_expression
        
        pass

    # Расчетно-табличный метод для СДНФ
    def minimize_sdnf_raschet_table(self):
        array_sdnf = self.get_sdnf_minterms()
        if not array_sdnf:
            return "Функция всегда истинна"
        
        print("\nИсходные минтермы:")
        for term in array_sdnf:
            print(''.join(str(x) for x in term))

        current_terms = array_sdnf
        step = 1

        while True:
            print(f"\nШаг {step} склеивания:")
            combined_set = set()  
            new_terms_set = set() 

            for i in range(len(current_terms)):
                for j in range(i + 1, len(current_terms)):
                    term_1 = current_terms[i]
                    term_2 = current_terms[j]
                    diff = 0
                    diff_position = -1
                    
                    for k in range(len(self.new_letters_list)):
                        if term_1[k] != term_2[k]:
                            diff += 1
                            diff_position = k
                    
                    if diff == 1:
                        new_term = term_1.copy()
                        new_term[diff_position] = 'X'
                        new_terms_set.add(tuple(new_term))
                        combined_set.add(i)
                        combined_set.add(j)

            if new_terms_set:
                print("Склеенные импликанты:")
                for term in new_terms_set:
                    print(''.join(str(x) for x in term))
            else:
                print("Больше склеиваний нет")
                break

            result_set = set(new_terms_set)
            for i in range(len(current_terms)):
                if i not in combined_set:
                    result_set.add(tuple(current_terms[i]))

            current_terms = [list(term) for term in result_set]
            step += 1
        
        print("\nСклеенные термы:")
        print(current_terms)

        # Построение таблицы покрытия
        result_terms = set()
        table = []
        for term in current_terms:
            row = []
            for minterm in array_sdnf:
                is_covered = True
                for i in range(len(term)):
                    if term[i] != 'X' and term[i] != minterm[i]:
                        is_covered = False
                        break
                row.append(1 if is_covered else 0)
            table.append(row)

        # Компактная таблица
        print("\nТаблица покрытия:")
        col_width = max(4, max(len(''.join(str(x) for x in term)) for term in array_sdnf))  # Минимальная ширина 4
        header = [''.join(str(x) for x in minterm) for minterm in array_sdnf]
        
        # Заголовок таблицы
        header_line = " " * col_width + "|" + "|".join(f"{h:^{col_width}}" for h in header) + "|"
        separator = "-" * col_width + "+" + "+".join("-" * col_width for _ in header) + "+"
        
        print(separator)
        print(header_line)
        print(separator)

        # Строки таблицы
        for i, row in enumerate(table):
            term_str = ''.join(str(x) for x in current_terms[i])
            row_line = f"{term_str:<{col_width}}|" + "|".join(f"{x:^{col_width}}" for x in row) + "|"
            print(row_line)
            if i == len(table) - 1:
                print(separator)

        # Поиск существенных импликантов
        for j in range(len(array_sdnf)):  
            one_count = 0
            term_idx = -1
            for i in range(len(current_terms)):  
                if table[i][j] == 1:
                    one_count += 1
                    term_idx = i
            if one_count == 1:  
                result_terms.add(tuple(current_terms[term_idx]))

        print("\nСущественные импликанты:", result_terms)

        # Формирование минимизированной СДНФ
        print("\nМинимизированная СДНФ:")
        result_table_raschet = []
        for term in result_terms:
            term_str = []
            for i in range(len(term)):
                if term[i] == 'X':
                    continue  # Пропускаем позиции с 'X'
                if term[i] == 0: 
                    term_str.append(f"!{self.new_letters_list[i]}")
                elif term[i] == 1:  
                    term_str.append(f"{self.new_letters_list[i]}")
            if term_str:  
                result_table_raschet.append("(" + "&".join(term_str) + ")")

        final_expression = "|".join(result_table_raschet) if result_table_raschet else "Функция всегда истинна"
        print(final_expression)
        return final_expression
    # Расчетно-табличный метод для СКНФ
    def minimize_sknf_raschet_table(self):
        array_sdnf = self.get_sknf_maxterms()
        if not array_sdnf:
            return "Функция всегда истинна"
        
        print("\nИсходные максимумы:")
        for term in array_sdnf:
            print(''.join(str(x) for x in term))

        current_terms = array_sdnf
        step = 1

        while True:
            print(f"\nШаг {step} склеивания:")
            combined_set = set()  
            new_terms_set = set() 

            for i in range(len(current_terms)):
                for j in range(i + 1, len(current_terms)):
                    term_1 = current_terms[i]
                    term_2 = current_terms[j]
                    diff = 0
                    diff_position = -1
                    
                    for k in range(len(self.new_letters_list)):
                        if term_1[k] != term_2[k]:
                            diff += 1
                            diff_position = k
                    
                    if diff == 1:
                        new_term = term_1.copy()
                        new_term[diff_position] = 'X'
                        new_terms_set.add(tuple(new_term))
                        combined_set.add(i)
                        combined_set.add(j)

            if new_terms_set:
                print("Склеенные импликанты:")
                for term in new_terms_set:
                    print(''.join(str(x) for x in term))
            else:
                print("Больше склеиваний нет")
                break

            result_set = set(new_terms_set)
            for i in range(len(current_terms)):
                if i not in combined_set:
                    result_set.add(tuple(current_terms[i]))

            current_terms = [list(term) for term in result_set]
            step += 1
        
        print("\nСклеенные термы:")
        print(current_terms)

        # Построение таблицы покрытия
        result_terms = set()
        table = []
        for term in current_terms:
            row = []
            for minterm in array_sdnf:
                is_covered = True
                for i in range(len(term)):
                    if term[i] != 'X' and term[i] != minterm[i]:
                        is_covered = False
                        break
                row.append(1 if is_covered else 0)
            table.append(row)

        # Компактная таблица
        print("\nТаблица покрытия:")
        col_width = max(4, max(len(''.join(str(x) for x in term)) for term in array_sdnf))  # Минимальная ширина 4
        header = [''.join(str(x) for x in minterm) for minterm in array_sdnf]
        
        # Заголовок таблицы
        header_line = " " * col_width + "|" + "|".join(f"{h:^{col_width}}" for h in header) + "|"
        separator = "-" * col_width + "+" + "+".join("-" * col_width for _ in header) + "+"
        
        print(separator)
        print(header_line)
        print(separator)

        # Строки таблицы
        for i, row in enumerate(table):
            term_str = ''.join(str(x) for x in current_terms[i])
            row_line = f"{term_str:<{col_width}}|" + "|".join(f"{x:^{col_width}}" for x in row) + "|"
            print(row_line)
            if i == len(table) - 1:
                print(separator)

        # Поиск существенных импликантов
        for j in range(len(array_sdnf)):  
            one_count = 0
            term_idx = -1
            for i in range(len(current_terms)):  
                if table[i][j] == 1:
                    one_count += 1
                    term_idx = i
            if one_count == 1:  
                result_terms.add(tuple(current_terms[term_idx]))

        print("\nСущественные импликанты:", result_terms)

        # Формирование минимизированной СКНФ
        print("\nМинимизированная СКНФ:")
        result_table_raschet = []
        for term in result_terms:
            term_str = []
            for i in range(len(term)):
                if term[i] == 'X':
                    continue  
                if term[i] == 0: 
                    term_str.append(f"{self.new_letters_list[i]}")
                elif term[i] == 1:  
                    term_str.append(f"!{self.new_letters_list[i]}")
            if term_str:  
                result_table_raschet.append("(" + "|".join(term_str) + ")")

        final_expression = "&".join(result_table_raschet) if result_table_raschet else "Функция всегда истинна"
        print(final_expression)
        return final_expression
    # Карта Карно для СДНФ
    def karnaugh_map_sdnf(self):
        minterms = self.get_sdnf_minterms()
        n = len(self.new_letters_list)
        
        if not minterms:
            print("Функция равна 0, нет минтермов для СДНФ")
            return "0"
        
        if n == 2:
            rows, cols = 2, 2
            row_vars = [self.new_letters_list[0]]
            col_vars = [self.new_letters_list[1]]
        elif n == 3:
            rows, cols = 2, 4
            row_vars = [self.new_letters_list[0]]
            col_vars = [self.new_letters_list[1], self.new_letters_list[2]]
        elif n == 4:
            rows, cols = 4, 4
            row_vars = [self.new_letters_list[0], self.new_letters_list[1]]
            col_vars = [self.new_letters_list[2], self.new_letters_list[3]]
        elif n == 5:
            rows, cols = 4, 8
            row_vars = [self.new_letters_list[0], self.new_letters_list[1]]
            col_vars = [self.new_letters_list[2], self.new_letters_list[3], self.new_letters_list[4]]
        else:
            print("Карта Карно поддерживает только 2-5 переменных")
            return None

        kmap = [[0] * cols for _ in range(rows)]
        
        gray_rows = ['0', '1'] if rows == 2 else ['00', '01', '11', '10']
        gray_cols = ['0', '1'] if cols == 2 else ['00', '01', '11', '10'] if cols == 4 else ['000', '001', '011', '010', '110', '111', '101', '100']
        
        for minterm in minterms:
            if n == 2:
                row = minterm[0]
                col = minterm[1]
            elif n == 3:
                row = minterm[0]
                col_bin = ''.join(str(minterm[i]) for i in [1, 2])
                col = {'00': 0, '01': 1, '11': 2, '10': 3}[col_bin]
            elif n == 4:
                row_bin = ''.join(str(minterm[i]) for i in [0, 1])
                col_bin = ''.join(str(minterm[i]) for i in [2, 3])
                row = {'00': 0, '01': 1, '11': 2, '10': 3}[row_bin]
                col = {'00': 0, '01': 1, '11': 2, '10': 3}[col_bin]
            else:  # n == 5
                row_bin = ''.join(str(minterm[i]) for i in [0, 1])
                col_bin = ''.join(str(minterm[i]) for i in [2, 3, 4])
                row = {'00': 0, '01': 1, '11': 2, '10': 3}[row_bin]
                col = {'000': 0, '001': 1, '011': 2, '010': 3, '110': 4, '111': 5, '101': 6, '100': 7}[col_bin]
            kmap[row][col] = 1

        print("\nКарта Карно для СДНФ:")
        if n == 2:
            header = f"{'':4} {col_vars[0]}=0 {col_vars[0]}=1"
        elif n == 3:
            header = f"{'':4} {col_vars[0]}{col_vars[1]}=00 {col_vars[0]}{col_vars[1]}=01 {col_vars[0]}{col_vars[1]}=11 {col_vars[0]}{col_vars[1]}=10"
        elif n == 4:
            header = f"{'':4} {col_vars[0]}{col_vars[1]}=00 {col_vars[0]}{col_vars[1]}=01 {col_vars[0]}{col_vars[1]}=11 {col_vars[0]}{col_vars[1]}=10"
        else:  
            header = f"{'':4} {col_vars[0]}{col_vars[1]}{col_vars[2]}=000 {col_vars[0]}{col_vars[1]}{col_vars[2]}=001 {col_vars[0]}{col_vars[1]}{col_vars[2]}=011 {col_vars[0]}{col_vars[1]}{col_vars[2]}=010 {col_vars[0]}{col_vars[1]}{col_vars[2]}=110 {col_vars[0]}{col_vars[1]}{col_vars[2]}=111 {col_vars[0]}{col_vars[1]}{col_vars[2]}=101 {col_vars[0]}{col_vars[1]}{col_vars[2]}=100"
        print(header)
        
        for i in range(rows):
            if n == 2:
                row_label = f"{row_vars[0]}={gray_rows[i]}"
            elif n == 3:
                row_label = f"{row_vars[0]}={gray_rows[i]}"
            else:  # n == 4 or 5
                row_label = f"{row_vars[0]}{row_vars[1]}={gray_rows[i]}"
            print(f"{row_label:4} {' '.join(str(kmap[i][j]) for j in range(cols))}")
        
        # Поиск групп
        groups = []
        covered = set()
        
        # Проверяем группы разного размера: 8, 4, 2, 1 (для 5 переменных до 8)
        for size in [8, 4, 2, 1]:
            if size > rows * cols:
                continue
            # Проверяем все возможные прямоугольники
            for r in range(rows):
                for c in range(cols):
                    # Проверяем группы размера size (например, 4 = 2x2, 2x1, 1x2)
                    for h in [1, 2, 4] if size > 1 else [1]:
                        for w in [size // h] if h * (size // h) == size else []:
                            if r + h > rows or c + w > cols:
                                continue
                            # Проверяем, содержит ли область единицы
                            ones = []
                            for i in range(r, r + h):
                                for j in range(c, c + w):
                                    i_mod = i % rows  # зацикливание для краев
                                    j_mod = j % cols
                                    if kmap[i_mod][j_mod] == 1:
                                        ones.append((i_mod, j_mod))
                            if len(ones) == size and ones:
                                # Проверяем, покрывает ли группа новые минтермы
                                new_coverage = set(ones) - covered
                                if new_coverage:
                                    groups.append(ones)
                                    covered.update(ones)
        
        # Формируем минимизированное выражение
        result = []
        for group in groups:
            # Определяем, какие переменные фиксированы
            term = []
            for var_idx in range(n):
                var = self.new_letters_list[var_idx]
                values = set()
                for r, c in group:
                    if n == 2:
                        bin_str = f"{r}{c}"
                    elif n == 3:
                        col_bin = gray_cols[c]
                        bin_str = f"{r}{col_bin}"
                    elif n == 4:
                        row_bin = gray_rows[r]
                        col_bin = gray_cols[c]
                        bin_str = f"{row_bin}{col_bin}"
                    else:  # n == 5
                        row_bin = gray_rows[r]
                        col_bin = gray_cols[c]
                        bin_str = f"{row_bin}{col_bin}"
                    values.add(int(bin_str[var_idx]))
                if len(values) == 1:
                    val = values.pop()
                    term.append(f"{var}" if val == 1 else f"!{var}")
            if term:
                result.append("(" + "&".join(term) + ")")
        
        final_expr = "|".join(result) if result else "0"
        print("\nМинимизированная СДНФ (Карта Карно):")
        print(final_expr)
        return final_expr
    def karnaugh_map_sknf(self):
        maxterms = self.get_sknf_maxterms()
        n = len(self.new_letters_list)
        
        if not maxterms:
            print("Функция равна 1, нет макстермов для СКНФ")
            return "1"
        
        if n == 2:
            rows, cols = 2, 2
            row_vars = [self.new_letters_list[0]]
            col_vars = [self.new_letters_list[1]]
        elif n == 3:
            rows, cols = 2, 4
            row_vars = [self.new_letters_list[0]]
            col_vars = [self.new_letters_list[1], self.new_letters_list[2]]
        elif n == 4:
            rows, cols = 4, 4
            row_vars = [self.new_letters_list[0], self.new_letters_list[1]]
            col_vars = [self.new_letters_list[2], self.new_letters_list[3]]
        elif n == 5:
            rows, cols = 4, 8
            row_vars = [self.new_letters_list[0], self.new_letters_list[1]]
            col_vars = [self.new_letters_list[2], self.new_letters_list[3], self.new_letters_list[4]]
        else:
            print("Карта Карно поддерживает только 2-5 переменных")
            return None

        kmap = [[1] * cols for _ in range(rows)]
        
        gray_rows = ['0', '1'] if rows == 2 else ['00', '01', '11', '10']
        gray_cols = ['0', '1'] if cols == 2 else ['00', '01', '11', '10'] if cols == 4 else ['000', '001', '011', '010', '110', '111', '101', '100']
        
        for maxterm in maxterms:
            if n == 2:
                row = maxterm[0]
                col = maxterm[1]
            elif n == 3:
                row = maxterm[0]
                col_bin = ''.join(str(maxterm[i]) for i in [1, 2])
                col = {'00': 0, '01': 1, '11': 2, '10': 3}[col_bin]
            elif n == 4:
                row_bin = ''.join(str(maxterm[i]) for i in [0, 1])
                col_bin = ''.join(str(maxterm[i]) for i in [2, 3])
                row = {'00': 0, '01': 1, '11': 2, '10': 3}[row_bin]
                col = {'00': 0, '01': 1, '11': 2, '10': 3}[col_bin]
            else:  
                row_bin = ''.join(str(maxterm[i]) for i in [0, 1])
                col_bin = ''.join(str(maxterm[i]) for i in [2, 3, 4])
                row = {'00': 0, '01': 1, '11': 2, '10': 3}[row_bin]
                col = {'000': 0, '001': 1, '011': 2, '010': 3, '110': 4, '111': 5, '101': 6, '100': 7}[col_bin]
            kmap[row][col] = 0

        print("\nКарта Карно для СКНФ:")
        if n == 2:
            header = f"{'':4} {col_vars[0]}=0 {col_vars[0]}=1"
        elif n == 3:
            header = f"{'':4} {col_vars[0]}{col_vars[1]}=00 {col_vars[0]}{col_vars[1]}=01 {col_vars[0]}{col_vars[1]}=11 {col_vars[0]}{col_vars[1]}=10"
        elif n == 4:
            header = f"{'':4} {col_vars[0]}{col_vars[1]}=00 {col_vars[0]}{col_vars[1]}=01 {col_vars[0]}{col_vars[1]}=11 {col_vars[0]}{col_vars[1]}=10"
        else:  
            header = f"{'':4} {col_vars[0]}{col_vars[1]}{col_vars[2]}=000 {col_vars[0]}{col_vars[1]}{col_vars[2]}=001 {col_vars[0]}{col_vars[1]}{col_vars[2]}=011 {col_vars[0]}{col_vars[1]}{col_vars[2]}=010 {col_vars[0]}{col_vars[1]}{col_vars[2]}=110 {col_vars[0]}{col_vars[1]}{col_vars[2]}=111 {col_vars[0]}{col_vars[1]}{col_vars[2]}=101 {col_vars[0]}{col_vars[1]}{col_vars[2]}=100"
        print(header)
        
        for i in range(rows):
            if n == 2:
                row_label = f"{row_vars[0]}={gray_rows[i]}"
            elif n == 3:
                row_label = f"{row_vars[0]}={gray_rows[i]}"
            else:  
                row_label = f"{row_vars[0]}{row_vars[1]}={gray_rows[i]}"
            print(f"{row_label:4} {' '.join(str(kmap[i][j]) for j in range(cols))}")
        
        groups = []
        covered = set()
        
        for size in [8, 4, 2, 1]:
            if size > rows * cols:
                continue
            for r in range(rows):
                for c in range(cols):
                    for h in [1, 2, 4] if size > 1 else [1]:
                        for w in [size // h] if h * (size // h) == size else []:
                            if r + h > rows or c + w > cols:
                                continue
                            zeros = []
                            for i in range(r, r + h):
                                for j in range(c, c + w):
                                    i_mod = i % rows  # зацикливание для краев
                                    j_mod = j % cols
                                    if kmap[i_mod][j_mod] == 0:
                                        zeros.append((i_mod, j_mod))
                            if len(zeros) == size and zeros:
                                new_coverage = set(zeros) - covered
                                if new_coverage:
                                    groups.append(zeros)
                                    covered.update(zeros)
        
        result = []
        for group in groups:
            term = []
            for var_idx in range(n):
                var = self.new_letters_list[var_idx]
                values = set()
                for r, c in group:
                    if n == 2:
                        bin_str = f"{r}{c}"
                    elif n == 3:
                        col_bin = gray_cols[c]
                        bin_str = f"{r}{col_bin}"
                    elif n == 4:
                        row_bin = gray_rows[r]
                        col_bin = gray_cols[c]
                        bin_str = f"{row_bin}{col_bin}"
                    else:  
                        row_bin = gray_rows[r]
                        col_bin = gray_cols[c]
                        bin_str = f"{row_bin}{col_bin}"
                    values.add(int(bin_str[var_idx]))
                if len(values) == 1:
                    val = values.pop()
                    term.append(f"{var}" if val == 0 else f"!{var}")  
            if term:
                result.append("(" + "|".join(term) + ")")
        
        final_expr = "&".join(result) if result else "1"
        print("\nМинимизированная СКНФ (Карта Карно):")
        print(final_expr)
        return final_expr

def menu():
    print("\n=== Меню ===")
    print("1. Ввести функцию и вывести таблицу истинности")
    print("2. SDNF")
    print("3. SKNF")
    print("4. Индексная форма")
    print("5. Минимизировать СДНФ (расчетный метод)")
    print("6. Минимизировать СКНФ (расчетный метод)")
    print("7. Минимизировать СДНФ (расчетно-табличный)")
    print("8. Минимизировать СКНФ (расчетно-табличный)")
    print("9. Минимизировать СДНФ (Карта Карно)")
    print("10. Минимизировать СКНФ (Карта Карно)")
    print("11. Выйти")
    return input("ВВОД (1-11): ")

def main():
    current_logic = None
    
    while True:
        choice = menu()
        
        if choice == "1":
            expression = input("Введите функцию (используйте a,b,c,d,e и операторы &,|,>,!,~): ")
            try:
                current_logic = Logic_operator(expression)
                print("\nТаблица истинности создана!")
            except Exception as e:
                print(f"Ошибка в выражении: {e}")
                
        elif choice == "2":
            if current_logic is None:
                print("Сначала введите функцию")
            else:
                sdnf = current_logic.build_sdnf_str()
                print(f"SDNF: {sdnf}")
                
        elif choice == "3":
            if current_logic is None:
                print("Сначала введите функцию")
            else:
                sknf = current_logic.build_sknf_str()
                print(f"SKNF: {sknf}")
                
        elif choice == "4":
            if current_logic is None:
                print("Сначала введите функцию")
            else:
                index = current_logic.rez_index_form()
                print(f"Индексная форма (Decimal): {index}")
                
        elif choice == "5":
            if current_logic is None:
                print("Сначала введите функцию")
            else:
                current_logic.minimize_sdnf_raschetny()
                
        elif choice == "6":
            if current_logic is None:
                print("Сначала введите функцию")
            else:
                current_logic.minimize_sknf_raschetny()
                
        elif choice == "7":
            if current_logic is None:
                print("Сначала введите функцию")
            else:
                current_logic.minimize_sdnf_raschet_table()
                
        elif choice == "8":
            if current_logic is None:
                print("Сначала введите функцию")
            else:
                current_logic.minimize_sknf_raschet_table()
                
        elif choice == "9":
            if current_logic is None:
                print("Сначала введите функцию")
            else:
                current_logic.karnaugh_map_sdnf()
                
        elif choice == "10":
            if current_logic is None:
                print("Сначала введите функцию")
            else:
                current_logic.karnaugh_map_sknf()
                
        elif choice == "11":
            print("Goodbye!")
            break
            
        else:
            print("Неверный выбор! Выберите 1-11")

if __name__ == "__main__":
    main()