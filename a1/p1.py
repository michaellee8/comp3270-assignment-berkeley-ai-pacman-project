import sys, grader
from parse import Problem
from collections import deque
from typing import List


def dfs_search(problem: Problem) -> str:
    qu = deque([[problem.start_state]])
    exploration_order = [problem.start_state]
    while qu:
        next_path = qu.pop()



if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, dfs_search, parse.read_graph_search_problem)
