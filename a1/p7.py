import sys, parse, grader
from parse import QueenProblem, QueenAnswer
from copy import deepcopy
from typing import List


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


def convert_queen_problem_to_string(qp: QueenProblem) -> str:
    return '\n'.join([
        ' '.join(['q' if qp[col_idx].row == row_idx else '.' for col_idx in range(8)])
        for row_idx in range(8)
    ])


def better_board(problem: QueenProblem) -> str:
    original_problem = deepcopy(problem)
    ans: List[List[int]] = [[0 for i in range(8)] for j in range(8)]
    for col_idx in range(8):
        for row_idx in range(8):
            problem[col_idx].row = row_idx
            local_sol = compute_number_of_attacks(problem)
            ans[row_idx][col_idx] = local_sol
        problem = deepcopy(original_problem)
    min_cost = min([min(r) for r in ans])
    for row_idx in range(8):
        for col_idx in range(8):
            if min_cost == ans[row_idx][col_idx]:
                problem_mut = deepcopy(original_problem)
                problem_mut[col_idx].row = row_idx
                return convert_queen_problem_to_string(problem_mut)


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 7
    grader.grade(problem_id, test_case_id, better_board, parse.read_8queens_search_problem)
