class Minimizer:
    def __init__(self, letters_list, truth_table):
        self.letters_list = letters_list
        self.truth_table = truth_table
        self.n = len(letters_list)

    def _minimize_common(self, terms, is_sdnf):
        if not terms:
            return "Function is always true" if is_sdnf else "Function is always false"

        current_terms = terms
        step = 1
        for term in current_terms:
            print("".join(str(x) for x in term))

        while True:
            combined_set = set()
            new_terms_set = set()

            for i in range(len(current_terms)):
                for j in range(i + 1, len(current_terms)):
                    term1, term2 = current_terms[i], current_terms[j]
                    diff = 0
                    diff_pos = -1
                    for k in range(self.n):
                        if term1[k] != term2[k]:
                            diff += 1
                            diff_pos = k
                    if diff == 1:
                        new_term = term1.copy()
                        new_term[diff_pos] = "X"
                        new_terms_set.add(tuple(new_term))
                        combined_set.add(i)
                        combined_set.add(j)

            if new_terms_set:
                print("Combined implicants:")
                for term in new_terms_set:
                    print("".join(str(x) for x in term))
            else:
                print("No more combinations possible")
                break

            result_set = set(new_terms_set)
            for i in range(len(current_terms)):
                if i not in combined_set:
                    result_set.add(tuple(current_terms[i]))
            current_terms = [list(term) for term in result_set]
            step += 1

        return current_terms

    def minimize_sdnf_raschetny(self, minterms):
        current_terms = self._minimize_common(minterms, True)
        result_expr = []
        for term in current_terms:
            term_str = []
            for i in range(len(term)):
                if term[i] == "X":
                    continue
                term_str.append(
                    f"!{self.letters_list[i]}" if term[i] == 0 else self.letters_list[i]
                )
            if term_str:
                result_expr.append("(" + "&".join(term_str) + ")")
        final_expr = "|".join(result_expr) if result_expr else "0"
        print(final_expr)
        self.result_final_expr = final_expr
        return final_expr

    def minimize_sknf_raschetny(self, maxterms):
        current_terms = self._minimize_common(maxterms, False)
        sknf_result_expr = []
        for term in current_terms:
            term_str = []
            for i in range(len(term)):
                if term[i] == "X":
                    continue
                term_str.append(
                    self.letters_list[i] if term[i] == 0 else f"!{self.letters_list[i]}"
                )
            if term_str:
                sknf_result_expr.append("(" + "|".join(term_str) + ")")
        final_expr = "&".join(sknf_result_expr) if sknf_result_expr else "1"
        self.result_sf=final_expr 
        print(final_expr)
        return final_expr

    def _build_coverage_table(self, terms, original_terms):
        table = []
        for term in terms:
            row = []
            for minterm in original_terms:
                is_covered = all(
                    term[i] == "X" or term[i] == minterm[i] for i in range(self.n)
                )
                row.append(1 if is_covered else 0)
            table.append(row)
        return table

    def minimize_sdnf_raschet_table(self, minterms):
        if not minterms:
            return "Function is always true"
        current_terms = self._minimize_common(minterms, True)
        print("\nCombined terms:")
        print(current_terms)

        table = self._build_coverage_table(current_terms, minterms)
        print("\nCoverage table:")
        col_width = max(4, max(len("".join(str(x) for x in term)) for term in minterms))
        header = ["".join(str(x) for x in term) for term in minterms]
        separator = "-" * col_width + "+" + "+".join("-" * col_width for _ in header) + "+"
        header_line = " " * col_width + "|" + "|".join(f"{h:^{col_width}}" for h in header) + "|"
        print(separator)
        print(header_line)
        print(separator)

        for i, row in enumerate(table):
            term_str = "".join(str(x) for x in current_terms[i])
            print(f"{term_str:<{col_width}}|" + "|".join(f"{x:^{col_width}}" for x in row) + "|")
        print(separator)

        result_terms = set()
        for j in range(len(minterms)):
            one_count = 0
            term_idx = -1
            for i in range(len(current_terms)):
                if table[i][j] == 1:
                    one_count += 1
                    term_idx = i
            if one_count == 1:
                result_terms.add(tuple(current_terms[term_idx]))

        print("\nEssential implicants:", result_terms)
        print("\nMinimized SDNF:")
        result_expr = []
        for term in result_terms:
            term_str = []
            for i in range(len(term)):
                if term[i] == "X":
                    continue
                term_str.append(
                    f"!{self.letters_list[i]}" if term[i] == 0 else self.letters_list[i]
                )
            if term_str:
                result_expr.append("(" + "&".join(term_str) + ")")
        final_expr = "|".join(result_expr) if result_expr else "0"
        print(final_expr)
        return final_expr

    def minimize_sknf_raschet_table(self, maxterms):
        if not maxterms:
            return "Function is always true"
        current_terms = self._minimize_common(maxterms, False)
        print("\nCombined terms:")
        print(current_terms)

        table = self._build_coverage_table(current_terms, maxterms)
        print("\nCoverage table:")
        col_width = max(4, max(len("".join(str(x) for x in term)) for term in maxterms))
        header = ["".join(str(x) for x in term) for term in maxterms]
        separator = "-" * col_width + "+" + "+".join("-" * col_width for _ in header) + "+"
        header_line = " " * col_width + "|" + "|".join(f"{h:^{col_width}}" for h in header) + "|"
        print(separator)
        print(header_line)
        print(separator)

        for i, row in enumerate(table):
            term_str = "".join(str(x) for x in current_terms[i])
            print(f"{term_str:<{col_width}}|" + "|".join(f"{x:^{col_width}}" for x in row) + "|")
        print(separator)

        result_terms = set()
        for j in range(len(maxterms)):
            one_count = 0
            term_idx = -1
            for i in range(len(current_terms)):
                if table[i][j] == 1:
                    one_count += 1
                    term_idx = i
            if one_count == 1:
                result_terms.add(tuple(current_terms[term_idx]))

        print("\nEssential implicants:", result_terms)
        print("\nMinimized SKNF:")
        result_expr = []
        for term in result_terms:
            term_str = []
            for i in range(len(term)):
                if term[i] == "X":
                    continue
                term_str.append(
                    self.letters_list[i] if term[i] == 0 else f"!{self.letters_list[i]}"
                )
            if term_str:
                result_expr.append("(" + "|".join(term_str) + ")")
        final_expr = "&".join(result_expr) if result_expr else "1"
        print(final_expr)
        return final_expr

   
    def _get_gray_code(self, n):
        """Возвращает код Грея для числа n."""
        return n ^ (n >> 1)

    def _get_possible_group_sizes(self, rows, cols):
        """Возвращает возможные размеры групп (высота, ширина)."""
        sizes = []
        row_sizes = [1] if rows == 1 else [1, 2, 4][:rows.bit_length()]
        col_sizes = [1, 2, 4, 8][:cols.bit_length()]
        for r in row_sizes:
            for c in col_sizes:
                if r * c >= 1:
                    sizes.append((r, c))
        return sizes

    def _is_power_of_two(self, x):
        """Проверяет, является ли x степенью двойки."""
        return x > 0 and (x & (x - 1)) == 0

    def _check_subgroup_validity(self, unique_rows, unique_cols):
        """Проверяет валидность подгруппы для 5 переменных."""
        row_count = len(unique_rows)
        col_count = len(unique_cols)
        return self._is_power_of_two(row_count) and self._is_power_of_two(col_count)

    def _filter_groups_for_five_variables(self, groups, kmap):
        """Фильтрует группы для случая с 5 переменными."""
        valid_groups = []
        rows, cols = len(kmap), len(kmap[0])

        for group in groups:
            unique_rows = set(group[i] for i in range(0, len(group), 2))
            unique_cols = set(group[i] for i in range(1, len(group), 2))

            is_valid = True
            if any(c in unique_cols for c in [0, 1, 2, 3]) and any(c in unique_cols for c in [4, 5, 6, 7]):
                left_cols = [c for c in unique_cols if c < 4]
                right_cols = [c for c in unique_cols if c >= 4]
                left_valid = self._check_subgroup_validity(unique_rows, left_cols)
                right_valid = self._check_subgroup_validity(unique_rows, right_cols)
                is_valid = left_valid and right_valid
            else:
                is_valid = self._check_subgroup_validity(unique_rows, unique_cols)

            if is_valid:
                valid_groups.append(group)

        return valid_groups

    def _is_subset(self, group, super_group):
        """Проверяет, является ли group подмножеством super_group."""
        group_pairs = [(group[i], group[i + 1]) for i in range(0, len(group), 2)]
        super_group_pairs = [(super_group[i], super_group[i + 1]) for i in range(0, len(super_group), 2)]
        return all(g in super_group_pairs for g in group_pairs)

    def _is_covered_by_union(self, group, all_groups):
        """Проверяет, покрывается ли group объединением других групп."""
        group_pairs = [(group[i], group[i + 1]) for i in range(0, len(group), 2)]
        united_pairs = []
        for other in all_groups:
            if other == group:
                continue
            united_pairs.extend((other[i], other[i + 1]) for i in range(0, len(other), 2))
        return all(g in united_pairs for g in group_pairs)

    def _find_additional_groups_by_mingling_maps(self, col_indexes, target_value, kmap, translation_rules):
        """Находит дополнительные группы для 5 переменных путем разбиения карты."""
        rows, cols = len(kmap), 4
        sub_kmap = [[0] * cols for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                sub_kmap[i][j] = kmap[i][col_indexes[j]]

        sub_groups = self._find_karnaugh_groups(sub_kmap, target_value, 4)
        self._translate_coordinates_from_submap(sub_groups, translation_rules)
        return sub_groups

    def _translate_coordinates_from_submap(self, sub_groups, translation_rules):
        """Переводит координаты из подкарты в общую карту."""
        for group in sub_groups:
            for j in range(1, len(group), 2):
                for rule in translation_rules:
                    if group[j] == rule[0]:
                        group[j] = rule[1]
                        break

    def _find_karnaugh_groups(self, kmap, target_value, n):
        """Находит группы в карте Карно."""
        rows, cols = len(kmap), len(kmap[0])
        groups = []
        unique_groups = set()

        dimensions = self._get_possible_group_sizes(rows, cols)
        for h, w in dimensions:
            start_rows = [0] if h == rows else range(rows)
            for s in start_rows:
                for c in range(cols):
                    cells = []
                    is_valid = True
                    for row in range(s, s + h):
                        current_row = row % rows
                        for i in range(w):
                            current_col = (c + i) % cols
                            if kmap[current_row][current_col] != target_value:
                                is_valid = False
                                break
                            cells.extend([current_row, current_col])
                        if not is_valid:
                            break
                    if is_valid and cells:
                        key = ",".join(map(str, sorted(cells)))
                        if key not in unique_groups:
                            unique_groups.add(key)
                            groups.append(cells)

        if n == 5:
            groups.extend(self._find_additional_groups_by_mingling_maps(
                [0, 3, 4, 7], target_value, kmap, [(0, 0), (1, 3), (2, 4), (3, 7)]
            ))
            groups.extend(self._find_additional_groups_by_mingling_maps(
                [1, 2, 5, 6], target_value, kmap, [(0, 1), (1, 2), (2, 5), (3, 6)]
            ))

        # Фильтрация групп
        filtered_groups = []
        sorted_groups = sorted(groups, key=lambda g: len(g), reverse=True)
        for group in sorted_groups:
            if not any(self._is_subset(group, existing) for existing in filtered_groups):
                filtered_groups.append(group)

        if n == 5:
            filtered_groups = self._filter_groups_for_five_variables(filtered_groups, kmap)

        # Удаление групп, покрываемых объединением других
        result_groups = []
        for group in filtered_groups:
            if not self._is_covered_by_union(group, filtered_groups):
                result_groups.append(group)

        return result_groups

    def _get_variable_values(self, row, col, n, gray_rows, gray_cols):
        """Возвращает значения переменных для ячейки карты Карно."""
        if n == 1:
            return [col]
        elif n == 2:
            return [row, col]
        elif n == 3:
            bc = gray_cols[col]
            return [row, int(bc[0]), int(bc[1])]
        elif n == 4:
            ab = gray_rows[row]
            cd = gray_cols[col]
            return [int(ab[0]), int(ab[1]), int(cd[0]), int(cd[1])]
        elif n == 5:
            ab = gray_rows[row]
            cde = gray_cols[col]
            return [int(ab[0]), int(ab[1]), int(cde[0]), int(cde[1]), int(cde[2])]
        return []

    def _setup_karnaugh_map(self, terms, is_sdnf):
        """Настраивает карту Карно."""
        if not terms:
            print(f"Function is {'1' if is_sdnf else '0'}, no {'minterms' if is_sdnf else 'maxterms'}")
            return None, None, None, None, None, None, None

        if self.n > 5:
            print("Karnaugh map supports only 2-5 variables")
            return None, None, None, None, None, None, None

        if self.n == 1:
            rows, cols = 1, 2
            row_vars = []
            col_vars = [self.letters_list[0]]
        elif self.n == 2:
            rows, cols = 2, 2
            row_vars = [self.letters_list[0]]
            col_vars = [self.letters_list[1]]
        elif self.n == 3:
            rows, cols = 2, 4
            row_vars = [self.letters_list[0]]
            col_vars = [self.letters_list[1], self.letters_list[2]]
        elif self.n == 4:
            rows, cols = 4, 4
            row_vars = [self.letters_list[0], self.letters_list[1]]
            col_vars = [self.letters_list[2], self.letters_list[3]]
        else:
            rows, cols = 4, 8
            row_vars = [self.letters_list[0], self.letters_list[1]]
            col_vars = [self.letters_list[2], self.letters_list[3], self.letters_list[4]]

        kmap = [[1 if not is_sdnf else 0] * cols for _ in range(rows)]
        gray_rows = ["0", "1"] if rows <= 2 else ["00", "01", "11", "10"]
        gray_cols = (
            ["0", "1"] if cols == 2
            else ["00", "01", "11", "10"] if cols == 4
            else ["000", "001", "011", "010", "110", "111", "101", "100"]
        )

        for term in terms:
            if self.n == 1:
                row, col = 0, term[0]
            elif self.n == 2:
                row, col = term[0], term[1]
            elif self.n == 3:
                row = term[0]
                col_bin = "".join(str(term[i]) for i in [1, 2])
                col = {"00": 0, "01": 1, "11": 2, "10": 3}[col_bin]
            elif self.n == 4:
                row_bin = "".join(str(term[i]) for i in [0, 1])
                col_bin = "".join(str(term[i]) for i in [2, 3])
                row = {"00": 0, "01": 1, "11": 2, "10": 3}[row_bin]
                col = {"00": 0, "01": 1, "11": 2, "10": 3}[col_bin]
            else:
                row_bin = "".join(str(term[i]) for i in [0, 1])
                col_bin = "".join(str(term[i]) for i in [2, 3, 4])
                row = {"00": 0, "01": 1, "11": 2, "10": 3}[row_bin]
                col = {
                    "000": 0, "001": 1, "011": 2, "010": 3,
                    "110": 4, "111": 5, "101": 6, "100": 7
                }[col_bin]
            kmap[row][col] = 1 if is_sdnf else 0

        return kmap, rows, cols, row_vars, col_vars, gray_rows, gray_cols

    def karnaugh_map_sdnf(self, minterms):
        """Минимизация СДНФ с помощью карты Карно."""
        kmap, rows, cols, row_vars, col_vars, gray_rows, gray_cols = self._setup_karnaugh_map(minterms, True)
        if kmap is None:
            return "0"

        print("\nКарта Карно для СДНФ:")
        header = (
            f"{'':4} {col_vars[0]}=0 {col_vars[0]}=1" if self.n == 2
            else f"{'':4} {col_vars[0]}{col_vars[1]}=00 {col_vars[0]}{col_vars[1]}=01 {col_vars[0]}{col_vars[1]}=11 {col_vars[0]}{col_vars[1]}=10" if self.n <= 4
            else f"{'':4} {col_vars[0]}{col_vars[1]}{col_vars[2]}=000 {col_vars[0]}{col_vars[1]}{col_vars[2]}=001 {col_vars[0]}{col_vars[1]}{col_vars[2]}=011 {col_vars[0]}{col_vars[1]}{col_vars[2]}=010 {col_vars[0]}{col_vars[1]}{col_vars[2]}=110 {col_vars[0]}{col_vars[1]}{col_vars[2]}=111 {col_vars[0]}{col_vars[1]}{col_vars[2]}=101 {col_vars[0]}{col_vars[1]}{col_vars[2]}=100"
        )
        print(header)
        for i in range(rows):
            row_label = (
                f"{row_vars[0]}={gray_rows[i]}" if self.n <= 3
                else f"{row_vars[0]}{row_vars[1]}={gray_rows[i]}"
            )
            print(f"{row_label:4} {' '.join(str(kmap[i][j]) for j in range(cols))}")

        groups = self._find_karnaugh_groups(kmap, 1, self.n)
        result = []
        for group in groups:
            var_values = [set() for _ in range(self.n)]
            for i in range(0, len(group), 2):
                row, col = group[i], group[i + 1]
                values = self._get_variable_values(row, col, self.n, gray_rows, gray_cols)
                for j in range(self.n):
                    var_values[j].add(values[j])

            term = []
            for i in range(self.n):
                if len(var_values[i]) == 1:
                    val = var_values[i].pop()
                    term.append(f"{self.letters_list[i]}" if val == 1 else f"!{self.letters_list[i]}")
            if term:
                result.append("(" + "&".join(term) + ")")
            else:
                return "1"

        final_expr = "|".join(result) if result else "0"
        print("\nМинимизированная СДНФ (Карта Карно):")
        print(final_expr)
        return final_expr

    def karnaugh_map_sknf(self, maxterms):
        """Минимизация СКНФ с помощью карты Карно."""
        kmap, rows, cols, row_vars, col_vars, gray_rows, gray_cols = self._setup_karnaugh_map(maxterms, False)
        if kmap is None:
            return "1"

        print("\nКарта Карно для СКНФ:")
        header = (
            f"{'':4} {col_vars[0]}=0 {col_vars[0]}=1" if self.n == 2
            else f"{'':4} {col_vars[0]}{col_vars[1]}=00 {col_vars[0]}{col_vars[1]}=01 {col_vars[0]}{col_vars[1]}=11 {col_vars[0]}{col_vars[1]}=10" if self.n <= 4
            else f"{'':4} {col_vars[0]}{col_vars[1]}{col_vars[2]}=000 {col_vars[0]}{col_vars[1]}{col_vars[2]}=001 {col_vars[0]}{col_vars[1]}{col_vars[2]}=011 {col_vars[0]}{col_vars[1]}{col_vars[2]}=010 {col_vars[0]}{col_vars[1]}{col_vars[2]}=110 {col_vars[0]}{col_vars[1]}{col_vars[2]}=111 {col_vars[0]}{col_vars[1]}{col_vars[2]}=101 {col_vars[0]}{col_vars[1]}{col_vars[2]}=100"
        )
        print(header)
        for i in range(rows):
            row_label = (
                f"{row_vars[0]}={gray_rows[i]}" if self.n <= 3
                else f"{row_vars[0]}{row_vars[1]}={gray_rows[i]}"
            )
            print(f"{row_label:4} {' '.join(str(kmap[i][j]) for j in range(cols))}")

        groups = self._find_karnaugh_groups(kmap, 0, self.n)
        result = []
        for group in groups:
            var_values = [set() for _ in range(self.n)]
            for i in range(0, len(group), 2):
                row, col = group[i], group[i + 1]
                values = self._get_variable_values(row, col, self.n, gray_rows, gray_cols)
                for j in range(self.n):
                    var_values[j].add(values[j])

            term = []
            for i in range(self.n):
                if len(var_values[i]) == 1:
                    val = var_values[i].pop()
                    term.append(f"!{self.letters_list[i]}" if val == 1 else f"{self.letters_list[i]}")
            if term:
                result.append("(" + "|".join(term) + ")")
            else:
                return "0"

        final_expr = "&".join(result) if result else "1"
        print("\nМинимизированная СКНФ (Карта Карно):")
        print(final_expr)
        return final_expr