import random
import sys
import parse
import time
import os
import copy
from parse import Problem, GameBoard, ImpossibleCaseError
from typing import Tuple, Union

# This number should be large enough
INF = float('inf')


def calculate_pacman_score(gm: GameBoard) -> int:
    if gm.game_ended():
        if gm.player_eaten:
            # return gm.score_final() * 50 - INF << 15
            return gm.score_final() * 50
        else:
            return gm.score_final() * 50

    # Prioritize game goals
    s = gm.score_final() * 50

    player_r, player_c = gm.player_position
    min_distance_to_food = gm.player_min_distance_to_food()
    distances_to_ghost = [abs(player_r - ghost_r) + abs(player_c - ghost_c) for ghost_r, ghost_c in gm.ghost_positions]
    # min_distance_to_ghost = min(distances_to_ghost)
    #
    # s += min_distance_to_ghost - min_distance_to_food

    sum_distance_to_ghost = sum(distances_to_ghost)
    s += sum_distance_to_ghost - 4 * min_distance_to_food

    # if gm.game_ended() and gm.player_eaten:
    #     # prevent being eaten at all cost
    #     s -= INF // 16

    return s


def expecti_max_search(gm: GameBoard, depth: int) -> Tuple[float, Union[str, None]]:
    if depth == 0 or gm.game_ended():
        return calculate_pacman_score(gm), None
    next_character = gm.next_move_character()
    if next_character not in ['W', 'X', 'Y', 'Z'] and next_character in ['P']:
        # maximizing player
        v = float('-inf')
        ret_move = None
        for direction, _ in gm.get_possible_next_moves():
            v2, direction2 = expecti_max_search(
                gm.execute_move(next_character, direction),
                depth - 1,
            )
            if v2 > v:
                v, ret_move = v2, direction
        return v, ret_move
    elif next_character in ['W', 'X', 'Y', 'Z'] and next_character not in ['P']:
        # random player
        v = 0
        ret_move = None
        num_next_moves = len(gm.get_possible_next_moves())
        for direction, _ in gm.get_possible_next_moves():
            v2, direction2 = expecti_max_search(
                gm.execute_move(next_character, direction),
                depth - 1,
            )
            v += v2 / num_next_moves
        return v, ret_move
    else:
        raise ImpossibleCaseError()


def expecti_max_mulitple_ghosts(problem: Problem, k: int) -> Tuple[str, str]:
    solution = ''
    random.seed(problem.seed, version=1)

    gm = GameBoard.from_problem(problem)

    solution += f"seed: {gm.seed}\n"
    solution += f"{gm.move_count}\n"
    solution += gm.to_string_board()

    depth = k * (len(gm.ghost_names) + 1)

    while True:
        moving_character = gm.next_move_character()
        if moving_character == 'P':
            _, picked_direction = expecti_max_search(gm, depth)
        else:
            possible_moves = gm.get_possible_next_moves()
            possible_directions = [nm[0] for nm in possible_moves]
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
    problem_id = 6
    file_name_problem = str(test_case_id) + '.prob'
    file_name_sol = str(test_case_id) + '.sol'
    path = os.path.join('test_cases', 'p' + str(problem_id))
    problem = parse.read_layout_problem(os.path.join(path, file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:', test_case_id)
    print('k:', k)
    print('num_trials:', num_trials)
    print('verbose:', verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = expecti_max_mulitple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count / num_trials * 100
    end = time.time()
    print('time: ', end - start)
    print('win %', win_p)
