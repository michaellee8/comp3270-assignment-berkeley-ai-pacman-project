import sys, grader, parse

from parse import Problem
from typing import Tuple, List, Dict, TypeVar
import random
from copy import deepcopy


def is_float(element: any) -> bool:
    # If you expect None to be passed:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


def dir_to_delta(d: str) -> Tuple[int, int]:
    if d == 'N':
        return -1, 0
    if d == 'S':
        return 1, 0
    if d == 'E':
        return 0, 1
    if d == 'W':
        return 0, -1
    raise ValueError('no such direction')


AnyTuple = TypeVar('AnyTuple', bound=Tuple)


def add_tuple(t1: AnyTuple, t2: AnyTuple) -> AnyTuple:
    return tuple(map(sum, zip(t1, t2)))


def can_dir_be_executed(grid: List[List[str]], pos: Tuple[int, int], d: str) -> bool:
    n_rows = len(grid)
    n_cols = len(grid[0])
    result_pos = add_tuple(pos, dir_to_delta(d))
    r, c = result_pos
    return r in range(n_rows) and c in range(n_cols) and grid[r][c] != '#'


def execute_dir(grid: List[List[str]], pos: Tuple[int, int], d: str) -> Tuple[int, int]:
    if can_dir_be_executed(grid, pos, d):
        return add_tuple(pos, dir_to_delta(d))
    return pos


def get_possible_dir_from_intended(d: str) -> List[str]:
    dm = {'N': ['N', 'E', 'W'], 'E': ['E', 'S', 'N'], 'S': ['S', 'W', 'E'], 'W': ['W', 'N', 'S']}
    return dm[d]


def get_intended_dir_to_actual_dir_prob_dict(intended_dir: str, noise: float) -> Dict[str, float]:
    possible_dirs = get_possible_dir_from_intended(intended_dir)
    ret = {possible_dirs[0]: 1.0 - noise * (len(possible_dirs) - 1)}
    for d in possible_dirs[1:]:
        ret[d] = noise
    return ret


def get_dir_from_intended(d: str, n: float) -> str:
    dm = {'N': ['N', 'E', 'W'], 'E': ['E', 'S', 'N'], 'S': ['S', 'W', 'E'], 'W': ['W', 'N', 'S']}
    return random.choices(population=dm[d], weights=[1 - n * 2, n, n])[0]


def main():
    problem = parse.parse_problem('test_cases/p3/2.prob')
    possible_directions = ['N', 'S', 'W', 'E']
    n_rows = len(problem.grid)
    n_cols = len(problem.grid[0])
    grid = [[e for e in row] for row in problem.grid]
    q_values = [[{'N': 0.0, 'S': 0.0, 'W': 0.0, 'E': 0.0} for e in row] for row in grid]
    decay_factor = 0.5
    while True:
        new_q_values = deepcopy(q_values)
        while True:



if __name__ == '__main__':
    main()

# How to run:
# 1. Assuming same directory structure as provided in the assignment zip.
# 2. cd a3
# 3. python3 p4.py
