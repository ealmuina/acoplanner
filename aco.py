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
