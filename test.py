from lp_problem import LPProblem
from simplex_solver import SimplexSolver


class Test:
    @classmethod
    def get_test_case(cls, case):
        # Конвертируем входные данные в нужный формат
        match case:
            case 1:
                return cls.create_problem(
                    num_variables=2, num_constraints=3, is_max=True,
                    coefficients=[14, 18],
                    constraint_coefficients=[[10, 8], [5, 10], [6, 12]],
                    constraint_signs=['<=', '<=', '<='],
                    rhs=[168, 180, 144]
                )
            case 2:
                return cls.create_problem(
                    num_variables=2, num_constraints=3, is_max=True,
                    coefficients=[3, 2],
                    constraint_coefficients=[[1, 2], [2, -1], [1, 3]],
                    constraint_signs=['<=', '>=', '>='],
                    rhs=[12, 7, 14]
                )
            case 3:
                return cls.create_problem(
                    num_variables=2, num_constraints=3, is_max=False,
                    coefficients=[4, 1],
                    constraint_coefficients=[[1, 2], [2, -1], [1, 3]],
                    constraint_signs=['>=', '>=', '<='],
                    rhs=[12, 12, 14]
                )
            case 4:
                return cls.create_problem(
                    num_variables=3, num_constraints=2, is_max=False,
                    coefficients=[4, 3, 6],
                    constraint_coefficients=[[3, -4, 2], [5, 2, 3]],
                    constraint_signs=['>=', '>='],
                    rhs=[11, 16]
                )
            case 5:
                return cls.create_problem(
                    num_variables=2, num_constraints=2, is_max=False,
                    coefficients=[10, 20],
                    constraint_coefficients=[[4, 3], [5, 6]],
                    constraint_signs=['>=', '>='],
                    rhs=[2, 3]
                )
            case 6:
                return cls.create_problem(
                    num_variables=2, num_constraints=3, is_max=True,
                    coefficients=[360, 240],
                    constraint_coefficients=[[3, 6], [8, 2], [4, 6]],
                    constraint_signs=['>=', '<=', '>='],
                    rhs=[1440, 720, 960]
                )
            case 7:
                return cls.create_problem(
                    num_variables=2, num_constraints=2, is_max=True,
                    coefficients=[4, 5],
                    constraint_coefficients=[[1, 1], [1, 1]],
                    constraint_signs=['<=', '>='],
                    rhs=[2, 5]
                )
            case 8:
                return cls.create_problem(
                    num_variables=2, num_constraints=2, is_max=False,
                    coefficients=[4, 5],
                    constraint_coefficients=[[1, 1], [1, 1]],
                    constraint_signs=['<=', '<='],
                    rhs=[2, 5]
                )
            case 9:
                return cls.create_problem(
                    num_variables=3, num_constraints=2, is_max=False,
                    coefficients=[168, 180, 144],
                    constraint_coefficients=[[10, 5, 6], [8, 10, 12]],
                    constraint_signs=['>=', '>='],
                    rhs=[14, 18]
                )
            case 10:
                return cls.create_problem(
                    num_variables=5, num_constraints=5, is_max=False,
                    coefficients=[1, 10, 100, 1000, 10000],
                    constraint_coefficients=[
                        [1, 2, 3, 4, 5],
                        [5, 6, 7, 8, 9],
                        [9, 10, 11, 12, 13],
                        [13, 14, 15, 16, 17],
                        [17, 18, 19, 20, 21]
                    ],
                    constraint_signs=['>=', '<=', '>=', '<=', '>='],
                    rhs=[2, 4, 8, 16, 32]
                )
            case _:
                raise ValueError("Неверный номер теста! Введите число от 1 до 10.")

    @staticmethod
    def create_problem(num_variables, num_constraints, is_max, coefficients,
                       constraint_coefficients, constraint_signs, rhs):
        objective_type = 'max' if is_max else 'min'
        problem = LPProblem(num_variables=num_variables, num_constraints=num_constraints, objective_type=objective_type)
        problem.set_objective_coefficients(coefficients)

        # Добавляем ограничения
        for i in range(num_constraints):
            constraint = " ".join(map(str, constraint_coefficients[i])) + f" {constraint_signs[i]} {rhs[i]}"
            problem.add_constraint(constraint)

        return problem

    @classmethod
    def run_tests(cls):
        start, end = 1, 10
        for case in range(start, end + 1):
            try:
                print(f"\nТест {case}:")
                lp_problem = cls.get_test_case(case)
                solver = SimplexSolver(lp_problem)
                solver.convert_to_extended_form()
                solver.prepare_basis()
                result = solver.simplex_iteration()
                print("Результат:", result)
            except Exception as e:
                print(f"Ошибка в тесте {case}: {e}")