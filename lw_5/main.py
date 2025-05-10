from logic_processor import LogicProcessor
from minimizer import Minimizer

class DownCounterTTrigger:
    def __init__(self):
        self.literals = ['a', 'b', 'c', 'd'] 
        self.transition_table = self.build_transition_table()
        self.minimize_excitation_functions()

    def build_transition_table(self):
        table = []
        for q3_star in range(2):
            for q2_star in range(2):
                for q1_star in range(2):
                    for v in range(2):
                        state = [q3_star, q2_star, q1_star]
                        decimal = q3_star * 4 + q2_star * 2 + q1_star
                        if v == 0:
                            next_decimal = decimal
                        else:
                            next_decimal = (decimal - 1) % 8
                        q3 = (next_decimal // 4) % 2
                        q2 = (next_decimal // 2) % 2
                        q1 = next_decimal % 2
                        t3 = 1 if q3_star != q3 else 0
                        t2 = 1 if q2_star != q2 else 0
                        t1 = 1 if q1_star != q1 else 0
                        table.append(([q3_star, q2_star, q1_star, v], [q3, q2, q1], [t3, t2, t1]))
        return table

    def print_transition_table(self):
        print("Transition and Excitation Table:")
        print("a   b   c   d | q3 q2 q1 | h3 h2 h1")
        for row in self.transition_table:
            inputs, outputs, excitations = row
            print(f"{inputs[0]}   {inputs[1]}   {inputs[2]}   {inputs[3]} | "
                  f"{outputs[0]}  {outputs[1]}  {outputs[2]} | "
                  f"{excitations[0]}  {excitations[1]}  {excitations[2]}")

    def build_sdnf_for_t(self, t_index):
        sdnf = []
        for row in self.transition_table:
            inputs, _, excitations = row
            if excitations[t_index] == 1:
                term = []
                for j, literal in enumerate(self.literals):
                    if inputs[j] == 0:
                        term.append(f"!{literal}")
                    else:
                        term.append(literal)
                    term.append("&")
                term.pop()  
                sdnf.append("(" + "".join(term) + ")")
                sdnf.append("|")
        
        if sdnf:
            sdnf.pop()  
            return "".join(sdnf)
        return "0" 

    def minimize_excitation_functions(self):
        self.print_transition_table()
        
        print("\nMinimized Excitation Functions:")
        for i, t_func in enumerate(['T3', 'T2', 'T1']):
            sdnf = self.build_sdnf_for_t(i)
            print(f"\nMinimizing {t_func}:")
            print(f"SDNF: {sdnf}")
            
            if sdnf == "0":
                print(f"{t_func} is always 0 (no minterms).")
                continue
            
            try:
                lp = LogicProcessor(sdnf)
                minterms = lp.sdnf_builder.get_minterms()
                lp.minimizer.karnaugh_map_sdnf(minterms)
            except Exception as e:
                print(f"Error minimizing {t_func}: {str(e)}")
                print("Skipping minimization for this function.")

if __name__ == "__main__":
    counter = DownCounterTTrigger()

## таблица H - это таблица возбуждения памяти 
## hi - сигнал возбуждения определяются так, если входное a/b/c = q3/q2/q1, то Ti = 0, если поменялось состояние тригера изменилось на противоположное то ставим 1
## d - входной счетчик автомата
##