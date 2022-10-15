import os, sys
from dataclasses import dataclass, field
from enum import Enum
from typing import List


class Character(Enum):
    Wall = '%'
    Ghost = 'W'
    Pacman = 'P'
    Food = '.'
    Empty = ' '


@dataclass
class Problem:
    seed: int = 0
    width: int = 0
    height: int = 0
    board: List[List[Character]] = field(default_factory=list)

    def __repr__(self) -> str:
        ret = ''
        ret += f"seed: {self.seed}\n"
        ret += f"width: {self.width}\n"
        ret += f"height: {self.height}\n"
        ret += f"board:\n"
        ret += '\n'.join([''.join(line) for line in self.board])


def input_text_to_character(t: str) -> Character:
    if t == '%':
        return Character.Wall
    if t == 'W':
        return Character.Ghost
    if t == 'P':
        return Character.Pacman
    if t == '.':
        return Character.Food
    return Character.Empty


def read_layout_problem(file_path: str) -> Problem:
    ret = Problem()
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        ret.seed = int(first_line.split(' ')[1])
        ret.board = [
            [
                input_text_to_character(c)
                for c in line.strip().split()
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
