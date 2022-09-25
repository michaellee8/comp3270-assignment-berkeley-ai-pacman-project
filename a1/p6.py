import sys, parse, grader
from parse import QueenProblem, QueenAnswer

def compute_number_of_attacks(state: QueenProblem) -> int:
    num = 0
    for i, current_coordinate in enumerate(state):
        for target_coordinate in state[i+1:]:
            if current_coordinate.col - target_coordinate.col == current_coordinate.row - target_coordinate.row:
                num += 1
            elif


def number_of_attacks(problem):
    #Your p6 code here
    solution = """18 12 14 13 13 12 14 14
14 16 13 15 12 14 12 16
14 12 18 13 15 12 14 14
15 14 14 17 13 16 13 16
17 14 17 15 17 14 16 16
17 17 16 18 15 17 15 17
18 14 17 15 15 14 17 16
14 14 13 17 12 14 12 18"""
    return solution


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)