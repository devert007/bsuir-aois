from decimal_bin_trans import *
from Binary_translate import *

class Binary_operator:
    ACCUR=5
    MANTISSA_LEN = 23
    dec_trans = Decimal_translate()
    bin_trans = Binary_translate()
    
    def sum_binary(self,value_1,value_2,max_len):
        result=''
        carry=0
        value_1=value_1.ljust(max_len,'0')
        value_2=value_2.ljust(max_len,'0')
        for i in range(max_len-1,-1,-1) :
            bit1 = int(value_1[i])  
            bit2 = int(value_2[i])
            sum_bit=bit1+bit2 +carry
            result =  str(sum_bit % 2) +result
            carry = sum_bit // 2 
        if carry== 1:
            result=str(carry)+result
        return result
    
    def sum_add_binary(self,value_1, value_2):
        add_val_1= self.bin_trans.get_add_bin(value_1) 
        add_val_2= self.bin_trans.get_add_bin(value_2)
        max_len = max(len(add_val_1), len(add_val_2))
        if value_1 > 0:
            add_val_1 = add_val_1.zfill(max_len)  
        else :
            add_val_1 = add_val_1.rjust(max_len,'1') 
        if value_2 > 0:  
            add_val_2 = add_val_2.zfill(max_len)
        else :
            add_val_2 = add_val_2.rjust(max_len,'1') 
        result=self.sum_binary(add_val_1,add_val_2,max_len)
        result = result[-8:]
        return result
    

    def sub_add_binary(self,value_1,value_2):
        value_2=0-value_2
        return self.sum_add_binary(value_1,value_2)

    def mult_direct_binary(self,value_1,value_2):
        dir_value_1=self.bin_trans.get_bin(value_1)
        dir_value_2=self.bin_trans.get_bin(value_2)
        product=''
        current_value=''
        for i in range(len(dir_value_1)-1,-1,-1):
            bit1 = int(dir_value_1[i])  

            if bit1 == 1: 
                current_value=dir_value_2
                for j in range(i,len(dir_value_1)-1 ,1):
                    current_value=current_value +'0'

                product=product.zfill(len(current_value)) 
                product=self.sum_binary(current_value,product,len(current_value))
            else:
                product='0'+product

        if (value_1>0 and value_2>0) or (value_1>0 and value_2>0):
            product='0'+product
        else:
            product='1'+product

        return product

    def div_direct(self,value_1, value_2):
        dir_value_1=self.bin_trans.get_bin(value_1)
        dir_value_2=self.bin_trans.get_bin(value_2)
        result_sign = '1' if value_1*value_2 < 0 else '0'
        carry = ''
        result = ''
        for i in range(len(dir_value_1)):
            carry += dir_value_1[i]  
            if self.dec_trans.bin_to_dec(carry) < self.dec_trans.bin_to_dec(dir_value_2):
                result += '0'
            else:
                result += '1'
                carry = self.bin_trans.get_bin(self.dec_trans.bin_to_dec(carry) - self.dec_trans.bin_to_dec(dir_value_2))

        # делаем точность 5 sign 
        if self.dec_trans.bin_to_dec(carry) != 0:
                result += '.'
                for _ in range(self.ACCUR):
                    carry += '0'
                    if self.dec_trans.bin_to_dec(carry) < self.dec_trans.bin_to_dec(dir_value_2):
                        result += '0'
                    else:
                        result += '1'
                        carry = self.bin_trans.get_bin(self.dec_trans.bin_to_dec(carry) - self.dec_trans.bin_to_dec(dir_value_2))
        result = result.lstrip('0') #лишние нули в начале удаляем
        return result_sign+result 

    def sum_binary_float(self,value_1, value_2):
        value_1= self.bin_trans.dec_to_float_bin(value_1)
        value_2= self.bin_trans.dec_to_float_bin(value_2)
        sign_1, exp1, mant_1 = value_1[0], value_1[1:9], value_1[9:]
        sign_2, exp2, mant_2 = value_2[0], value_2[1:9], value_2[9:]
        exp_1_int = int(exp1, 2)
        exp_2_int = int(exp2, 2)
        result_mant=''
        mant_2 = '1' + mant_2
        mant_1= '1' + mant_1

        if exp_1_int > exp_2_int:
            shift = exp_1_int - exp_2_int
            for i in range (0,shift-1,1):
                mant_2 = '0'+ mant_2 
            mant_2 = '0' + mant_2
            exp_2_int = exp_1_int
        
        elif exp_2_int > exp_1_int:
            shift = exp_2_int - exp_1_int
            for i in range (0,shift-1,1):
                mant_1 = '0'+ mant_1
            mant_1 = '0' + mant_1
            exp_1_int = exp_2_int
        result_mant =self.sum_binary(mant_1, mant_2,max(len(mant_1),len(mant_2)))
        result_sign = sign_1
        if len(result_mant) > max(len(mant_1),len(mant_2)):
            shift_1= len(result_mant)-max(len(mant_1),len(mant_2))
            exp_1_int+=shift_1
        result_mant=result_mant[1:]

        #округляем
        if len(result_mant) > self.MANTISSA_LEN :
            if (result_mant[self.MANTISSA_LEN ] == '1'):
                result_mant=result_mant[:self.MANTISSA_LEN ]
                one_to_add='1'
                one_to_add=one_to_add.zfill(len(result_mant))
                result_mant=self.sum_binary(result_mant,one_to_add,len(result_mant))
            result_mant=result_mant[:self.MANTISSA_LEN ]
        
        if result_mant == '0':
            result_mant = '0' * self.MANTISSA_LEN 
            exp_1_int = 0
        
        result_exp = self.bin_trans.get_bin(exp_1_int)
        return f"{result_sign}{result_exp}{result_mant}"


# test_1 = Binary_operator()
# test_1.div_direct(12,2)