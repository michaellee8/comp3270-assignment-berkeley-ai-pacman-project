import sys, parse, grader
from parse import Problem
import parse
from collections import deque
from typing import List
import heapq


def ucs_search(problem: Problem):
    pq = []
    exploration_order = []
    exploration_order_added = set()
    heapq.heappush(pq, (0, [problem.start_state]))
    while pq:
        total_cost, path = heapq.heappop(pq)
        if path[-1] in problem.goal_state:
            return f"{' '.join(exploration_order)}\n{' '.join(path)}"
        if path[-1] not in exploration_order_added:
            exploration_order.append(path[-1])
            exploration_order_added.add(path[-1])
        for next_node, cost in problem.state_transitions[path[-1]].items():
            heapq.heappush(pq, (cost + total_cost, path + [next_node]))


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, ucs_search, parse.read_graph_search_problem)
