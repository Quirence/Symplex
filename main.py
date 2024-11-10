from lp_problem import LPProblem
from simplex_solver import SimplexSolver


def main():
    # Ввод параметров прямой задачи ЛП
    print("Задача линейного программирования (ЛП)")
    num_variables = int(input("Введите количество переменных: "))
    num_constraints = int(input("Введите количество ограничений: "))
    objective_type = input("Тип задачи (max или min): ").strip().lower()

    # Создание объекта прямой задачи ЛП
    lp_problem = LPProblem(num_variables, num_constraints, objective_type)

    # Ввод коэффициентов целевой функции прямой задачи
    print("\nВведите коэффициенты целевой функции через пробел:")
    objective_coefficients = list(map(float, input().split()))
    lp_problem.set_objective_coefficients(objective_coefficients)

    # Ввод ограничений для прямой задачи
    print("\nВведите каждое ограничение в формате:\n<коэффициенты> <знак неравенства> <правая часть>")
    print("Пример: 1 2 3 <= 10")
    for _ in range(num_constraints):
        constraint_input = input(f"Ограничение {_ + 1}: ")
        lp_problem.add_constraint(constraint_input)

    # Отобразить заданную прямую задачу ЛП
    print("\nЗаданная прямая задача ЛП:")
    print(lp_problem)

    # Генерация двойственной задачи
    dual_problem = lp_problem.generate_dual()

    # Отобразить двойственную задачу
    print("\nСгенерированная двойственная задача ЛП:")
    print(dual_problem)

    # Решение двойственной задачи с использованием двойственного симплекс-метода
    simplex_solver = SimplexSolver(dual_problem)
    simplex_solver.convert_to_extended_form()
    simplex_solver.prepare_basis()
    print("\nНачало итераций двойственного симплекс-метода для двойственной задачи:")
    simplex_solver.simplex_iteration()
    simplex_solver.print_solution()


if __name__ == "__main__":
    main()
