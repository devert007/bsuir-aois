from logic_processor import LogicProcessor
from minimizer import Minimizer

class D8421:
    def __init__(self):
        self.all_values = [self._get_binary_value(i, 4) for i in range(10)]
        self.n = self._get_binary_value(6, 4)
        self.D8421_n()

    def _get_binary_value(self, value, length) -> str:
        if value == 0:
            return "0" * length
        direct_binary = ""
        abs_value = abs(value)
        while abs_value > 0:
            direct_binary = str(abs_value % 2) + direct_binary
            abs_value //= 2
        return direct_binary.zfill(length)
    def bin_to_dec(self,value):
        result =0
        degree=0
        for i in range(len(value)-1,-1,-1):
            result += int(value[i])*2**degree
            degree+=1
        return result
    def _sum_binary(self, value_1, value_2):
        result = ""
        carry = 0
        for i in range(3, -1, -1):
            bit1 = int(value_1[i])
            bit2 = int(value_2[i])
            sum_bit = bit1 + bit2 + carry
            result = str(sum_bit % 2) + result
            carry = sum_bit // 2
        return result if self.bin_to_dec(result)<=9 else 'X'

    def D8421_n(self):
        self.result_plus_n=[self._sum_binary(self.n, i) for i in self.all_values]
        return self.result_plus_n
    def D8421_n_sdnf(self):
          letters_list=['A','B','C','D']
          sdnf = []
          for i in range(len(self.all_values)):
            if self.result_plus_n[i] != 'X':
                  term = []
                  for j in range(len(letters_list)):
                      if self.all_values[i][j] == '0':
                          term.append(f"!{letters_list[j]}")
                      else:
                          term.append(letters_list[j])
                      term.append("&")
                  term.pop()  
                  sdnf.append("(" + "".join(term) + ")")
                  sdnf.append("|")
          
          if sdnf:
              sdnf.pop()
              return "".join(sdnf)
          return "0"
    def print_result(self):
        print("D8421:\t\tD8421+6:")
        for i in range(10):
            print (self.all_values[i],'\t\t',self.result_plus_n[i])

    def build_sndf_for_all_y(self):
        letters_list = ['a', 'b', 'c', 'd']
        y_functions = ['0011', '1100', '1100', '0101']
        sdnf_array = []
        
        for y_index in range(4): 
            sdnf = []
            for i in range(len(self.all_values)):
                if self.result_plus_n[i] != 'X':
                    if self.result_plus_n[i][y_index] == '1':
                        term = []
                        for j in range(len(letters_list)):
                            if self.all_values[i][j] == '0':
                                term.append(f"!{letters_list[j]}")
                            else:
                                term.append(letters_list[j])
                            term.append("&")
                        term.pop()
                        sdnf.append("(" + "".join(term) + ")")
                        sdnf.append("|")
            
            if sdnf:
                sdnf.pop()  # Удаляем последний "|"
                sdnf_array.append("".join(sdnf))
            else:
                sdnf_array.append("0")
        
        return sdnf_array
                
    def minimize_all_y_by_karnaugh(self):
        sdnf_array = self.build_sndf_for_all_y()
        for i in range(len(sdnf_array)):
            print(f"\nMinimizing Y{i+1}:")
            lp = LogicProcessor(sdnf_array[i])
            minterms = lp.sdnf_builder.get_minterms()
            print(f"SDNF: {sdnf_array[i]}")
            lp.minimizer.karnaugh_map_sdnf(minterms)
            

d = D8421()
d.print_result()
print(d.D8421_n_sdnf())
print(d.build_sndf_for_all_y())
d.minimize_all_y_by_karnaugh()