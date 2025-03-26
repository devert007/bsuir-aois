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








def menu():
    print("\n=== Меню ===")
    print("1. ввести функцию и вывести таблицу истинности")
    print("2.SDNF ")
    print("3.SKNF ")
    print("4. Индексная форма ")
    print("5. Выйти")
    return input("ВВОД (1-5): ")

def main():
    current_logic = None
    
    while True:
        choice = menu()
        
        if choice == "1":
            expression = input("Введите функцию (используйте a,b,c,d и операторы &,|,>,!,~): ")
            try:
                current_logic = Logic_operator(expression)
                print("\nTТаблица истинности создана!")
            except Exception as e:
                print(f"Error in expression: {e}")
                
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
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice! Please select 1-5")



main()

