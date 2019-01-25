import json
import os
import sys
import time

import aco

from domain import DomainProblem
from state import State


def run(domain, problem, config):
    print('==================================================')
    print(f'{os.path.split(domain)[-1]} --- {os.path.split(problem)[-1]}')
    print('==================================================')

    domprob = DomainProblem(domain, problem)

    initial = State(frozenset({tuple(atom.predicate) for atom in domprob.initialstate()}))
    goals = set(tuple(atom.predicate) for atom in domprob.goals())

    ground_operators = []
    for op in domprob.operators():
        for o in domprob.ground_operator(op):
            ground_operators.append(o)

    planner = aco.ACOPlanner(initial, ground_operators, goals, config)
    start = time.time()
    s = planner.solve()

    for i, action in enumerate(map(lambda x: x[1], s)):
        print(f'{i + 1} \t {action.operator_name} {str(action.variable_list)}')

    print('--------------------------------------------------')
    print(f'IS GOAL:\t{s[-1][0].apply(s[-1][1]).is_goal(goals)}')
    print('TIME:\t\t%.2f s' % (time.time() - start))
    print('--------------------------------------------------')


def main(argv):
    with open(argv[1]) as file:
        config = json.load(file)

    run(argv[2], argv[3], config)


if __name__ == '__main__':
    main(sys.argv)
