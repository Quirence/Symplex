from tabulate import tabulate


class SimplexSolver:
    def __init__(self, lp_problem):
        self.lp_problem = lp_problem
        self.extended_problem = None  # Для хранения расширенной задачи
        self.num_variables = lp_problem.num_variables  # Храним количество переменных
        self.start_basis = None

    def convert_to_extended_form(self):
        # Инвертируем коэффициенты ограничений и правые части
        new_constraints = []
        new_rhs = []

        for i in range(self.lp_problem.num_constraints):
            # Инвертируем коэффициенты ограничения
            constraint = [-coef for coef in self.lp_problem.constraint_coefficients[i]]
            new_constraints.append(constraint)
            # Инвертируем правую часть
            new_rhs.append(-self.lp_problem.right_hand_sides[i])

        # Создаем целевую функцию для расширенной задачи
        extended_objective = self.lp_problem.objective_coefficients + [0] * self.lp_problem.num_constraints

        extended_constraints = []
        extended_rhs = []

        for i in range(self.lp_problem.num_constraints):
            # Копируем инвертированные коэффициенты
            constraint = new_constraints[i].copy()
            # Создаем список для искусственных переменных
            artificial_variable = [0] * self.lp_problem.num_constraints
            artificial_variable[i] = 1  # Устанавливаем 1 для текущего ограничения

            # Добавляем искусственные переменные в зависимости от знака неравенства
            if self.lp_problem.constraint_signs[i] == '>=':
                # Если неравенство ">=", добавляем 1
                constraint += artificial_variable
            else:
                # Если неравенство "<=", добавляем 0
                constraint += [0] * self.lp_problem.num_constraints

            # Сохраняем ограничение и правую часть
            extended_constraints.append(constraint)
            extended_rhs.append(new_rhs[i])

        # Сохраняем расширенные данные
        self.extended_problem = (extended_objective, extended_constraints, extended_rhs)

    def prepare_basis(self):
        objective, constraints, rhs = self.extended_problem
        basis = [(i + self.lp_problem.num_constraints + 1) for i in range(self.lp_problem.num_constraints)]

        # Печатаем целевую функцию
        print("Целевая функция:")
        print(objective)

        # Печатаем ограничения
        print("\nОграничения:")
        for i, constraint in enumerate(constraints, start=1):
            print(f"{i}. {constraint}")

        # Печатаем правую часть
        print("\nПравая часть (RHS):")
        for i, value in enumerate(rhs, start=1):
            print(f"{i}. {value}")

        # Печатаем базис
        print("\nБазис:")
        print(basis)

        while any(num < 0 for num in rhs):  # Продолжаем, пока есть отрицательные значения в RHS
            # Находим максимальное отрицательное значение в RHS
            b_max = max((num for num in rhs if num < 0), key=abs, default=None)

            if b_max is None:
                print("Нет отрицательных значений в RHS.")
                break

            b_index = rhs.index(b_max)  # Индекс строки для замены базисного элемента

            # Находим максимальный отрицательный элемент в текущей строке (constraints[b_index])
            max_line_elem = max((num for num in constraints[b_index] if num < 0), key=abs, default=None)

            if max_line_elem is None:
                print("Нет отрицательных элементов в строке базиса.")
                break

            new_basis_elem = constraints[b_index].index(max_line_elem)  # Индекс нового базисного элемента

            # Нормализуем разрешающую строку
            normalized_row = [num / max_line_elem for num in constraints[b_index]]
            normalized_rhs = rhs[b_index] / max_line_elem

            # Обновляем строки и правые части
            updated_rows = []
            updated_rhs = []

            for i in range(len(constraints)):
                if i != b_index:  # Пропускаем разрешающую строку
                    coefficient = constraints[i][
                        new_basis_elem]  # Получаем коэффициент из столбца базиса текущей строки
                    # Обновляем текущую строку
                    updated_row = [
                        constraints[i][j] - coefficient * normalized_row[j]
                        for j in range(len(constraints[i]))
                    ]
                    updated_rows.append(updated_row)
                    updated_rhs.append(rhs[i] - coefficient * normalized_rhs)

            # Обновляем базис и строки для следующей итерации
            constraints[b_index] = normalized_row
            rhs[b_index] = normalized_rhs

            for i in range(len(updated_rows)):
                constraints[i if i < b_index else i + 1] = updated_rows[i]
                rhs[i if i < b_index else i + 1] = updated_rhs[i]

            # Обновляем базис
            basis[b_index] = new_basis_elem + 1  # Обновляем элемент базиса
            print("\nОбновленный базис:")
            print(basis)

            # Печатаем все строки и правые части в виде таблицы
            self.print_table(constraints, rhs)

        self.extended_problem = (objective, constraints, rhs)
        self.basis = basis

    def calc_deltas(self):
        """
        Вычисляет дельты (обратные симплекс-разности) для каждой переменной, включая значение целевой функции.
        Предполагается, что функция вызывается после prepare_basis.
        """
        objective, constraints, rhs = self.extended_problem  # Получаем целевую функцию и ограничения
        basis = self.basis  # Используем текущий базис

        # Вычисляем дельты для всех переменных, не входящих в базис
        deltas = []
        for j in range(len(objective)):
            # Вычисляем значение целевой функции для базисных переменных
            basis_value = sum(objective[basis[i] - 1] * constraints[i][j] for i in range(len(basis)))
            delta = basis_value - objective[j]  # Изменили порядок вычитания для корректного знака
            deltas.append(delta)

        # Вычисляем значение целевой функции для текущего базисного плана
        objective_value = sum(objective[basis[i] - 1] * rhs[i] for i in range(len(basis)))
        deltas.append(objective_value)  # Добавляем это значение как последнюю "дельту"

        # Выводим дельты для отладки
        for idx, delta in enumerate(deltas[:-1]):
            print(f"Переменная {idx + 1}: дельта = {delta}")
        print(f"Значение целевой функции для текущего базиса: {objective_value}")

        return deltas

    def simplex_iteration(self):
        """
        Выполняет итерации симплекс-метода для поиска оптимального решения.
        """
        objective, constraints, rhs = self.extended_problem
        while True:
            # 1. Вычисляем дельты и находим разрешающий столбец (столбец с максимальной дельтой)
            deltas = self.calc_deltas()
            max_delta = max(deltas[:-1])  # Последний элемент - значение целевой функции, его не учитываем
            if max_delta <= 0:
                print("Оптимальное решение найдено.")
                break  # Все дельты <= 0, решение оптимально

            pivot_col = deltas.index(max_delta)  # Индекс разрешающего столбца

            # 2. Находим симплекс-отношения Q для каждой строки
            ratios = []
            for i in range(len(rhs)):
                elem = constraints[i][pivot_col]
                if elem > 0:  # Учитываем только положительные значения в разрешающем столбце
                    ratios.append(rhs[i] / elem)
                else:
                    ratios.append(float('inf'))  # Если элемент <= 0, отношение не учитывается

            # 3. Определяем разрешающую строку - строку с наименьшим положительным Q
            if all(ratio == float('inf') for ratio in ratios):
                print("Задача не ограничена, решение не существует.")
                break

            min_ratio = min(ratios)
            pivot_row = ratios.index(min_ratio)

            # 4. Пересчитываем таблицу, нормализуем разрешающую строку
            pivot_element = constraints[pivot_row][pivot_col]
            constraints[pivot_row] = [x / pivot_element for x in constraints[pivot_row]]
            rhs[pivot_row] /= pivot_element

            # Обновляем остальные строки, исключая разрешающую строку
            for i in range(len(constraints)):
                if i != pivot_row:
                    factor = constraints[i][pivot_col]
                    constraints[i] = [
                        constraints[i][j] - factor * constraints[pivot_row][j]
                        for j in range(len(constraints[i]))
                    ]
                    rhs[i] -= factor * rhs[pivot_row]

            # 5. Обновляем базис
            self.basis[pivot_row] = pivot_col + 1

            # Выводим промежуточное состояние таблицы для отладки
            print("\nОбновленный базис:")
            print(self.basis)
            self.print_table(constraints, rhs)

    def print_table(self, constraints, rhs):
        # Форматируем данные в виде таблицы с использованием tabulate
        table = [constraint + [rhs[i]] for i, constraint in enumerate(constraints)]
        headers = [f'x{i + 1}' for i in range(len(constraints[0]))] + ['RHS']
        print(tabulate(table, headers=headers, tablefmt='pretty'))

    def print_extended_problem(self):
        if self.extended_problem:
            objective, constraints, rhs = self.extended_problem
            print("Расширенная целевая функция: ", objective)
            print("Расширенные ограничения:")
            for i in range(len(constraints)):
                constraint_str = " ".join(map(str, constraints[i])) + f" = {rhs[i]}"  # Изменено на "="
                print(constraint_str)
        else:
            print("Расширенная проблема не инициализирована.")
