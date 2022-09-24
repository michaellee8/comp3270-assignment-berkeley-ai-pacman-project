import sys, grader
from parse import Problem
import parse
from collections import deque
from typing import List

def bfs_search(problem: Problem) -> str:
    qu = deque([[problem.start_state]])
    exploration_order = [problem.start_state]
    explored = {problem.start_state}
    while qu:
        next_path = qu.pop()
        for end_state, cost in problem.state_transitions[next_path[-1]].items():
            if end_state not in explored:
                if end_state in problem.goal_state:
                    return f"{' '.join(exploration_order)}\n{' '.join(next_path + [end_state])}"
                qu.append(next_path + [end_state])
                exploration_order.append(end_state)
                explored.add(end_state)

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 2
    grader.grade(problem_id, test_case_id, bfs_search, parse.read_graph_search_problem)