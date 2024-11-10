from tabulate import tabulate


class SimplexSolver:
    def __init__(self, lp_problem):
        self.lp_problem = lp_problem
        self.is_maximization = lp_problem.objective_type == 'max'  # Определяем тип задачи
        self.extended_problem = None
        self.num_variables = lp_problem.num_variables
        self.start_basis = None
        self.optimized_solution = None  # Для хранения оптимального решения
        self.optimized_objective_value = None  # Для хранения оптимального значения целевой функции

    def convert_to_extended_form(self):
        if self.is_maximization:
            extended_objective = [-coef for coef in self.lp_problem.objective_coefficients]
        else:
            extended_objective = self.lp_problem.objective_coefficients.copy()

        extended_objective += [0] * self.lp_problem.num_constraints
        extended_constraints = []
        extended_rhs = []

        for i in range(self.lp_problem.num_constraints):
            constraint = self.lp_problem.constraint_coefficients[i].copy()
            rhs_value = self.lp_problem.right_hand_sides[i]

            if self.lp_problem.constraint_signs[i] == '>=':
                constraint = [-coef for coef in constraint]
                rhs_value = -rhs_value
                sign = '<='
            else:
                sign = self.lp_problem.constraint_signs[i]

            artificial_variable = [0] * self.lp_problem.num_constraints
            if sign == '<=':
                artificial_variable[i] = 1

            extended_constraints.append(constraint + artificial_variable)
            extended_rhs.append(rhs_value)

        self.extended_problem = (extended_objective, extended_constraints, extended_rhs)

    def prepare_basis(self):
        objective, constraints, rhs = self.extended_problem
        basis = [(i + self.lp_problem.num_constraints + 1) for i in range(self.lp_problem.num_constraints)]

        print("Целевая функция:")
        print(objective)

        print("\nОграничения:")
        for i, constraint in enumerate(constraints, start=1):
            print(f"{i}. {constraint}")

        print("\nПравая часть (RHS):")
        for i, value in enumerate(rhs, start=1):
            print(f"{i}. {value}")

        print("\nБазис:")
        print(basis)

        while any(num < 0 for num in rhs):
            b_max = max((num for num in rhs if num < 0), key=abs, default=None)

            if b_max is None:
                print("Нет отрицательных значений в RHS.")
                break

            b_index = rhs.index(b_max)

            max_line_elem = max((num for num in constraints[b_index] if num < 0), key=abs, default=None)

            if max_line_elem is None:
                print("Нет отрицательных элементов в строке базиса.")
                break

            new_basis_elem = constraints[b_index].index(max_line_elem)

            normalized_row = [num / max_line_elem for num in constraints[b_index]]
            normalized_rhs = rhs[b_index] / max_line_elem

            updated_rows = []
            updated_rhs = []

            for i in range(len(constraints)):
                if i != b_index:
                    coefficient = constraints[i][new_basis_elem]
                    updated_row = [
                        constraints[i][j] - coefficient * normalized_row[j]
                        for j in range(len(constraints[i]))
                    ]
                    updated_rows.append(updated_row)
                    updated_rhs.append(rhs[i] - coefficient * normalized_rhs)

            constraints[b_index] = normalized_row
            rhs[b_index] = normalized_rhs

            for i in range(len(updated_rows)):
                constraints[i if i < b_index else i + 1] = updated_rows[i]
                rhs[i if i < b_index else i + 1] = updated_rhs[i]

            basis[b_index] = new_basis_elem + 1
            print("\nОбновленный базис:")
            print(basis)

            self.print_table(constraints, rhs)

        self.extended_problem = (objective, constraints, rhs)
        self.start_basis = basis

    def calc_deltas(self):
        objective, constraints, rhs = self.extended_problem
        basis = self.start_basis

        deltas = []
        for j in range(len(objective)):
            basis_value = sum(objective[basis[i] - 1] * constraints[i][j] for i in range(len(basis)))
            delta = basis_value - objective[j]
            deltas.append(delta)

        objective_value = sum(objective[basis[i] - 1] * rhs[i] for i in range(len(basis)))
        deltas.append(objective_value)

        for idx, delta in enumerate(deltas[:-1]):
            print(f"Переменная {idx + 1}: дельта = {delta}")
        print(f"Значение целевой функции для текущего базиса: {objective_value}")

        return deltas

    def simplex_iteration(self):
        objective, constraints, rhs = self.extended_problem
        while True:
            deltas = self.calc_deltas()
            max_delta = max(deltas[:-1])  # Максимальная дельта среди переменных

            if max_delta <= 0:
                print("Оптимальное решение найдено.")
                self.save_solution()  # Сохраняем решение, если оно найдено
                break

            pivot_col = deltas.index(max_delta)  # Столбец для разрешающей переменной

            ratios = []
            for i in range(len(rhs)):
                elem = constraints[i][pivot_col]
                if elem > 0:
                    ratios.append(rhs[i] / elem)
                else:
                    ratios.append(float('inf'))  # Если элемент <= 0, то бесконечность

            if all(ratio == float('inf') for ratio in ratios):
                print("Задача не ограничена, решение не существует.")
                break

            min_ratio = min(ratios)
            pivot_row = ratios.index(min_ratio)

            pivot_element = constraints[pivot_row][pivot_col]
            constraints[pivot_row] = [x / pivot_element for x in constraints[pivot_row]]
            rhs[pivot_row] /= pivot_element

            # Обновление строк с учетом разрешающего элемента
            for i in range(len(constraints)):
                if i != pivot_row:
                    factor = constraints[i][pivot_col]
                    constraints[i] = [
                        constraints[i][j] - factor * constraints[pivot_row][j]
                        for j in range(len(constraints[i]))
                    ]
                    rhs[i] -= factor * rhs[pivot_row]

            # Обновление базиса
            self.start_basis[pivot_row] = pivot_col + 1

            print("\nОбновленный базис:")
            print(self.start_basis)

            self.print_table(constraints, rhs)

            # Проверка на отсутствие отрицательных коэффициентов в разрешающей строке
            if all(coef >= 0 for coef in constraints[pivot_row]):
                print("В разрешающей строке нет отрицательных коэффициентов. Задача не имеет решения.")
                break

        self.extended_problem = (objective, constraints, rhs)  # Обновляем задачу после завершения итераций

    def print_table(self, constraints, rhs):
        table = [constraint + [rhs[i]] for i, constraint in enumerate(constraints)]
        headers = [f'x{i + 1}' for i in range(len(constraints[0]))] + ['RHS']
        print(tabulate(table, headers=headers, tablefmt='pretty'))

    def save_solution(self):
        _, constraints, rhs = self.extended_problem
        solution = [0] * self.num_variables

        for i, basis_index in enumerate(self.start_basis):
            if 1 <= basis_index <= self.num_variables:
                solution[basis_index - 1] = rhs[i]

        objective_value = sum(
            self.lp_problem.objective_coefficients[i] * solution[i]
            for i in range(self.num_variables)
        )

        self.optimized_solution = solution
        self.optimized_objective_value = objective_value

    def print_solution(self):
        try:
            print("\nОптимальное решение:")
            print("Значения переменных:")
            for i, value in enumerate(self.optimized_solution, start=1):
                print(f"x{i} = {value}")
            print(f"\nОптимальное значение целевой функции: {self.optimized_objective_value}")
        except Exception as e:  # Если optimized_solution или optimized_objective_value не существуют
            print("Задача не имеет оптимального решения.")
