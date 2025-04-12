from logic_operator import LogicOperator
from truth_table import TruthTable
from opz_converter import OPZConverter
from sdnf_builder import SDNFBuilder
from sknf_builder import SKNFBuilder
from index_form import IndexForm
from minimizer import Minimizer
from menu import menu

class LogicProcessor:
    def __init__(self, expression):
        self.logic_op = LogicOperator(expression)
        self.truth_table = TruthTable(self.logic_op.new_letters_list)
        self.truth_table.fill_table()
        self.opz_converter = OPZConverter(
            self.logic_op.func_str,
            self.logic_op.operations_array,
            self.logic_op.new_letters_list
        )
        self._compute_expression()
        self.sdnf_builder = SDNFBuilder(self.truth_table.truth_table, self.logic_op.new_letters_list)
        self.sknf_builder = SKNFBuilder(self.truth_table.truth_table, self.logic_op.new_letters_list)
        self.index_form = IndexForm(self.truth_table.truth_table)
        self.minimizer = Minimizer(self.logic_op.new_letters_list, self.truth_table.truth_table)

    def _compute_expression(self):
        stack = []
        val_dict = {}
        additional_rows = []
        for col in range(1, len(self.truth_table.truth_table[0])):
            count_operations = len(self.logic_op.new_letters_list) - 1
            for row in range(len(self.logic_op.new_letters_list)):
                val_dict[self.truth_table.truth_table[row][0]] = self.truth_table.truth_table[row][col]
            for char in self.opz_converter.opz:
                if char in self.logic_op.new_letters_list:
                    stack.append(char)
                elif char == "!":
                    op1 = int(val_dict[stack[-1]])
                    rez = "0" if op1 == 1 else "1"
                    if col == 1:
                        additional_rows.append([0] * (pow(2, len(self.logic_op.new_letters_list)) + 1))
                        additional_rows[-1][0] = char + stack[-1]
                    count_operations += 1
                    additional_rows[count_operations - len(self.logic_op.new_letters_list)][col] = rez
                    val_dict[char + stack[-1]] = rez
                    stack.append(char + stack[-1])
                    stack.pop(-2)
                else:
                    op1 = int(val_dict[stack[-2]])
                    op2 = int(val_dict[stack[-1]])
                    if char == "&":
                        rez = str(op1 * op2)
                    elif char == "|":
                        rez = str(op1 | op2)
                    elif char == ">":
                        rez = str(int(not op1 or op2))
                    elif char == "~":
                        rez = str(int(op1 == op2))
                    if col == 1:
                        additional_rows.append([0] * (pow(2, len(self.logic_op.new_letters_list)) + 1))
                        additional_rows[-1][0] = stack[-2] + char + stack[-1]
                    count_operations += 1
                    additional_rows[count_operations - len(self.logic_op.new_letters_list)][col] = rez
                    val_dict[stack[-2] + char + stack[-1]] = rez
                    stack.append(stack[-2] + char + stack[-1])
                    stack.pop(-3)
                    stack.pop(-2)
            stack.clear()
            val_dict.clear()
        self.truth_table.truth_table.extend(additional_rows)
        print("\nOPZ:", self.opz_converter.opz)
        self.truth_table.print_table()

def main():
    current_processor = None
    while True:
        choice = menu()
        if choice == "1":
            expression = input("Enter function (use a,b,c,d,e and operators &,|,>,!,~): ")
            try:
                current_processor = LogicProcessor(expression)
                print("\nTruth table created!")
            except Exception as e:
                print(f"Error in expression: {e}")
        elif choice in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            if current_processor is None:
                print("Please enter a function first")
                continue
            if choice == "2":
                print(f"SDNF: {current_processor.sdnf_builder.build_sdnf()}")
            elif choice == "3":
                print(f"SKNF: {current_processor.sknf_builder.build_sknf()}")
            elif choice == "4":
                print(f"Index form (Decimal): {current_processor.index_form.compute_index()}")
            elif choice == "5":
                current_processor.minimizer.minimize_sdnf_raschetny(current_processor.sdnf_builder.get_minterms())
            elif choice == "6":
                current_processor.minimizer.minimize_sknf_raschetny(current_processor.sknf_builder.get_maxterms())
            elif choice == "7":
                current_processor.minimizer.minimize_sdnf_raschet_table(current_processor.sdnf_builder.get_minterms())
            elif choice == "8":
                current_processor.minimizer.minimize_sknf_raschet_table(current_processor.sknf_builder.get_maxterms())
            elif choice == "9":
                current_processor.minimizer.karnaugh_map_sdnf(current_processor.sdnf_builder.get_minterms())
            elif choice == "10":
                current_processor.minimizer.karnaugh_map_sknf(current_processor.sknf_builder.get_maxterms())
        elif choice == "11":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please select 1-11")

if __name__ == "__main__":
    main()