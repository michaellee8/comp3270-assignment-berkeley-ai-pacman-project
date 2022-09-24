import sys, parse, grader
from parse import Problem
import parse
from collections import deque
from typing import List
import heapq


def greedy_search(problem: Problem):
    pq = []
    exploration_order = []
    exploration_order_added = set()
    heapq.heappush(pq, (problem.heuristic[problem.start_state], [problem.start_state]))
    while pq:
        current_cost, current_path = heapq.heappop(pq)
        if current_path[-1] in problem.goal_state:
            return f"{' '.join(exploration_order)}\n{' '.join(current_path)}"
        if current_path[-1] not in exploration_order_added:
            exploration_order.append(current_path[-1])
            exploration_order_added.add(current_path[-1])
        for next_node in problem.state_transitions[current_path[-1]]:
            heapq.heappush(pq, (problem.heuristic[next_node], current_path + [next_node]))


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 4
    grader.grade(problem_id, test_case_id, greedy_search, parse.read_graph_search_problem)
