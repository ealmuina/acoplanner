class ACO:
    def __init__(self, alpha, beta, operators):
        self.alpha = alpha
        self.beta = beta
        self.operators = operators

        self.pheromone = {}  # (state, action) -> pheromone level
        self.evaluation = {}  # (state, action) -> heuristic value

    def _evaluate(self, state, action):
        result = self.evaluation.get((state, action), None)

        if result is not None:
            return result

        # TODO Do actual heuristics

        self.evaluation[(state, action)] = result
        return result

    def get_probability(self, state, action):
        a = self.alpha
        b = self.beta

        num = self.pheromone[(state, action)] ** a * self._evaluate(state, action) ** b
        den = sum(
            (self.pheromone[(state, a)] ** a * self._evaluate(state, a) ** b for a in self.operators)
        )
        return num / den


def ff(state, operators, goals):
    k = 0
    actions = []
    layers = [set(state.predicates)]

    while True:
        next_layer = set()
        next_actions = set()

        if goals.issubset(layers[-1]):
            break

        for op in operators:
            if op.precondition_pos.issubset(layers[-1]) and not op.effect_pos.issubset(layers[-1]):
                next_layer.update(op.effect_pos)
                next_actions.add(op)

        if not next_layer:
            return 2 ** 32

        next_layer.update(layers[-1])
        layers.append(next_layer)
        actions.append(next_actions)
        k += 1

    # TODO Build relaxed plan

    return k
