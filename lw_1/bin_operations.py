from bin_converter import BinaryConverter
from dec_converter import DecimalConverter

class BinaryOperations:
    PRECISION = 5
    MANTISSA_BITS = 23

    def __init__(self):
        self.bin_conv = BinaryConverter()
        self.dec_conv = DecimalConverter()

    def binary_add(self, bin1, bin2, length):
        result = []
        carry = 0
        bin1 = bin1.rjust(length, "0")
        bin2 = bin2.rjust(length, "0")
        for i in range(length - 1, -1, -1):
            bit_sum = int(bin1[i]) + int(bin2[i]) + carry
            result.append(str(bit_sum % 2))
            carry = bit_sum // 2
        if carry:
            result.append("1")
        return "".join(result[::-1])

    def add_additional_codes(self, num1, num2):
        code1 = self.bin_conv.additional_code(num1)
        code2 = self.bin_conv.additional_code(num2)
        max_len = max(len(code1), len(code2))
        code1 = code1.rjust(max_len, "1" if num1 < 0 else "0")
        code2 = code2.rjust(max_len, "1" if num2 < 0 else "0")
        result = self.binary_add(code1, code2, max_len)
        return result[-8:] if len(result) > 8 else result

    def subtract_additional_codes(self, num1, num2):
        return self.add_additional_codes(num1, -num2)

    def multiply_direct_codes(self, num1, num2):
        bin1 = self.bin_conv.to_binary(abs(num1))
        bin2 = self.bin_conv.to_binary(abs(num2))
        result = "0"
        for i, bit in enumerate(bin1[::-1]):
            if bit == "1":
                shifted = bin2 + "0" * i
                result = self.binary_add(result.rjust(len(shifted), "0"), shifted, len(shifted))
        sign = "0" if (num1 >= 0 and num2 >= 0) or (num1 < 0 and num2 < 0) else "1"
        return sign + result

    def divide_direct_codes(self, num1, num2):
        if num2 == 0:
            raise ValueError("Division by zero")
        bin1 = self.bin_conv.to_binary(abs(num1))
        bin2 = self.bin_conv.to_binary(abs(num2))
        sign = "0" if (num1 >= 0 and num2 >= 0) or (num1 < 0 and num2 < 0) else "1"
        quotient = []
        remainder = ""
        for bit in bin1:
            remainder += bit
            rem_val = self.dec_conv.binary_to_decimal(remainder)
            div_val = self.dec_conv.binary_to_decimal(bin2)
            if rem_val >= div_val:
                quotient.append("1")
                remainder = self.bin_conv.to_binary(rem_val - div_val)
            else:
                quotient.append("0")
        quotient = "".join(quotient).lstrip("0") or "0"
        if remainder != "0":
            quotient += "."
            for _ in range(self.PRECISION):
                remainder += "0"
                rem_val = self.dec_conv.binary_to_decimal(remainder)
                if rem_val >= div_val:
                    quotient += "1"
                    remainder = self.bin_conv.to_binary(rem_val - div_val)
                else:
                    quotient += "0"
        return sign + quotient

    def add_floating_point(self, val1, val2):
        bin1 = self.bin_conv.floating_point_binary(val1)
        bin2 = self.bin_conv.floating_point_binary(val2)
        s1, e1, m1 = bin1[0], bin1[1:9], "1" + bin1[9:]
        s2, e2, m2 = bin2[0], bin2[1:9], "1" + bin2[9:]
        exp1 = int(e1, 2)
        exp2 = int(e2, 2)
        if exp1 > exp2:
            shift = exp1 - exp2
            m2 = "0" * shift + m2
            exp2 = exp1
        elif exp2 > exp1:
            shift = exp2 - exp1
            m1 = "0" * shift + m1
            exp1 = exp2
        mantissa = self.binary_add(m1, m2, max(len(m1), len(m2)))
        if len(mantissa) > max(len(m1), len(m2)):
            exp1 += len(mantissa) - max(len(m1), len(m2))
            mantissa = mantissa[1:]
        if len(mantissa) > self.MANTISSA_BITS:
            if mantissa[self.MANTISSA_BITS] == "1":
                one = "1".rjust(len(mantissa), "0")
                mantissa = self.binary_add(mantissa[:self.MANTISSA_BITS], one, len(mantissa))[:self.MANTISSA_BITS]
            else:
                mantissa = mantissa[:self.MANTISSA_BITS]
        if mantissa == "0" * len(mantissa):
            exp1 = 0
            mantissa = "0" * self.MANTISSA_BITS
        exp_bin = format(exp1, f"0{self.bin_conv.EXP_BITS}b")
        return s1 + exp_bin + mantissa