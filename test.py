import json
import sys
import time

import aco

from domain import DomainProblem
from state import State


def main(argv):
    demonumber = int(argv[1])
    domainfile = "./examples-pddl/domain-0%d.pddl" % demonumber
    problemfile = "./examples-pddl/problem-0%d.pddl" % demonumber
    domprob = DomainProblem(domainfile, problemfile)

    with open(argv[2]) as file:
        config = json.load(file)

    initial = State(frozenset({tuple(atom.predicate) for atom in domprob.initialstate()}))
    goals = set(tuple(atom.predicate) for atom in domprob.goals())

    ground_operators = []
    for op in domprob.operators():
        for o in domprob.ground_operator(op):
            ground_operators.append(o)

    planner = aco.ACO(initial, ground_operators, goals, config)
    start = time.time()
    s = planner.solve()

    for i, action in enumerate(map(lambda x: x[1], s)):
        print(f'{i + 1} \t {action.operator_name} {str(action.variable_list)}')

    print()
    print(f'IS GOAL:\t{s[-1][0].apply(s[-1][1]).is_goal(goals)}')
    print('TIME:\t\t%.2f s' % (time.time() - start))


if __name__ == '__main__':
    main(sys.argv)
