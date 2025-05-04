class DecimalConverter:
    @staticmethod
    def _invert_bit(bit):
        return 0 if bit == 1 else 1

    def binary_to_decimal(self, binary):
        if not binary:
            return 0
        result = 0
        for bit in binary:
            result = result * 2 + int(bit)
        return result

    def fixed_to_decimal(self, binary):
        sign = -1 if binary[0] == "1" else 1
        binary = binary[1:] if binary[0] in "01" else binary
        if "." not in binary:
            return sign * self.binary_to_decimal(binary)
        int_part, frac_part = binary.split(".")
        int_val = self.binary_to_decimal(int_part)
        frac_val = 0
        for i, bit in enumerate(frac_part, 1):
            frac_val += int(bit) / (2**i)
        return sign * (int_val + frac_val)

    def direct_to_decimal(self, binary):
        if not binary:
            return "0"
        sign = "-" if binary[0] == "1" else ""
        return sign + str(self.binary_to_decimal(binary[1:]))

    def inverse_to_decimal(self, binary):
        if not binary:
            return "0"
        sign = "-" if binary[0] == "1" else ""
        result = 0
        for i, bit in enumerate(binary[1:][::-1]):
            result += self._invert_bit(int(bit)) * (2**i)
        return sign + str(result)

    def additional_to_decimal(self, binary):
        if not binary:
            return "0"
        inverse = self.inverse_to_decimal(binary)
        value = int(inverse.lstrip("-"))
        if binary[0] == "1":
            return str(value - 1)
        return str(value + 1)

    def floating_to_decimal(self, binary):
        if len(binary) < 32:
            return 0
        sign = -1 if binary[0] == "1" else 1
        exponent = int(binary[1:9], 2) - 127
        mantissa = 1.0
        for i, bit in enumerate(binary[9:], 1):
            mantissa += int(bit) / (2**i)
        return sign * mantissa * (2**exponent)