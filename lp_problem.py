# lp_problem.py

class LPProblem:
    def __init__(self, num_variables, num_constraints, objective_type='max'):
        self.num_variables = num_variables  # Количество переменных
        self.num_constraints = num_constraints  # Количество ограничений
        self.objective_coefficients = []  # Коэффициенты целевой функции
        self.constraint_coefficients = []  # Коэффициенты ограничений
        self.constraint_signs = []  # Знаки неравенств
        self.right_hand_sides = []  # Правые части ограничений
        self.objective_type = objective_type  # Тип задачи ('max' или 'min')

    def set_objective_coefficients(self, coefficients):
        if len(coefficients) != self.num_variables:
            raise ValueError("Количество коэффициентов целевой функции должно совпадать с количеством переменных.")
        self.objective_coefficients = coefficients

    def add_constraint(self, constraint_input):
        parts = constraint_input.split()

        # Определяем коэффициенты ограничения
        coefficients = list(map(float, parts[:-2]))  # Все кроме последних двух
        sign = parts[-2]  # Предпоследний элемент — знак неравенства
        rhs = float(parts[-1])  # Последний элемент — правая часть

        if len(coefficients) != self.num_variables:
            raise ValueError("Количество коэффициентов ограничения должно совпадать с количеством переменных.")

        self.constraint_coefficients.append(coefficients)
        self.constraint_signs.append(sign)
        self.right_hand_sides.append(rhs)

    def generate_dual(self):
        # Проверка, что исходная задача полностью задана
        if not self.objective_coefficients or not self.constraint_coefficients:
            raise ValueError("Необходимо полностью задать прямую задачу перед генерацией двойственной.")

        # Двойственная задача имеет m переменных и n ограничений
        dual_problem = LPProblem(self.num_constraints, self.num_variables,
                                 'min' if self.objective_type == 'max' else 'max')

        # Коэффициенты целевой функции двойственной задачи
        dual_problem.set_objective_coefficients(self.right_hand_sides)

        # Формирование ограничений для двойственной задачи
        for j in range(self.num_variables):
            constraint = []
            for i in range(self.num_constraints):
                constraint.append(self.constraint_coefficients[i][j])
            sign = '>=' if self.objective_type == 'max' else '<='
            dual_problem.add_constraint(" ".join(map(str, constraint)) + f" {sign} {self.objective_coefficients[j]}")

        return dual_problem

    def __str__(self):
        result = f"Целевая функция: {'Minimize' if self.objective_type == 'min' else 'Maximize'} {self.objective_coefficients}\n"
        result += "Ограничения:\n"
        for i in range(self.num_constraints):
            result += f"  {' '.join(map(str, self.constraint_coefficients[i]))} {self.constraint_signs[i]} {self.right_hand_sides[i]}\n"
        return result
