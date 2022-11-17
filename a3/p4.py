"""
Analysis:
- My approach here is basically let the agent run the game using random moves
  and let it learn its way to the best q_values, and then use mean squared error
  to see if we have achieved converge yet.
- Interestingly the agent seems to prefer hitting the bad exit and exit early for
  unknown reason, and therefore unable to attain the optimal policy as discussed in the
  problem set.
"""

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


possible_directions = ['N', 'S', 'W', 'E']


def get_intended_dir() -> str:
    return random.choices(population=possible_directions)[0]


def mse_q_values(old_q_values: List[List[Dict[str, float]]], new_q_values: List[List[Dict[str, float]]],
                 grid: List[List[str]]) -> float:
    n_rows = len(old_q_values)
    n_cols = len(old_q_values[0])
    sq_sum = 0.0
    count = 0
    for r in range(n_rows):
        for c in range(n_cols):
            if is_float(grid[r][c]):
                count += 1
                direction = 'exit'
                sq_sum += (old_q_values[r][c][direction] - new_q_values[r][c][direction]) ** 2
                continue
            for direction in possible_directions:
                count += 1
                sq_sum += (old_q_values[r][c][direction] - new_q_values[r][c][direction]) ** 2
    return sq_sum / count


def main():
    problem = parse.parse_problem('test_cases/p3/2.prob')
    n_rows = len(problem.grid)
    n_cols = len(problem.grid[0])
    grid = [[e for e in row] for row in problem.grid]
    q_values = [[{'N': 0.0, 'S': 0.0, 'W': 0.0, 'E': 0.0, 'exit': 0.0} for e in row] for row in grid]
    decay_factor = 0.0001
    start_pos = (0, 0)
    for r in range(n_rows):
        for c in range(n_cols):
            if grid[r][c] == 'S':
                start_pos = (r, c)
    while True:
        new_q_values = deepcopy(q_values)
        player_pos = start_pos

        # Loop until we are in an exit
        while not is_float(grid[player_pos[0]][player_pos[1]]):
            intended_dir = get_intended_dir()
            actual_dir = get_dir_from_intended(intended_dir, problem.noise)
            new_player_pos = execute_dir(grid, player_pos, actual_dir)
            old_player_pos = player_pos
            reward = problem.living_reward
            new_q_values[old_player_pos[0]][old_player_pos[1]][intended_dir] = \
                (1 - decay_factor) * \
                new_q_values[old_player_pos[0]][
                    old_player_pos[1]][intended_dir] + decay_factor * (
                        reward + problem.discount *
                        max({k: v for (k, v) in new_q_values[new_player_pos[0]][new_player_pos[1]].items() if
                             k != 'exit'}.values())
                )
            player_pos = new_player_pos

        # Now, update exit reward
        reward = float(grid[player_pos[0]][player_pos[1]])
        intended_dir = 'exit'

        new_q_values[player_pos[0]][player_pos[1]][intended_dir] = \
            (1 - decay_factor) * \
            new_q_values[player_pos[0]][
                player_pos[1]][intended_dir] + decay_factor * reward

        print(f"mse: {mse_q_values(q_values, new_q_values, grid)}")
        if mse_q_values(q_values, new_q_values, grid) <= 0.00000000000001:
            # We have learnt into a good solution, let's break the learning loop
            break

        q_values = new_q_values

    # print the result policy
    print(
        [
            [
                max({k: v for (k, v) in e.items() if
                     (k == 'exit' and is_float(grid[r][c]) or k != 'exit' and not is_float(grid[r][c]))}.items(),
                    key=lambda p: p[1])[0]
                for c, e in enumerate(row)
            ] for r, row in enumerate(q_values)
        ]
    )


if __name__ == '__main__':
    main()

# How to run:
# 1. Assuming same directory structure as provided in the assignment zip.
# 2. cd a3
# 3. python3 p4.py
