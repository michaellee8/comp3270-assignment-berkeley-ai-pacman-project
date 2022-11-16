import os
from typing import List
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
                ret.iterations = float(line.removeprefix('iterations: '))
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
