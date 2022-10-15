import os, sys
from dataclasses import dataclass, field
from enum import Enum
from typing import List

CHARACTER_WALL = '%'
CHARACTER_GHOST = 'W'
CHARACTER_PACMAN = 'P'
CHARACTER_FOOD = '.'
CHARACTER_EMPTY = ' '


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
