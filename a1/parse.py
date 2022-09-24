from dataclasses import dataclass, field
import os, sys
from typing import List, Dict, Set
from collections import defaultdict
import logging


@dataclass
class Problem:
    start_state: str = field(default_factory=str)
    goal_state: Set[str] = field(default_factory=set)
    heuristic: Dict[str, float] = field(default_factory=dict)
    state_transitions: Dict[str, Dict[str, float]] = field(default_factory=lambda: defaultdict(dict))


QueenProblem = List[List[bool]]
QueenAnswer = List[List[int]]


def read_graph_search_problem(file_path) -> Problem:
    ret = Problem()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            splits = line.strip().split(' ')
            if splits[0] == 'goal_states:':
                ret.goal_state = set(splits[1:])
                continue
            elif len(splits) == 2:
                if splits[0] == 'start_state:':
                    ret.start_state = splits[1]
                    continue
                else:
                    ret.heuristic[splits[0]] = float(splits[1])
                    continue
            elif len(splits) == 3:
                ret.state_transitions[splits[0]][splits[1]] = float(splits[2])
                continue
            logging.error(f'invalid line when parsing problem: {line}')
    return ret


def read_8queens_search_problem(file_path) -> QueenProblem:
    problem: QueenProblem = [[False for x in range(8)] for y in range(8)]
    with open(file_path, 'r', encoding='utf-8') as f:
        line_idx = 0
        for line in f:
            splits = line.strip().split(' ')
            for split_idx in range(8):
                if splits[split_idx] == '.':
                    problem[line_idx][split_idx] = False
                elif splits[split_idx] == 'q':
                    problem[line_idx][split_idx] = True
                else:
                    logging.error(f'invalid line when parsing queen problem: {line}')
            line_idx += 1
    return problem


if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        if int(problem_id) <= 5:
            problem = read_graph_search_problem(os.path.join('test_cases', 'p' + problem_id, test_case_id + '.prob'))
        else:
            problem = read_8queens_search_problem(os.path.join('test_cases', 'p' + problem_id, test_case_id + '.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')
