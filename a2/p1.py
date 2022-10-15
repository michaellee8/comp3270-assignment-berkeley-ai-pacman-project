import sys, random, grader, parse
from parse import Problem


def random_play_single_ghost(problem: Problem):
    random.seed(problem.seed, version=1)

    # Your p1 code here
    solution = ''
    return solution


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)
