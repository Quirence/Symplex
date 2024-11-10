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

        # Приводим все ограничения к одному виду, если смешанные знаки
        for i in range(self.num_constraints):
            if self.constraint_signs[i] == '>=':
                # Умножаем коэффициенты ограничения и правую часть на -1 для приведения к '<='
                self.constraint_coefficients[i] = [-coef for coef in self.constraint_coefficients[i]]
                self.right_hand_sides[i] = -self.right_hand_sides[i]
                self.constraint_signs[i] = '<='  # Меняем знак на '<='

        # Двойственная задача имеет m переменных и n ограничений
        dual_problem = LPProblem(self.num_constraints, self.num_variables,
                                 'min' if self.objective_type == 'max' else 'max')

        # Коэффициенты целевой функции двойственной задачи (это правые части исходных ограничений)
        dual_problem.set_objective_coefficients(self.right_hand_sides)

        # Формирование ограничений для двойственной задачи
        for j in range(self.num_variables):  # Перебираем каждую переменную в прямой задаче
            constraint = []
            for i in range(self.num_constraints):  # Перебираем каждое ограничение в прямой задаче
                # Строим коэффициенты для ограничения в двойственной задаче из столбцов исходных коэффициентов
                constraint.append(self.constraint_coefficients[i][j])

            # Знак в ограничении двойственной задачи зависит от знака исходного ограничения
            if self.constraint_signs[i] == '<=':
                dual_sign = '>='  # Если в прямой задаче знак <=, то в двойственной будет >=
            elif self.constraint_signs[i] == '>=':
                dual_sign = '<='  # Если в прямой задаче знак >=, то в двойственной будет <=
            else:
                raise ValueError(f"Неизвестный знак ограничения: {self.constraint_signs[i]}")

            # Добавление ограничения в двойственную задачу
            dual_problem.add_constraint(
                " ".join(map(str, constraint)) + f" {dual_sign} {self.objective_coefficients[j]}")

        # Перезаписываем число переменных и ограничений
        dual_problem.num_variables = self.num_constraints
        dual_problem.num_constraints = self.num_variables

        return dual_problem

    def __str__(self):
        result = f"Целевая функция: {'Minimize' if self.objective_type == 'min' else 'Maximize'} {self.objective_coefficients}\n"
        result += "Ограничения:\n"
        for i in range(self.num_constraints):
            result += f"  {' '.join(map(str, self.constraint_coefficients[i]))} {self.constraint_signs[i]} {self.right_hand_sides[i]}\n"
        return result
