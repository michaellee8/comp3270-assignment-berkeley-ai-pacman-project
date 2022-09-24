import sys, grader
from parse import Problem
import parse
from collections import deque
from typing import List


def dfs_search(problem: Problem) -> str:
    qu = deque([problem.start_state])
    exploration_order = [problem.start_state]
    explored = {problem.start_state}

    def perform_search():
        next_node = qu[-1]
        has_valid_child = False
        for target in reversed(list(problem.state_transitions[next_node].keys())):
            if target in explored:
                continue
            if target in problem.goal_state:
                return f"{' '.join(exploration_order)}\n{' '.join(list(qu) + [target])}"
            has_valid_child = True
            qu.append(target)
            explored.add(target)
            exploration_order.append(target)
            ret2 = perform_search()
            if ret2 is not None:
                return ret2
        if not has_valid_child:
            qu.pop()

    while qu:
        ret = perform_search()
        if ret is not None:
            return ret
        # next_node = qu[-1]
        # has_valid_child = False
        # for target, cost in reversed(list(problem.state_transitions[next_node].items())):
        #     if target not in explored:
        #         if target in problem.goal_state:
        #             return f"{' '.join(exploration_order)}\n{' '.join(list(qu) + [target])}"
        #         has_valid_child = True
        #         qu.append(target)
        #         explored.add(target)
        #         exploration_order.append(target)
        #         break
        # if not has_valid_child:
        #     qu.pop()


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, dfs_search, parse.read_graph_search_problem)
