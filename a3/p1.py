import random
import sys
import grader
from parse import Problem
import parse
from typing import Tuple, List, TypeVar


def get_dir_from_intended(d: str, n: float) -> str:
    dm = {'N': ['N', 'E', 'W'], 'E': ['E', 'S', 'N'], 'S': ['S', 'W', 'E'], 'W': ['W', 'N', 'S']}
    return random.choices(population=dm[d], weights=[1 - n * 2, n, n])[0]


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


def play_episode(problem: Problem) -> str:
    n_rows = len(problem.grid)
    n_cols = len(problem.grid[0])
    grid = [[e for e in row] for row in problem.grid]
    reward_sum = 0.0
    experience = ''
    # (row, col)
    player_pos = (0, 0)
    for r in range(n_rows):
        for c in range(n_cols):
            if grid[r][c] == 'S':
                player_pos = (r, c)
    experience += 'Start state:\n'
    experience += parse.grid_to_str_with_player_pos(grid, player_pos)
    experience += '\n'
    experience += f"Cumulative reward sum: {reward_sum}\n"
    if problem.seed != -1:
        random.seed(problem.seed, version=1)
    while True:
        experience += '-------------------------------------------- \n'
        old_pos_r, old_pos_c = player_pos
        intended_dir = problem.policy[old_pos_r][old_pos_c]
        if intended_dir == 'exit':
            experience += 'Taking action: exit (intended: exit)\n'
            exit_reward = 0.0
            if grid[old_pos_r][old_pos_c] == '1':
                exit_reward = 1.0
            elif grid[old_pos_r][old_pos_c] == '-1':
                exit_reward = -1.0
            reward_sum += exit_reward
            experience += f'Reward received: {exit_reward}\n'
            experience += 'New state:\n'
            experience += parse.grid_to_str(grid)
            experience += '\n'
            experience += f"Cumulative reward sum: {round(reward_sum,2)}"
            break
        actual_dir = get_dir_from_intended(intended_dir, problem.noise)
        step_reward = problem.living_reward
        reward_sum += step_reward
        player_pos = execute_dir(grid, player_pos, actual_dir)
        experience += f"Taking action: {actual_dir} (intended: {intended_dir})\n"
        experience += f"Reward received: {step_reward}\n"
        experience += 'New state:\n'
        experience += parse.grid_to_str_with_player_pos(grid, player_pos)
        experience += '\n'
        experience += f"Cumulative reward sum: {round(reward_sum,2)}\n"

    return experience


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    # test_case_id = 1
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)


def test_random():
    import random
    from collections import Counter
    seed = 2
    if seed != -1:
        random.seed(seed, version=1)
    n = 0.1  # noise
    a = 'N'  # intended action
    d = {'N': ['N', 'E', 'W'], 'E': ['E', 'S', 'N'], 'S': ['S', 'W', 'E'], 'W': ['W', 'N', 'S']}
    l = []
    for _ in range(100000):
        l += random.choices(population=d[a], weights=[1 - n * 2, n, n])[0]
    print(Counter(l).keys())  # equals to list(set(words))
    print(Counter(l).values())  # counts the elements' frequency
    print(l[:5])

# test_random()
