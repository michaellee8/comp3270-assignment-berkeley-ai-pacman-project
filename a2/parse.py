import copy
import os, sys
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict

CHARACTER_WALL = '%'
CHARACTER_GHOST = 'W'
CHARACTER_PACMAN = 'P'
CHARACTER_FOOD = '.'
CHARACTER_EMPTY = ' '


class LoopLabel(Exception):
    pass


@dataclass
class Problem:
    seed: int = 0
    width: int = 0
    height: int = 0
    board: List[List[str]] = field(default_factory=list)

    def __repr__(self) -> str:
        ret = ''
        ret += f"seed: {self.seed}\n"
        ret += f"width: {self.width}\n"
        ret += f"height: {self.height}\n"
        ret += f"board:\n"
        ret += '\n'.join([''.join(line) for line in self.board])
        return ret

    def __str__(self):
        ret = ''
        ret += f"seed: {self.seed}\n"
        ret += f"width: {self.width}\n"
        ret += f"height: {self.height}\n"
        ret += f"board:\n"
        ret += '\n'.join([''.join(line) for line in self.board])
        return ret


def board_to_str(board: List[List[str]]) -> str:
    return '\n'.join([''.join(line) for line in board])


def board_to_str_with_characters(board: List[List[str]], c_pos: Dict[str, List[int]]) -> str:
    b = copy.deepcopy(board)
    for c, pos in c_pos.items():
        b[pos[0]][pos[1]] = c
    return board_to_str(b)


def read_layout_problem(file_path: str) -> Problem:
    ret = Problem()
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        ret.seed = int(first_line.split(' ')[1])
        ret.board = [
            [
                c
                for c in list(line.strip())
            ]
            for line in f
        ]
        ret.height = len(ret.board)
        ret.width = len(ret.board[0])
    return ret


if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases', 'p' + problem_id, test_case_id + '.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')
