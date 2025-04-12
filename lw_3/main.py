class Logic_operator:
    def __init__(self,func_str:str):
        self.operaions_array=["&",">","|","!","~"]
        self.letters_array=["a","b","c","d"]
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
                    op1=int(val_dict[stack_list[0]])
                    op2=int(val_dict[stack_list[1]])
                    match(char_el):
                        case '&': rez=str(op1 * op2)
                        case'|': rez= str(op1 | op2)
                        case'>': rez=str(int(not (bool(op1)) or bool(op2)))
                        case'~':rez=str(int(op1==op2))
                    if num_str==1:
                        self.truth_table.append([0]*(pow(2,len(self.new_letters_list))+1))
                        self.truth_table[len(self.truth_table)-1][0]=stack_list[0]+char_el+stack_list[1]
                    count_operaions_array+=1
                    self.truth_table[count_operaions_array][num_str]=rez
                    val_dict[self.truth_table[count_operaions_array][0]]=self.truth_table[count_operaions_array][num_str]
                    stack_list.append(stack_list[0]+char_el+stack_list[1])
                    stack_list.pop(1)
                    stack_list.pop(0)
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

    def raschetny_metod(self):
        minterms = self.get_sdnf_minterms() 
        print(minterms)
        # to_glu_array = []
        # for i in range(0,len(minterms),1):
        #     for j in range(i,len(minterms),1):
        #         diff_count = sum(1 for a, b in zip(minterms[i], minterms[j]) if a != b)
        #         if diff_count == 1:
        #             glued = self.glue_arrays(minterms[i], minterms[j])
        #             if glued not in to_glu_array: 
        #                 to_glu_array.append(glued)
        #                 print(f"Склеиваем {minterms[i]} и {minterms[j]} → {glued}")

    def glue_arrays(self,arr_1,arr_2):
        new_arr = []
        for a, b in zip(arr_1, arr_2):
            if a != b:
                new_arr.append('x')  
            else:
                new_arr.append(a)    
        return new_arr
    # def minimize_sdnf(self):
    #     minterms = self.get_sdnf_minterms()
    #     n = len(self.new_letters_list)
    #     minterm_strs = [''.join(map(str, m)) for m in minterms]

    #     # Функция для склеивания двух импликант
    #     def glue(p, q):
    #         diff = -1
    #         for i in range(n):
    #             if p[i] != q[i]:
    #                 if diff != -1:
    #                     return None  # Больше одного различия
    #                 diff = i
    #         if diff == -1:
    #             return None  # Одинаковые импликанты
    #         glued = list(p)
    #         glued[diff] = 'X'
    #         return ''.join(glued)

    #     # Функция для преобразования импликанты в выражение
    #     def implicant_to_expr(imp):
    #         expr = []
    #         for i, val in enumerate(imp):
    #             if val == '0':
    #                 expr.append('!' + self.new_letters_list[i])
    #             elif val == '1':
    #                 expr.append(self.new_letters_list[i])
    #         return ' & '.join(expr) if expr else '1'

    #     # Склеивание импликант
    #     implicants = set(minterm_strs)
    #     all_implicants = set()
    #     while implicants:
    #         next_implicants = set()
    #         used = set()
    #         for p in implicants:
    #             for q in implicants:
    #                 if p != q:
    #                     glued = glue(p, q)
    #                     if glued:
    #                         next_implicants.add(glued)
    #                         used.add(p)
    #                         used.add(q)
    #         all_implicants.update(implicants - used)
    #         implicants = next_implicants

    #     # Для простоты считаем все импликанты необходимыми
    #     final_implicants = all_implicants

    #     # Формирование минимизированного выражения
    #     exprs = [implicant_to_expr(imp) for imp in final_implicants]
    #     minimized_sdnf = ' | '.join(exprs) if exprs else '0'
    #     print(f"Минимизированная СДНФ: {minimized_sdnf.replace(' & ','')}")





def menu():
    print("\n=== Меню ===")
    print("1. ввести функцию и вывести таблицу истинности")
    print("2. SDNF ")
    print("3. SKNF ")
    print("4. Индексная форма ")
    print("5. Минимизировать СДНФ")  # Новая опция
    print("6. Выйти")  # Изменяем нумерацию
    return input("ВВОД (1-6): ")

def main():
    current_logic = None
    
    while True:
        choice = menu()
        
        if choice == "1":
            expression = input("Введите функцию (используйте a,b,c,d и операторы &,|,>,!,~): ")
            try:
                current_logic = Logic_operator(expression)
                print("\nТаблица истинности создана!")
            except Exception as e:
                print(f"Error in expression: {e}")
                
        elif choice == "2":
            if current_logic is None:
                print("Сначала введите функцию")
            else:
                sdnf = current_logic.build_sdnf_str()
                print(f"SDNF: {sdnf}")
                minterms = current_logic.get_sdnf_minterms()
                print(f"Минтермы СДНФ: {minterms}")
                
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
                current_logic.raschetny_metod() 
                
        elif choice == "6":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice! Please select 1-6")

main()

