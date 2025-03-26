class Decimal_translate:
    def reverse(self,value):
        if value % 2 == 1:
            return 0
        else :
            return 1

    def fixed_bin_to_dec(self,bin_str):
        if '.' in bin_str:
            int_part,fraction_part = bin_str.split('.') #разделим на две части 
        else :
            int_part, fraction_part = bin_str,False
        
        degree=0
        dec_int = 0
        dec_fraction = 0
        for i in range(len(int_part)-1,0,-1):
            dec_int += int(int_part[i])*2**degree
            degree+=1
        if fraction_part:
            for i in range(len(fraction_part)):
                bit = fraction_part[i] 
                dec_fraction += int(bit) * (0.5 ** (i + 1))

        return dec_int + dec_fraction   

    def bin_to_dec(self,value):
        result =0
        degree=0
        for i in range(len(value)-1,-1,-1):
            result += int(value[i])*2**degree
            degree+=1
        return result
    def fixed_bin_to_dec(self,bin_str):
        if '.' in bin_str:
            int_part,fraction_part = bin_str.split('.')
        else :
            int_part, fraction_part = bin_str,False
        
        degree=0
        dec_int = 0
        dec_fraction = 0
        for i in range(len(int_part)-1,0,-1):
            dec_int += int(int_part[i])*2**degree
            degree+=1
        if fraction_part:
            for i in range(len(fraction_part)):
                bit = fraction_part[i] 
                dec_fraction += int(bit) * (0.5**(i + 1))

        return dec_int + dec_fraction

    def direct_bin_to_dec(self,value):
        value_sign = value[0]
        result =0
        degree=0
        for i in range(len(value)-1,0,-1):
            result += int(value[i])*2**degree
            degree+=1
        sign_result = '-' if value_sign=='1' else ''
        return sign_result + str(result)

    def reverse_bin_to_dec(self,value):
        value_sign = value[0]
        result =0
        degree=0
        for i in range(len(value)-1,0,-1):
            result +=self.reverse(int(value[i]))*2**degree
            degree+=1
        sign_result = '-' if value_sign=='1' else ''
        return sign_result + str(result)

    def additional_bin_to_dec(self,value):
        result= self.reverse_bin_to_dec(value)
        if value[0]=='1':
            result=int(result)-1
        else:
            result=int(result)+1
        return str(result)

    def float_bin_to_dec(self,value):
        sign, exp, mant = value[0], value[1:9], value[9:]
        exp_int = int(exp,2)-127
        result_mant=0
        k=-1
        for i in range(len(mant)):
            result_mant+=int(mant[i]) *2**(k)
            k-=1
        return((-1)**int(sign) * (result_mant+1)*2**exp_int)


  
