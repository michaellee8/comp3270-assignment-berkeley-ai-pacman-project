from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import copy


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


class GameBoard:
    EAT_FOOD_SCORE = 10
    PACMAN_EATEN_SCORE = -500
    PACMAN_WIN_SCORE = 500
    PACMAN_MOVING_SCORE = -1

    def __init__(self):
        self.ghost_names: List[str] = []
        self.ghost_positions: List[Tuple[int, int]] = []
        self.player_position: Tuple[int, int] = (0, 0)
        self.move_count: int = 0
        self.seed: int = 0
        self.board: List[List[str]] = []
        self.width: int = 0
        self.height: int = 0

        self.num_food_left: int = 0
        self.num_food_eaten: int = 0
        self.player_eaten: bool = False

    def game_ended(self):
        return self.num_food_left == 0 or self.player_eaten

    @staticmethod
    def from_problem(prob: Problem) -> GameBoard:
        gb = GameBoard()
        gb.board = copy.deepcopy(prob.board)
        ghosts: List[Tuple[str, int, int]] = []
        for row in range(prob.height):
            for col in range(prob.width):
                if gb.board[row][col] == 'P':
                    gb.player_position = (row, col)
                    gb.board[row][col] = ' '
                if gb.board[row][col] in ['W', 'X', 'Y', 'Z']:
                    ghosts.append((gb.board[row][col], row, col))
                    gb.board[row][col] = ' '
                if gb.board[row][col] == '.':
                    gb.num_food_left += 1

        ghosts.sort(key=lambda gh: gh[0])
        for g in ghosts:
            gb.ghost_names.append(g[0])
            gb.ghost_positions.append((g[1], g[2]))
        return gb

    def player_steps_taken(self) -> int:
        ret = self.move_count // (1 + len(self.ghost_names))
        if self.move_count % (1 + len(self.ghost_names)) >= 1:
            ret += 1
        return ret

    def score_without_end(self) -> int:
        return self.player_steps_taken() * GameBoard.PACMAN_MOVING_SCORE + self.num_food_eaten * GameBoard.PACMAN_EATEN_SCORE

    def score_final(self) -> int:
        s = self.score_without_end()

    def next_move_character(self) -> str:
        return (['P'] + self.ghost_names)[(self.move_count + 1) % (1 + len(self.ghost_names))]

    def get_pos_for_character(self, ch: str) -> Tuple[int, int]:
        if ch == 'P':
            return self.player_position
        gh_idx = self.ghost_names.index(ch)
        return self.ghost_positions[gh_idx]

    def is_wall(self, pos: Tuple[int, int]) -> bool:
        r, c = pos
        return self.board[r][c] == '%'

    @staticmethod
    def compute_next_moves(pos: Tuple[int, int]) -> List[Tuple[str, Tuple[int, int]]]:
        r, c = pos
        return [
            (
                'E',
                (r, c + 1)
            ),
            (
                'N',
                (r - 1, c)
            ),
            (
                'S',
                (r + 1, c)
            ),
            (
                'W',
                (r, c - 1)
            )
        ]

    def get_possible_next_moves(self) -> List[Tuple[str, Tuple[int, int]]]:
        if self.game_ended():
            return []
        next_character = self.next_move_character()
        next_character_pos = self.get_pos_for_character(next_character)
        next_moves = GameBoard.compute_next_moves(next_character_pos)
        return [nm for nm in next_moves if not self.is_wall(nm[1])]

    def make_copy(self):
        return copy.deepcopy(self)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases', 'p' + problem_id, test_case_id + '.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')
