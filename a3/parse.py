import os
from typing import List, Tuple
from dataclasses import dataclass, field


class Problem:
    # p1 | p2 | p3
    type: str = ''
    seed: int = -1
    discount: float = 0.0
    noise: float = 0.0
    living_reward: float = 0.0
    iterations: int = 0
    grid: List[List[str]] = field(default_factory=list)
    policy: List[List[str]] = field(default_factory=list)


# Assuming python language level 3.9

def parse_problem(file_path: str) -> Problem:
    ret = Problem()
    with open(file_path, 'r', encoding='utf-8') as f:
        current_field = ''
        current_board = []

        def reset_board_parser():
            nonlocal current_board
            nonlocal current_field
            if current_field == '':
                return
            ret.__setattr__(current_field, current_board)
            current_field = ''
            current_board = []

        for line in f:
            if line.startswith('seed: '):
                ret.seed = int(line.removeprefix('seed: '))
                continue
            if line.startswith('discount: '):
                ret.discount = float(line.removeprefix('discount: '))
                continue
            if line.startswith('noise: '):
                ret.noise = float(line.removeprefix('noise: '))
                continue
            if line.startswith('livingReward: '):
                ret.living_reward = float(line.removeprefix('livingReward: '))
                continue
            if line.startswith('iterations: '):
                ret.iterations = int(line.removeprefix('iterations: '))
                continue
            if line.startswith('grid:'):
                reset_board_parser()
                current_field = 'grid'
                continue
            if line.startswith('policy:'):
                reset_board_parser()
                current_field = 'policy'
                continue
            current_board.append(line.strip().split())
        reset_board_parser()

    return ret


def read_grid_mdp_problem_p1(file_path: str) -> Problem:
    ret = parse_problem(file_path)
    ret.type = 'p1'
    return ret


def read_grid_mdp_problem_p2(file_path: str) -> Problem:
    ret = parse_problem(file_path)
    ret.type = 'p2'
    return ret


def read_grid_mdp_problem_p3(file_path: str) -> Problem:
    ret = parse_problem(file_path)
    ret.type = 'p3'
    return ret


def grid_to_str(b: List[List[str]]) -> str:
    return '\n'.join([''.join([e.rjust(5, ' ') for e in row]) for row in b])


def grid_to_str_with_player_pos(b: List[List[str]], pos: Tuple[int, int]) -> str:
    cb = [[e for e in row] for row in b]
    cb[pos[0]][pos[1]] = 'P'
    return '\n'.join([''.join([e.rjust(5, ' ') for e in row]) for row in cb])


def value_to_str(b: List[List[float]]) -> str:
    return '\n'.join([''.join([f"|{e:7.2f}|" for e in row]) for row in b])


def value_to_str_with_wall(b: List[List[float]], grid: List[List[str]]) -> str:
    return '\n'.join(
        [''.join([f"|{e:7.2f}|" if grid[r][c] != '#' else '| ##### |' for c, e in enumerate(row)]) for r, row in
         enumerate(b)])


def dir_to_str(b: List[List[str]]) -> str:
    return '\n'.join([''.join([f"|{e.rjust(3, ' ')}|" for e in row]) for row in b])
