#
# Copyright 2015 Hernán M. Foffani
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#

import sys

from domain import DomainProblem

from state import State


def main(argv):
    demonumber = int(argv[1])
    domainfile = "./examples-pddl/domain-0%d.pddl" % demonumber
    problemfile = "./examples-pddl/problem-0%d.pddl" % demonumber
    domprob = DomainProblem(domainfile, problemfile)
    print()
    print("DOMAIN PROBLEM")
    print("objects")
    print("\t", domprob.worldobjects())
    print("operators")
    print("\t", list(domprob.operators()))
    print("init", )
    print("\t", domprob.initialstate())
    print("goal", )
    print("\t", domprob.goals())

    # print()
    # ops_to_test = {1: "op2", 2: "move", 3: "move", 4: "move", 5: "A1"}
    # op = ops_to_test[demonumber]
    # print("ground for operator", op, "applicable if (adjacent loc1 loc2)")
    # for o in domprob.ground_operator(op):
    #     if ("adjacent", "loc1", "loc2") in o.precondition_pos:
    #         print()
    #         print("\tvars", o.variable_list)
    #         print("\tpre+", o.precondition_pos)
    #         print("\tpre-", o.precondition_neg)
    #         print("\teff+", o.effect_pos)
    #         print("\teff-", o.effect_neg)

    initial = State(frozenset({tuple(atom.predicate) for atom in domprob.initialstate()}))
    space = {initial}

    ground_operators = []
    for op in domprob.operators():
        for o in domprob.ground_operator(op):
            ground_operators.append(o)

    pending = [initial]

    from aco import ff
    goals = set(tuple(atom.predicate) for atom in domprob.goals())
    print(ff(initial, ground_operators, goals))

    # while pending:
    #     current = pending.pop()
    #     for o in ground_operators:
    #         next_state = current.apply(o)
    #         if next_state and next_state not in space:
    #             pending.append(next_state)
    #             space.add(next_state)
    #
    #     print(len(space))


if __name__ == '__main__':
    main(sys.argv)
