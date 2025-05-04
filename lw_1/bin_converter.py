import math

class BinaryConverter:
    EXP_BITS = 8
    MANT_BITS = 23

    @staticmethod
    def _flip_bit(bit):
        return 1 if bit == 0 else 0

    def to_binary(self, num):
        if num == 0:
            return "0"
        binary = []
        abs_num = abs(num)
        while abs_num:
            binary.append(str(abs_num & 1))
            abs_num >>= 1
        return "".join(binary[::-1])

    def direct_code(self, num):
        binary = self.to_binary(abs(num))
        sign = "1" if num < 0 else "0"
        return sign + binary

    def inverse_code(self, num):
        binary = []
        abs_num = abs(num)
        sign = "1" if num < 0 else "0"
        while abs_num:
            bit = abs_num & 1
            binary.append(str(self._flip_bit(bit) if num < 0 else bit))
            abs_num >>= 1
        return sign + "".join(binary[::-1])

    def additional_code(self, num):
        if num >= 0:
            return self.direct_code(num)
        binary = []
        abs_num = abs(num) - 1
        sign = "1"
        while abs_num:
            binary.append(str(self._flip_bit(abs_num & 1)))
            abs_num >>= 1
        return sign + "".join(binary[::-1])

    def fixed_point_binary(self, value):
        sign = "1" if value < 0 else "0"
        value = abs(value)
        integer = int(value)
        fractional = value - integer
        bin_int = self.to_binary(integer) or "0"
        bin_frac = []
        while fractional and len(bin_frac) < 32:  # Prevent infinite loop
            fractional *= 2
            bit = int(fractional)
            bin_frac.append(str(bit))
            fractional -= bit
        frac_str = "".join(bin_frac)
        return sign + bin_int + (f".{frac_str}" if frac_str else "")

    def floating_point_binary(self, value):
        sign = "1" if value < 0 else "0"
        if value == 0:
            return sign + "0" * (self.EXP_BITS + self.MANT_BITS)
        fixed_bin = self.fixed_point_binary(abs(value))[1:]  # Remove sign
        point_idx = fixed_bin.find(".")
        if point_idx == -1:
            point_idx = len(fixed_bin)
        binary = fixed_bin.replace(".", "")
        first_one = binary.find("1")
        if first_one == -1:
            return sign + "0" * (self.EXP_BITS + self.MANT_BITS)
        if binary[0] == "1":
            exponent = point_idx - 1
            mantissa = binary[1:point_idx] + binary[point_idx:]
        else:
            exponent = -(first_one - point_idx)
            mantissa = binary[first_one + 1 :]
        exponent += 127
        exp_bin = format(exponent, f"0{self.EXP_BITS}b")
        mantissa = mantissa.ljust(self.MANT_BITS, "0")[:self.MANT_BITS]
        return sign + exp_bin + mantissa