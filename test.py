class LPProblem:
    def __init__(self, num_variables, num_constraints):
        self.num_variables = num_variables
        self.num_constraints = num_constraints
        self.objective_coefficients = []
        self.constraint_coefficients = []
        self.right_hand_sides = []
        self.constraint_signs = []

    def set_objective_coefficients(self, coeffs):
        self.objective_coefficients = coeffs

    def add_constraint(self, constraint):
        coeffs, rhs = constraint.split(" >= ")
        coeffs = list(map(float, coeffs.split()))
        self.constraint_coefficients.append(coeffs)
        self.right_hand_sides.append(float(rhs))
        self.constraint_signs.append(">=")

class SimplexSolver:
    def __init__(self, lp_problem):
        self.lp_problem = lp_problem
        self.extended_problem = None
        self.num_variables = lp_problem.num_variables

    def convert_to_extended_form(self):
        num_constraints = self.lp_problem.num_constraints

        # Создаем целевую функцию для расширенной задачи
        extended_objective = self.lp_problem.objective_coefficients + [0] * num_constraints

        # Создаем ограничения для расширенной задачи
        extended_constraints = []
        extended_rhs = []

        for i in range(num_constraints):
            constraint = self.lp_problem.constraint_coefficients[i][:]  # Копируем коэффициенты ограничения
            rhs = self.lp_problem.right_hand_sides[i]

            # Добавляем искусственные переменные
            artificial_variable = [0] * num_constraints  # Создаем список для искусственных переменных
            artificial_variable[i] = 1  # Устанавливаем 1 для текущего ограничения

            constraint += artificial_variable  # Добавляем искусственные переменные
            extended_constraints.append(constraint)
            extended_rhs.append(rhs)

        self.extended_problem = (extended_objective, extended_constraints, extended_rhs)

    def prepare_dual_simplex(self):
        if self.extended_problem:
            objective, constraints, rhs = self.extended_problem
            num_rows = len(constraints)
            num_cols = len(objective)

            # Создаем симплекс-таблицу
            tableau = [[0] * (num_cols + 1) for _ in range(num_rows + 1)]

            # Заполняем симплекс-таблицу
            for i in range(num_rows):
                tableau[i][:num_cols] = constraints[i]
                tableau[i][num_cols] = rhs[i]
            tableau[num_rows][:num_cols] = [-coeff for coeff in objective]

            # Запускаем двойственный симплекс-метод
            self.dual_simplex(tableau)

    def dual_simplex(self, tableau):
        num_rows, num_cols = len(tableau), len(tableau[0])
        basis = list(range(num_cols - 1, num_cols - 1 - (num_rows - 1), -1))

        while True:
            # Проверка на оптимальность: если все элементы в последней строке >= 0
            if all(tableau[-1][j] >= 0 for j in range(num_cols)):
                break

            # Шаг 1: Выбор опорного элемента (строка)
            pivot_row = min(range(num_rows - 1), key=lambda r: tableau[r][-1] / tableau[r][0] if tableau[r][0] > 0 else float('inf'))

            # Шаг 2: Выбор опорного столбца
            ratios = [tableau[r][-1] / tableau[r][pivot_row] if tableau[r][pivot_row] > 0 else float('inf') for r in range(num_rows - 1)]
            pivot_col = ratios.index(min(ratios))

            # Шаг 3: Обновление таблицы
            pivot_value = tableau[pivot_row][pivot_col]
            for j in range(num_cols):
                tableau[pivot_row][j] /= pivot_value  # Нормализуем опорную строку

            for i in range(num_rows):
                if i != pivot_row:
                    factor = tableau[i][pivot_col]
                    for j in range(num_cols):
                        tableau[i][j] -= factor * tableau[pivot_row][j]

            # Обновляем базис
            basis[pivot_row] = pivot_col

            # Печать текущей симплекс-таблицы
            self.print_tableau(tableau, basis)

    def print_tableau(self, tableau, basis):
        print("Симплекс-таблица:")
        header = [""] + [f"x{i}" for i in range(len(tableau[0]) - 1)] + ["RHS"]
        print(" | ".join(header))
        for i in range(len(tableau)):
            row = [f"x{basis[i]}" if i < len(basis) else "z" if i == len(basis) else ""]
            row += [f"{tableau[i][j]:.2f}" for j in range(len(tableau[i]))]
            print(" | ".join(row))
        print("\n")

def main():
    # Пример инициализации задачи
    problem = LPProblem(3, 3)
    problem.set_objective_coefficients([800.0, 600.0, 120.0])
    problem.add_constraint("0.8 0.4 0.0 >= 108.0")
    problem.add_constraint("0.5 0.4 0.1 >= 112.0")
    problem.add_constraint("0.6 0.3 0.1 >= 126.0")

    solver = SimplexSolver(problem)
    solver.convert_to_extended_form()
    solver.prepare_dual_simplex()  # Запускаем двойственный симплекс-метод

if __name__ == "__main__":
    main()
