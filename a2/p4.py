import random
import parse
import time
import os
import copy
from parse import Problem, GameBoard
from typing import Tuple
import sys


def calculate_score(gm: GameBoard) -> int:
    if gm.game_ended():
        if gm.player_eaten:
            return gm.score_final() * 50 - sys.maxsize // 2
        else:
            return gm.score_final() * 50

    # Prioritize game goals
    s = gm.score_final() * 50

    player_r, player_c = gm.player_position
    min_distance_to_food = gm.player_min_distance_to_food()
    distances_to_ghost = [abs(player_r - ghost_r) + abs(player_c - ghost_c) for ghost_r, ghost_c in gm.ghost_positions]
    min_distance_to_ghost = min(distances_to_ghost)

    s += min_distance_to_ghost - min_distance_to_food

    if gm.game_ended() and gm.player_eaten:
        # prevent being eaten at all cost
        s -= sys.maxsize // 2

    return s


def better_play_mulitple_ghosts(problem: Problem) -> Tuple[str, str]:
    # It will take some time to run but in complex cases but given any modern CPU it
    # will stop in 5 minutes.
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
        if moving_character == 'P':
            scores = [(i, calculate_score(gm.execute_move(moving_character, possible_directions[i]))) for i in
                      range(len(possible_directions))]
            best_idx, _ = max(scores, key=lambda sc: sc[1])
            picked_direction = possible_directions[best_idx]
        else:
            picked_direction = random.choice(possible_directions)
        gm = gm.execute_move(moving_character, picked_direction)
        solution += f"{gm.move_count}: {moving_character} moving {picked_direction}\n"
        solution += gm.to_string_board()
        solution += f"score: {gm.score_final()}\n"

        if gm.game_ended():
            if gm.pacman_won():
                solution += "WIN: Pacman"
            else:
                solution += "WIN: Ghost"
            break

    return solution, 'Pacman' if gm.pacman_won() else 'Ghost'


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 4
    file_name_problem = str(test_case_id) + '.prob'
    file_name_sol = str(test_case_id) + '.sol'
    path = os.path.join('test_cases', 'p' + str(problem_id))
    problem = parse.read_layout_problem(os.path.join(path, file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:', test_case_id)
    print('num_trials:', num_trials)
    print('verbose:', verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = better_play_mulitple_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count / num_trials * 100
    end = time.time()
    print('time: ', end - start)
    print('win %', win_p)
