import json
import sys
import time

import aco

from domain import DomainProblem
from state import State


def test(domain, problem, config):
    domainfile = "./examples-pddl/domains/%s.pddl" % domain
    problemfile = "./examples-pddl/problems/%s.pddl" % problem
    domprob = DomainProblem(domainfile, problemfile)

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

    print('--------------------------------------------------')
    print(f'IS GOAL:\t{s[-1][0].apply(s[-1][1]).is_goal(goals)}')
    print('TIME:\t\t%.2f s' % (time.time() - start))
    print('--------------------------------------------------')


def main(argv):
    tests = [
        ('domain-01', 'problem-01'),
        ('domain-03', 'problem-03')
    ]

    with open(argv[1]) as file:
        config = json.load(file)

    for domain, problem in tests:
        print('==================================================')
        print(f'{domain} --- {problem}')
        print('==================================================')
        test(domain, problem, config)
        print()


if __name__ == '__main__':
    main(sys.argv)
