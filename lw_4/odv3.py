from logic_processor import LogicProcessor
from minimizer import Minimizer


class ODV_3:
  def __init__(self):
    self.letters_array=["a","b","bin"]#,"d","_BOUT"]
    self.new_letters_list=[]

    for i in self.letters_array:
        if  (i not in self.new_letters_list)&(i in self.letters_array):
            self.new_letters_list.append(i)
    self.truth_table = []
    for i in range(0,len(self.new_letters_list),1):
        self.truth_table.append([0]*(pow(2,len(self.new_letters_list))+1))
        self.truth_table[i][0]=self.new_letters_list[i]

    for i in range(0,pow(2,len(self.new_letters_list)),1):
          binary_value=self.get_binary_value(i,len(self.new_letters_list))
          bin_value = '0' if i%2==0 else '1'
          self.truth_table 
          for j in range(0,len(self.new_letters_list),1):
              self.truth_table[j][i+1]=binary_value[j]
    
    bout_formula='(!a&b)|(!a&c)|(b&c)'    
    self.bout_result = LogicProcessor(bout_formula)
    self.bout_result.truth_table.print_table()
    bout_result_array  = self.bout_result.truth_table.get_last_column()
   
    d_formula = 'a/b/c'
    self.d_result = LogicProcessor(d_formula)
    self.d_result.truth_table.print_table()
    d_result_array  = self.d_result.truth_table.get_last_column()

    self.truth_table.append(d_result_array)
    self.truth_table.append(bout_result_array)
    self.print_truth_table()
    self.print_sdnf()
    self.print_minimize()


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

  def get_binary_value(self,value,length)->str:
        direct_binary = ''
        abs_value= abs(value)
        while abs_value > 0 :
            direct_binary= str(abs_value % 2)+direct_binary
            abs_value = abs_value // 2 
        if len(direct_binary)<length:
            direct_binary=direct_binary.zfill(length)
        return direct_binary


  def print_minimize(self):
    self.d_result.minimizer.minimize_sdnf_raschetny(self.d_result.sdnf_builder.get_minterms())
    print("minimized bout:")
    self.bout_result.minimizer.minimize_sdnf_raschetny(self.bout_result.sdnf_builder.get_minterms())

  def print_sdnf(self):
    print("СДНФ:")
    print(f"D ={self.d_result.sdnf_builder.build_sdnf()}")
    print(f"BOUT ={self.bout_result.sdnf_builder.build_sdnf()}")


odv=ODV_3()