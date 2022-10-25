from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import List, Tuple
import copy


class LoopLabel(Exception):
    pass


class ImpossibleCaseError(Exception):
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
        self.food_positions: set = set()

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
                    gb.food_positions.add((row, col))

        ghosts.sort(key=lambda gh: gh[0])
        for g in ghosts:
            gb.ghost_names.append(g[0])
            gb.ghost_positions.append((g[1], g[2]))

        gb.width = prob.width
        gb.height = prob.height
        gb.seed = prob.seed
        return gb

    def player_steps_taken(self) -> int:
        ret = self.move_count // (1 + len(self.ghost_names))
        if self.move_count % (1 + len(self.ghost_names)) >= 1:
            ret += 1
        return ret

    def score_without_end(self) -> int:
        return self.player_steps_taken() * GameBoard.PACMAN_MOVING_SCORE + self.num_food_eaten * GameBoard.EAT_FOOD_SCORE

    def score_final(self) -> int:
        s = self.score_without_end()
        if not self.game_ended():
            return s
        if self.player_eaten:
            return s + GameBoard.PACMAN_EATEN_SCORE
        if self.num_food_left == 0:
            return s + GameBoard.PACMAN_WIN_SCORE
        raise ImpossibleCaseError

    def next_move_character(self) -> str:
        return (['P'] + self.ghost_names)[self.move_count % (1 + len(self.ghost_names))]

    def get_pos_for_character(self, ch: str) -> Tuple[int, int]:
        if ch == 'P':
            return self.player_position
        gh_idx = self.ghost_names.index(ch)
        return self.ghost_positions[gh_idx]

    def set_pos_for_character(self, ch: str, pos: Tuple[int, int]):
        if ch == 'P':
            self.player_position = pos
            return
        gh_idx = self.ghost_names.index(ch)
        self.ghost_positions[gh_idx] = pos

    def is_wall(self, pos: Tuple[int, int]) -> bool:
        r, c = pos
        return self.board[r][c] == '%'

    def is_food(self, pos: Tuple[int, int]) -> bool:
        r, c = pos
        return self.board[r][c] == '.'

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
        return [nm for nm in next_moves if
                not self.is_wall(nm[1]) and (next_character == 'P' or nm[1] not in self.ghost_positions)]

    def pacman_won(self) -> bool:
        if not self.game_ended():
            raise ImpossibleCaseError()
        return not self.player_eaten

    def make_copy(self):
        return copy.deepcopy(self)

    def execute_move(self, character: str, direction: str) -> GameBoard:
        ngb = self.make_copy()
        if ngb.next_move_character() != character:
            raise ValueError()
        if ngb.game_ended():
            raise ImpossibleCaseError()
        _, next_pos = [nm for nm in ngb.get_possible_next_moves() if nm[0] == direction][0]
        ngb.set_pos_for_character(character, next_pos)
        if ngb.player_position in ngb.ghost_positions:
            # pacman eaten
            ngb.player_eaten = True
        elif self.is_food(ngb.player_position):
            r, c = ngb.player_position
            ngb.board[r][c] = ' '
            ngb.num_food_left -= 1
            ngb.num_food_eaten += 1
            ngb.food_positions.remove((r, c))
        ngb.move_count += 1
        return ngb

    def to_string_board(self) -> str:
        ret = ''
        for r in range(self.height):
            for c in range(self.width):
                if self.player_position == (r, c) and not self.player_eaten:
                    ret += 'P'
                elif (r, c) in self.ghost_positions:
                    gh_idx = self.ghost_positions.index((r, c))
                    ret += self.ghost_names[gh_idx]
                else:
                    ret += self.board[r][c]
            ret += '\n'
        return ret

    def player_min_distance_to_food(self) -> int:
        if self.num_food_left == 0:
            # No food, we won
            return -10000
        NEAR_SEARCH_DEPTH = 3
        player_r, player_c = self.player_position
        for depth in range(1 + NEAR_SEARCH_DEPTH):
            for r in range(player_r - depth, player_r + depth + 1):
                for c in range(player_c - depth, player_c + depth + 1):
                    if r in range(self.height) and c in range(self.width) and self.board[r][c] == '.':
                        return depth

        distances_to_food = [abs(player_r - food_r) + abs(player_c - food_c) for food_r, food_c in
                             self.food_positions]
        return min(distances_to_food)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases', 'p' + problem_id, test_case_id + '.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')
