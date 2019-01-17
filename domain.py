import itertools

import pddlpy


class DomainProblem(pddlpy.DomainProblem):
    def _instantiate(self, variables):
        vargroundspace = []
        for vname, t in variables:
            c = []
            for symb in self._typesymbols(t):
                c.append((vname, symb))
            vargroundspace.append(c)
        return itertools.product(*vargroundspace)
