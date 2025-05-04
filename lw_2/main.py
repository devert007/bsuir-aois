from enum import Enum
from typing import List, Dict

class Operator(Enum):
    AND = "&"
    OR = "|"
    IMPLIES = ">"
    NOT = "!"
    EQUIV = "~"

class LogicProcessor:
    def __init__(self, expression: str):
        self.operators = {op.value for op in Operator}
        self.variables = {"a", "b", "c", "d"}
        self.expression = expression
        self.var_list = sorted({c for c in expression if c in self.variables and c not in self.operators})
        self.table = self._init_table()
        self.rpn = self._build_rpn()
        self._populate_table()
        self._display_table()

    def _init_table(self) -> List[List[str]]:
        rows = len(self.var_list)
        cols = 2**rows + 1
        table = [[None] * cols for _ in range(rows)]
        for i, var in enumerate(self.var_list):
            table[i][0] = var
        return table

    def _to_binary(self, num: int, length: int) -> str:
        return format(num, f"0{length}b")

    def _populate_table(self):
        rows = len(self.var_list)
        for i in range(2**rows):
            binary = self._to_binary(i, rows)
            for j, bit in enumerate(binary):
                self.table[j][i + 1] = bit

    def _build_rpn(self) -> str:
        precedence = {
            Operator.NOT.value: 3,
            Operator.AND.value: 2,
            Operator.OR.value: 2,
            Operator.IMPLIES.value: 2,
            Operator.EQUIV.value: 2,
            "(": 1,
        }
        stack = []
        output = []
        for char in self.expression:
            if char in self.var_list:
                output.append(char)
            elif char == "(":
                stack.append(char)
            elif char == ")":
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
                stack.pop()  # Remove "("
            elif char in self.operators:
                while stack and precedence.get(stack[-1], 0) >= precedence[char]:
                    output.append(stack.pop())
                stack.append(char)
        while stack:
            output.append(stack.pop())
        print(f"RPN: {''.join(output)}")
        return "".join(output)

    def _evaluate_rpn(self, values: Dict[str, int]) -> int:
        stack = []
        for char in self.rpn:
            if char in self.var_list:
                stack.append(values[char])
            elif char == Operator.NOT.value:
                val = stack.pop()
                stack.append(0 if val == 1 else 1)
            else:
                b, a = stack.pop(), stack.pop()
                if char == Operator.AND.value:
                    stack.append(a & b)
                elif char == Operator.OR.value:
                    stack.append(a | b)
                elif char == Operator.IMPLIES.value:
                    stack.append(1 if not a or b else 0)
                elif char == Operator.EQUIV.value:
                    stack.append(1 if a == b else 0)
        return stack[0]

    def _populate_table(self):
        rows = len(self.var_list)
        total_rows = rows
        for col in range(1, 2**rows + 1):
            values = {self.table[i][0]: int(self.table[i][col]) for i in range(rows)}
            result = self._evaluate_rpn(values)
            if col == 1:
                self.table.append([None] * (2**rows + 1))
                self.table[-1][0] = self.expression
            self.table[total_rows][col] = str(result)

    def _display_table(self):
        print(f"Variables: {''.join(self.var_list)}")
        for i in range(2**len(self.var_list)):
            print(self._to_binary(i, len(self.var_list)))
        header = " ".join(row[0] for row in self.table)
        print(header)
        for col in range(1, 2**len(self.var_list) + 1):
            row = " ".join(row[col] for row in self.table)
            print(row)

    def get_sdnf(self) -> str:
        result = []
        for col in range(1, 2**len(self.var_list) + 1):
            if self.table[-1][col] == "1":
                term = []
                for i, var in enumerate(self.var_list):
                    val = self.table[i][col]
                    if val == "0":
                        term.append(f"!{var}")
                    else:
                        term.append(var)
                result.append(f"({'&'.join(term)})")
        return f"({'|'.join(result)})" if result else "()"

    def get_sknf(self) -> str:
        result = []
        for col in range(1, 2**len(self.var_list) + 1):
            if self.table[-1][col] == "0":
                term = []
                for i, var in enumerate(self.var_list):
                    val = self.table[i][col]
                    if val == "1":
                        term.append(f"!{var}")
                    else:
                        term.append(var)
                result.append(f"({'|'.join(term)})")
        return f"({'&'.join(result)})" if result else "()"

    def get_index_form(self) -> int:
        result = "".join(self.table[-1][1:])
        return int(result, 2)

class LogicInterface:
    def __init__(self):
        self.processor = None

    def display_menu(self):
        print("\n=== Logic Evaluator ===")
        print("1. Enter expression and show truth table")
        print("2. Generate SDNF")
        print("3. Generate SKNF")
        print("4. Compute index form")
        print("5. Exit")
        return input("Select option (1-5): ")

    def run(self):
        while True:
            choice = self.display_menu()
            if choice == "1":
                expr = input("Enter logical expression (use a,b,c,d and &,|,>,!,~): ")
                try:
                    self.processor = LogicProcessor(expr)
                    print("Truth table generated!")
                except Exception as e:
                    print(f"Invalid expression: {e}")
            elif choice == "2":
                if not self.processor:
                    print("Please enter an expression first.")
                else:
                    print(f"SDNF: {self.processor.get_sdnf()}")
            elif choice == "3":
                if not self.processor:
                    print("Please enter an expression first.")
                else:
                    print(f"SKNF: {self.processor.get_sknf()}")
            elif choice == "4":
                if not self.processor:
                    print("Please enter an expression first.")
                else:
                    print(f"Index form: {self.processor.get_index_form()}")
            elif choice == "5":
                print("Exiting...")
                break
            else:
                print("Invalid option. Choose 1-5.")

if __name__ == "__main__":
    LogicInterface().run()