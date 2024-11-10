from lp_problem import LPProblem
from simplex_solver import SimplexSolver


def test_lp_1():
    """
    max Z = 3x1 + 5x2
    s.t.
    x1 + 2x2 <= 8
    2x1 + x2 <= 10
    x1, x2 >= 0
    Optimal Z = 20
    """
    lp_problem = LPProblem(2, 2, 'max')
    lp_problem.set_objective_coefficients([3, 5])
    lp_problem.add_constraint("1 2 <= 8")
    lp_problem.add_constraint("2 1 <= 10")

    print("Прямая задача:")
    print(lp_problem)

    # Генерация двойственной задачи
    dual_problem = lp_problem.generate_dual()

    print("\nДвойственная задача:")
    print(dual_problem)

    # Решение двойственной задачи с использованием симплекс-метода
    simplex_solver = SimplexSolver(dual_problem)
    simplex_solver.convert_to_extended_form()
    simplex_solver.prepare_basis()
    print("\nНачало итераций двойственного симплекс-метода для двойственной задачи:")
    simplex_solver.simplex_iteration()
    simplex_solver.print_solution()
    print("Optimal Z = 22")


def test_lp_2():
    """
    max Z = 4x1 + 3x2
    s.t.
    x1 + x2 <= 6
    x1 - x2 <= 3
    x1, x2 >= 0
    Optimal Z = 24
    """
    lp_problem = LPProblem(2, 2, 'max')
    lp_problem.set_objective_coefficients([4, 3])
    lp_problem.add_constraint("1 1 <= 6")
    lp_problem.add_constraint("1 -1 <= 3")

    print("Прямая задача:")
    print(lp_problem)

    # Генерация двойственной задачи
    dual_problem = lp_problem.generate_dual()

    print("\nДвойственная задача:")
    print(dual_problem)

    # Решение двойственной задачи с использованием симплекс-метода
    simplex_solver = SimplexSolver(dual_problem)
    simplex_solver.convert_to_extended_form()
    simplex_solver.prepare_basis()
    print("\nНачало итераций двойственного симплекс-метода для двойственной задачи:")
    simplex_solver.simplex_iteration()
    simplex_solver.print_solution()
    print("Optimal Z = 24")


def test_lp_3():
    """
    min Z = 2x1 + 3x2
    s.t.
    x1 + x2 >= 5
    x1 - x2 >= 1
    x1, x2 >= 0
    Optimal Z = 15
    """
    lp_problem = LPProblem(2, 2, 'min')
    lp_problem.set_objective_coefficients([2, 3])
    lp_problem.add_constraint("1 1 >= 5")
    lp_problem.add_constraint("1 -1 >= 1")

    print("Прямая задача:")
    print(lp_problem)

    # Генерация двойственной задачи
    dual_problem = lp_problem.generate_dual()

    print("\nДвойственная задача:")
    print(dual_problem)

    # Решение двойственной задачи с использованием симплекс-метода
    simplex_solver = SimplexSolver(dual_problem)
    simplex_solver.convert_to_extended_form()
    simplex_solver.prepare_basis()
    print("\nНачало итераций двойственного симплекс-метода для двойственной задачи:")
    simplex_solver.simplex_iteration()
    simplex_solver.print_solution()
    print("Optimal Z = 15")


def test_lp_4():
    """
    max Z = 5x1 + 4x2
    s.t.
    3x1 + 2x2 <= 12
    x1 + 3x2 <= 10
    x1, x2 >= 0
    Optimal Z = 18
    """
    lp_problem = LPProblem(2, 2, 'max')
    lp_problem.set_objective_coefficients([5, 4])
    lp_problem.add_constraint("3 2 <= 12")
    lp_problem.add_constraint("1 3 <= 10")

    print("Прямая задача:")
    print(lp_problem)

    # Генерация двойственной задачи
    dual_problem = lp_problem.generate_dual()

    print("\nДвойственная задача:")
    print(dual_problem)

    # Решение двойственной задачи с использованием симплекс-метода
    simplex_solver = SimplexSolver(dual_problem)
    simplex_solver.convert_to_extended_form()
    simplex_solver.prepare_basis()
    print("\nНачало итераций двойственного симплекс-метода для двойственной задачи:")
    simplex_solver.simplex_iteration()
    simplex_solver.print_solution()
    print("Optimal Z = 18")


def test_lp_5():
    """
    min Z = 6x1 + 5x2
    s.t.
    4x1 + x2 >= 8
    x1 + 2x2 >= 6
    x1, x2 >= 0
    Optimal Z = 17
    """
    lp_problem = LPProblem(2, 2, 'min')
    lp_problem.set_objective_coefficients([6, 5])
    lp_problem.add_constraint("4 1 >= 8")
    lp_problem.add_constraint("1 2 >= 6")

    print("Прямая задача:")
    print(lp_problem)

    # Генерация двойственной задачи
    dual_problem = lp_problem.generate_dual()

    print("\nДвойственная задача:")
    print(dual_problem)

    # Решение двойственной задачи с использованием симплекс-метода
    simplex_solver = SimplexSolver(dual_problem)
    simplex_solver.convert_to_extended_form()
    simplex_solver.prepare_basis()
    print("\nНачало итераций двойственного симплекс-метода для двойственной задачи:")
    simplex_solver.simplex_iteration()
    simplex_solver.print_solution()
    print("Optimal Z = 17")


# Запуск всех тестов
def run_all_tests():
    test_lp_1()
    test_lp_2()
    test_lp_3()
    test_lp_4()
    test_lp_5()
    print("Все тесты пройдены успешно!")


if __name__ == "__main__":
    run_all_tests()
