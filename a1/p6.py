import sys, parse, grader
from parse import QueenProblem, QueenAnswer
from copy import deepcopy


def compute_number_of_attacks(state: QueenProblem) -> int:
    num = 0
    for i, current_coordinate in enumerate(state):
        for target_coordinate in state[i + 1:]:
            if current_coordinate.col - target_coordinate.col == current_coordinate.row - target_coordinate.row:
                num += 1
            elif current_coordinate.col + current_coordinate.row == target_coordinate.col + target_coordinate.row:
                num += 1
            elif current_coordinate.row == target_coordinate.row:
                num += 1
            elif current_coordinate.col == target_coordinate.col:
                num += 1
    return num


def convert_queen_answer_to_string(qa: QueenAnswer) -> str:
    return '\n'.join([' '.join(r) for r in qa])


def number_of_attacks(problem: QueenProblem) -> str:
    original_problem = deepcopy(problem)
    ans: QueenAnswer = [[0 for i in range(8)] for j in range(8)]
    for col_idx in range(8):
        for row_idx in range(8):
            problem[col_idx].row = row_idx
            local_sol = compute_number_of_attacks(problem)
            ans[row_idx][col_idx] = str(local_sol).rjust(2, ' ')
        problem = deepcopy(original_problem)
    return convert_queen_answer_to_string(ans)


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)
