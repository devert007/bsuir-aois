from bin_converter import BinaryConverter
from dec_converter import DecimalConverter
from bin_operations import BinaryOperations

class UserInterface:
    def __init__(self):
        self.bin_converter = BinaryConverter()
        self.dec_converter = DecimalConverter()
        self.bin_ops = BinaryOperations()

    def run(self):
        while True:
            print("\nВыберите действие:")
            print("1. Двоичный код числа")
            print("2. Прямой двоичный код")
            print("3. Обратный двоичный код")
            print("4. Дополнительный двоичный код")
            print("5. Двоичный код с фиксированной точкой")
            print("6. Двоичный код с плавающей точкой")
            print("7. Сумма дополнительных кодов")
            print("8. Разность дополнительных кодов")
            print("9. Произведение прямых кодов")
            print("10. Деление прямых кодов")
            print("11. Сумма чисел с плавающей точкой")
            print("Другое число для выхода")
            try:
                choice = int(input("Ваш выбор (1-11): "))
            except ValueError:
                print("Выход...")
                break

            if choice == 1:
                num = int(input("Введите число: "))
                result = self.bin_converter.to_binary(num)
                print(f"Результат: {result}")
                print(f"Проверка: {self.dec_converter.binary_to_decimal(result)}")

            elif choice == 2:
                num = int(input("Введите число: "))
                result = self.bin_converter.direct_code(num)
                print(f"Результат: {result}")
                print(f"Проверка: {self.dec_converter.direct_to_decimal(result)}")

            elif choice == 3:
                num = int(input("Введите число: "))
                result = self.bin_converter.inverse_code(num)
                print(f"Результат: {result}")
                print(f"Проверка: {self.dec_converter.inverse_to_decimal(result)}")

            elif choice == 4:
                num = int(input("Введите число: "))
                result = self.bin_converter.additional_code(num)
                print(f"Результат: {result}")
                print(f"Проверка: {self.dec_converter.additional_to_decimal(result)}")

            elif choice == 5:
                num = float(input("Введите число: "))
                result = self.bin_converter.fixed_point_binary(num)
                print(f"Результат: {result}")
                print(f"Проверка: {self.dec_converter.fixed_to_decimal(result)}")

            elif choice == 6:
                num = float(input("Введите число: "))
                result = self.bin_converter.floating_point_binary(num)
                print(f"Результат: {result}")
                print(f"Проверка: {self.dec_converter.floating_to_decimal(result)}")

            elif choice == 7:
                num1 = int(input("Введите первое число: "))
                num2 = int(input("Введите второе число: "))
                print(f"Результат: {self.bin_ops.add_additional_codes(num1, num2)}")

            elif choice == 8:
                num1 = int(input("Введите первое число: "))
                num2 = int(input("Введите второе число: "))
                print(f"Результат: {self.bin_ops.subtract_additional_codes(num1, num2)}")

            elif choice == 9:
                num1 = int(input("Введите первое число: "))
                num2 = int(input("Введите второе число: "))
                print(f"Результат: {self.bin_ops.multiply_direct_codes(num1, num2)}")

            elif choice == 10:
                num1 = int(input("Введите делимое: "))
                num2 = int(input("Введите делитель: "))
                print(f"Результат: {self.bin_ops.divide_direct_codes(num1, num2)}")

            elif choice == 11:
                num1 = float(input("Введите первое число: "))
                num2 = float(input("Введите второе число: "))
                print(f"Результат: {self.bin_ops.add_floating_point(num1, num2)}")

            else:
                print("Выход...")
                break

if __name__ == "__main__":
    UserInterface().run()