import sys, grader, parse

from parse import Problem
from typing import Tuple, List, Dict, TypeVar


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


def value_iteration(problem: Problem) -> str:
    n_rows = len(problem.grid)
    n_cols = len(problem.grid[0])
    grid = [[e for e in row] for row in problem.grid]
    return_value = ''
    values = [[0.0 for c in range(n_cols)] for r in range(n_rows)]
    policies = [['N' for c in range(n_cols)] for r in range(n_rows)]
    for k in range(problem.iterations):
        return_value += f"V_k={k}\n"
        return_value += parse.value_to_str_with_wall(values, grid)
        return_value += '\n'
        if k != 0:
            return_value += f"pi_k={k}\n"
            return_value += parse.dir_to_str_with_grid(policies, grid)
            return_value += '\n'
        new_values = [[e for e in row] for row in values]
        for r in range(n_rows):
            for c in range(n_cols):
                if is_float(grid[r][c]):
                    new_values[r][c] = float(problem.grid[r][c])
                    continue
                if grid[r][c] == '#':
                    new_values[r][c] = 0.0
                    continue
                else:
                    possible_policies = ['N', 'S', 'E', 'W']
                    possible_policy_values = []
                    for chosen_policy in possible_policies:
                        policy_value = 0.0
                        intended_dir = chosen_policy
                        actual_prob_dict = get_intended_dir_to_actual_dir_prob_dict(intended_dir, problem.noise)
                        for actual_dir, t in actual_prob_dict.items():
                            new_pos_r, new_pos_c = execute_dir(grid, (r, c), actual_dir)
                            policy_value += t * (
                                    problem.living_reward + problem.discount * values[new_pos_r][new_pos_c])
                        possible_policy_values.append(policy_value)
                    new_value = max(possible_policy_values)
                    new_policy = possible_policies[
                        max(range(len(possible_policy_values)), key=lambda i: possible_policy_values[i])]
                    new_values[r][c] = new_value
                    policies[r][c] = new_policy
                    continue
        values = new_values
    # skip last newline
    return return_value.rstrip()


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    # test_case_id = -4
    problem_id = 3
    grader.grade(problem_id, test_case_id, value_iteration, parse.read_grid_mdp_problem_p3)
