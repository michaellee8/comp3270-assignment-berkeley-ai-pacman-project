import sys
import grader
import parse
from parse import Problem, GameBoard
import random


def random_play_multiple_ghosts(problem: Problem) -> str:
    solution = ''
    random.seed(problem.seed, version=1)

    gm = GameBoard.from_problem(problem)

    solution += f"seed: {gm.seed}\n"
    solution += f"{gm.move_count}\n"
    solution += gm.to_string_board()

    while True:
        moving_character = gm.next_move_character()
        possible_moves = gm.get_possible_next_moves()
        possible_directions = [nm[0] for nm in possible_moves]
        if possible_directions:
            picked_direction = random.choice(possible_directions)
            gm = gm.execute_move(moving_character, picked_direction)
        else:
            picked_direction = ''
            gm = gm.make_copy()
            gm.move_count += 1
        solution += f"{gm.move_count}: {moving_character} moving {picked_direction}\n"
        solution += gm.to_string_board()
        solution += f"score: {gm.score_final()}\n"

        if gm.game_ended():
            if gm.pacman_won():
                solution += "WIN: Pacman"
            else:
                solution += "WIN: Ghost"
            break

    return solution


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, random_play_multiple_ghosts, parse.read_layout_problem)
