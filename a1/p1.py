import sys, grader
from parse import Problem
import parse
from collections import deque
from typing import List


def dfs_search(problem: Problem) -> str:
    qu = deque([[problem.start_state]])
    exploration_order = [problem.start_state]
    explored = {problem.start_state}
    while qu:
        next_path = qu.pop()
        if next_path[-1] in problem.goal_state:
            return f"{' '.join(exploration_order)}\n{' '.join(next_path)}"
        for end_state, cost in problem.state_transitions[next_path[-1]].items():
            if end_state not in explored:
                qu.append(next_path + [end_state])
                exploration_order.append(end_state)
                explored.add(end_state)
                break


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, dfs_search, parse.read_graph_search_problem)
