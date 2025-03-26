class Binary_translate:
    EXPONENTA_LENGTH = 8
    MANTISSA_LEN = 23
    def reverse(self,value):
        if value % 2 == 1:
            return 0
        else :
            return 1

    def get_bin(self,value):
        result_direct_bin = ''
        abs_value= abs(value)
        while abs_value > 0 :
            result_direct_bin= str(abs_value % 2)+result_direct_bin
            abs_value = abs_value // 2 


        return result_direct_bin
    
    def get_direct_bin(self,value):
        result_direct_bin=self.get_bin(value)
        if value < 0:
            result_direct_bin='1'+result_direct_bin
        else :
            result_direct_bin='0'+result_direct_bin

        return result_direct_bin   

    def get_reverse_bin (self,value):
        result_reverse_bin = ''
        abs_value= abs(value)
        while abs_value > 0 :
            if value < 0:
                result_reverse_bin=str(self.reverse(abs_value))+result_reverse_bin
            else:
                result_reverse_bin= str(abs_value % 2)+result_reverse_bin
            abs_value = abs_value // 2
        if value < 0:
            result_reverse_bin='1'+result_reverse_bin
        else :
            result_reverse_bin='0'+result_reverse_bin
        return result_reverse_bin

    def get_add_bin (self,value):
        result_additional_bin=''
        result_direct_bin=''
        abs_value= abs(value)
        abs_neg_increased_by_one= abs_value-1 
        while abs_value > 0 :
            result_direct_bin= str(abs_value % 2)+result_direct_bin
            if value < 0:
                result_additional_bin=str(self.reverse( abs_neg_increased_by_one))+result_additional_bin
            abs_value = abs_value // 2
            abs_neg_increased_by_one =  abs_neg_increased_by_one // 2   
        if value < 0:
            result_additional_bin='1'+result_additional_bin
        
        else :
            result_additional_bin='0'+result_direct_bin
        return result_additional_bin

    def dec_to_fixed_bin(self,dec_num):
        sign_result = '1' if dec_num < 0 else '0'
        dec_num = abs(dec_num)
        int_part = int(dec_num)
        bin_int = ''
        if int_part == 0:
            bin_int = '0'
        else:
            while int_part > 0:
                bin_int = str(int_part % 2) + bin_int
                int_part = int_part // 2
        fract_part = dec_num - int(dec_num)
        bin_fract = ''

        while fract_part != 0:
            fract_part *= 2
            bit = int(fract_part)
            bin_fract += str(bit)
            fract_part -= bit
        return sign_result + bin_int + ('.' + bin_fract if bin_fract else '')

    def dec_to_float_bin (self,value):
        sign_result = '1' if value < 0 else '0'
        bin_value =self.dec_to_fixed_bin(value)[1:]
        index_of_point = bin_value.index('.')
        #находим экспоненту как длину смещения точки в самое начало -1 
        if bin_value[0] == '0':
            # если целая часть равна 0, сдвигаем точку вправо
            first_one_index = bin_value.index('1')
            exponent = -(first_one_index - index_of_point)
            mantissa = bin_value[first_one_index + 1:]
        else:
            exponent = (len(bin_value[:index_of_point])-1)
            mantissa = bin_value[1:index_of_point]+bin_value[index_of_point+1:]
        exponent+=127
        exponent_bin = ''
        for _ in range(self.EXPONENTA_LENGTH):  
            exponent_bin = str(exponent % 2) + exponent_bin
            exponent = exponent // 2
        
        mantissa=mantissa.ljust(self.MANTISSA_LEN, '0')[:self.MANTISSA_LEN]
        return sign_result + exponent_bin + mantissa