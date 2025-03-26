from Binary_translate import *
from decimal_translator import *
from Binary_operators import * 

class Menu:
    translator_bin = Binary_translate()
    translator_dec = Decimal_translate()
    binary_op = Binary_operator()  
    
    def __init__(self):
        is_cycle = True
        while(is_cycle):
            user_choice = int(input("Выберите операцию:\n1.Получить двоичный код\n2.Получить прямой двоичный код\n3.Получить обратный двоичный код\n4.Получить дополнительный двоичный код\n5.Получить двоичный код с фиксированной точкой\n6.Получить двоичный код с плавающей точкой\n7.Получить сумму дополнительных двоичных кодов\n8.Получить разность дополнительных двоичных кодов\n9.Получить произведение прямых двоичных кодов\n10.Разделить двоичные коды\n11.Получить сумму двоичных кодов с плавающей точкой\nВведите ваш выбор (1-11, или любое другое число для выхода): "))
            
            if user_choice == 1:
                value = int(input('Введите значение для перевода: '))
                print(self.translator_bin.get_bin(value))
                print("для проверки: ",self.translator_dec.bin_to_dec(self.translator_bin.get_bin(value)))
                continue
                
            elif user_choice == 2:
                value = int(input('Введите значение для перевода в прямой двоичный код: '))
                print(self.translator_bin.get_direct_bin(value))
                print("для проверки: ",self.translator_dec.direct_bin_to_dec(self.translator_bin.get_direct_bin(value)))
                continue
                
            elif user_choice == 3:
                value = int(input('Введите значение для перевода в обратный двоичный код: '))
                print(self.translator_bin.get_reverse_bin(value))
                print("для проверки: ",self.translator_dec.reverse_bin_to_dec(self.translator_bin.get_reverse_bin(value)))
                continue
                
            elif user_choice == 4:
                value = int(input('Введите значение для перевода в дополнительный двоичный код: '))
                print(self.translator_bin.get_add_bin(value))
                print("для проверки: ",self.translator_dec.additional_bin_to_dec(self.translator_bin.get_add_bin(value)))
                continue
                
            elif user_choice == 5:
                value = float(input('Введите значение для перевода в двоичный код с фиксированной точкой: ')) 
                print(self.translator_bin.dec_to_fixed_bin(value))
                print("для проверки: ",self.translator_dec.fixed_bin_to_dec(self.translator_bin.dec_to_fixed_bin(value)))
                continue
                
            elif user_choice == 6:
                value = float(input('Введите значение для перевода в двоичный код с плавающей точкой: '))
                print(self.translator_bin.dec_to_float_bin(value))
                print("для проверки: ",self.translator_dec.float_bin_to_dec(self.translator_bin.dec_to_float_bin(value)))
                continue
                
            elif user_choice == 7:
                value_1 = int(input('Введите первое значение для суммы: '))
                value_2 = int(input('Введите второе значение для суммы: '))
                print(self.binary_op.sum_add_binary(value_1, value_2))
                continue
                
            elif user_choice == 8:
                value_1 = int(input('Введите первое значение для вычитания: '))
                value_2 = int(input('Введите второе значение для вычитания: '))
                print(self.binary_op.sub_add_binary(value_1, value_2))
                continue
                
            elif user_choice == 9:
                value_1 = int(input('Введите первое значение для умножения: '))
                value_2 = int(input('Введите второе значение для умножения: '))
                print(self.binary_op.mult_direct_binary(value_1, value_2))
                continue
                
            elif user_choice == 10:
                value_1 = int(input('Введите делимое: '))
                value_2 = int(input('Введите делитель: '))
                print(self.binary_op.div_direct(value_1, value_2))
                continue
                
            elif user_choice == 11:
                value_1 = float(input('Введите первое значение для суммы с плавающей точкой: '))
                value_2 = float(input('Введите второе значение для суммы с плавающей точкой: '))
                print(self.binary_op.sum_binary_float(value_1, value_2))
                continue
                
            else:
                is_cycle = False
                print("Выход из программы...")

if __name__ == "__main__":
    menu = Menu()   