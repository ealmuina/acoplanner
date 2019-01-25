import json
import sys

from planner import run


def main(argv):
    tests = [
        ('domain-03', 'problem-03'),
        ('domain-04', 'problem-04'),
        ('driverlog', 'driverlog-01'),
        ('rover', 'rover-01')
    ]

    with open(argv[1]) as file:
        config = json.load(file)

    for domain, problem in tests:
        domainfile = "./examples-pddl/domains/%s.pddl" % domain
        problemfile = "./examples-pddl/problems/%s.pddl" % problem

        run(domainfile, problemfile, config)


if __name__ == '__main__':
    main(sys.argv)
