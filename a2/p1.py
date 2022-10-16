import sys, random, grader, parse
from parse import Problem, board_to_str, board_to_str_with_characters
import copy


def random_play_single_ghost(problem: Problem) -> str:
    random.seed(problem.seed, version=1)

    board = copy.deepcopy(problem.board)

    # (row, col)
    ghost_position = [-1, -1]
    pacman_position = [-1, -1]
    num_food = 0

    score = 0

    is_eaten = False

    def is_wall(r: int, c: int) -> bool:
        return board[r][c] == '%'

    def is_food(r: int, c: int) -> bool:
        return board[r][c] == '.'

    def is_ghost(r: int, c: int) -> bool:
        return board[r][c] == 'W'

    def is_pacman_walkable(r: int, c: int) -> bool:
        return not is_wall(r, c)

    def is_pacman(r: int, c: int) -> bool:
        return r == pacman_position[0] and c == pacman_position[1]

    solution = ''

    solution += f"seed: {problem.seed}\n"
    solution += f"0\n"
    solution += board_to_str(board)
    solution += "\n"

    for row in range(problem.height):
        for col in range(problem.width):
            if board[row][col] == 'W':
                ghost_position = [row, col]
                board[row][col] = ' '
            if board[row][col] == 'P':
                pacman_position = [row, col]
                board[row][col] = ' '
            if board[row][col] == '.':
                num_food += 1

    round_num = 0
    while True:
        round_num += 1
        if round_num % 2 == 1:
            # pacman round
            possible_moves = []
            if is_pacman_walkable(pacman_position[0] - 1, pacman_position[1]):
                possible_moves.append('N')
            if is_pacman_walkable(pacman_position[0] + 1, pacman_position[1]):
                possible_moves.append('S')
            if is_pacman_walkable(pacman_position[0], pacman_position[1] - 1):
                possible_moves.append('W')
            if is_pacman_walkable(pacman_position[0], pacman_position[1] + 1):
                possible_moves.append('E')
            possible_moves.sort()
            decided_move = random.choice(possible_moves)
            if decided_move == 'N':
                pacman_position[0] -= 1
            if decided_move == 'S':
                pacman_position[0] += 1
            if decided_move == 'W':
                pacman_position[1] -= 1
            if decided_move == 'E':
                pacman_position[1] += 1
            score -= 1
            if is_food(pacman_position[0], pacman_position[1]):
                score += 10
                board[pacman_position[0]][pacman_position[1]] = ' '
                num_food -= 1
            if is_pacman(ghost_position[0], ghost_position[1]):
                score -= 500
                is_eaten = True
            solution += f"{round_num}: P moving {decided_move}\n"
            if num_food <= 0:
                score += 500
                break
            if is_eaten:
                break
        else:
            # ghost round
            possible_moves = []
            if not is_wall(ghost_position[0] - 1, ghost_position[1]):
                possible_moves.append('N')
            if not is_wall(ghost_position[0] + 1, ghost_position[1]):
                possible_moves.append('S')
            if not is_wall(ghost_position[0], ghost_position[1] - 1):
                possible_moves.append('W')
            if not is_wall(ghost_position[0], ghost_position[1] + 1):
                possible_moves.append('E')
            possible_moves.sort()
            decided_move = random.choice(possible_moves)
            if decided_move == 'N':
                ghost_position[0] -= 1
            if decided_move == 'S':
                ghost_position[0] += 1
            if decided_move == 'W':
                ghost_position[1] -= 1
            if decided_move == 'E':
                ghost_position[1] += 1
            if is_pacman(ghost_position[0], ghost_position[1]):
                score -= 500
                is_eaten = True
            solution += f"{round_num}: W moving {decided_move}\n"
            if is_eaten:
                break
        solution += board_to_str_with_characters(board, {
            'P': pacman_position,
            'W': ghost_position
        })
        solution += "\n"
        solution += f"score: {score}\n"

    if is_eaten:
        solution += board_to_str_with_characters(board, {
            'W': ghost_position
        })
    else:
        solution += board_to_str_with_characters(board, {
            'P': pacman_position,
            'W': ghost_position
        })

    solution += "\n"
    solution += f"score: {score}\n"

    if is_eaten:
        solution += "WIN: Ghost"
    else:
        solution += "WIN: Pacman"

    return solution


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)
