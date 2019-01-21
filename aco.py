import random


class ACO:
    def __init__(self, init_state, operators, goals):
        self.init_state = init_state
        self.operators = operators
        self.goals = goals

        self.ants = 10
        self.iterations = 5000
        self.alpha = 2
        self.beta = 5
        self.rho = 0.15
        self.max_length = 100

        self.pheromone = {}  # (state, action) -> pheromone level
        self.evaluation = {}  # (state, action) -> heuristic value

    def _choose_action(self, probs):
        total = sum(map(lambda x: x[0], probs))
        r = random.uniform(0, total)
        acum = 0
        for prob, action in probs:
            acum += prob
            if acum >= r:
                return prob, action
        raise RuntimeError('aaaaaaaaaaaaaaaaaaaaaaaaaa')

    def _evaluate_plan(self, plan):
        t = 0
        for i, (_, _, prob) in enumerate(plan):
            if prob > plan[t][1]:
                t = i
        return t, plan[t][1] if plan else -1

    def _evaluate_step(self, state, action):
        result = self.evaluation.get((state, action), None)

        if result is not None:
            return result

        state = state.apply(action)
        if not state:
            result = 0
        else:
            h = ff(state, self.operators, self.goals)
            result = 1 / h if h else 2 ** 32
        self.evaluation[(state, action)] = result
        return result

    def _get_probability(self, state, action):
        a = self.alpha
        b = self.beta

        num = self.pheromone[(state, action)] ** a * self._evaluate_step(state, action) ** b
        den = sum(
            (self.pheromone[(state, op)] ** a * self._evaluate_step(state, op) ** b for op in self.operators)
        )
        return num / den

    def _is_improvement(self, plan_a, plan_b):
        t_a, prob_a = self._evaluate_plan(plan_a)
        t_b, prob_b = self._evaluate_plan(plan_b)

        return prob_a > prob_b or (prob_a == prob_b and t_a < t_b)

    def _quality(self, plan):
        t, prob = self._evaluate_plan(plan)
        return (1 / (1 + 1 / prob)) * (1 / (1 + t))

    def _update_pheromones(self, s_best, s_iter):
        q_best = self._quality(s_best)
        q_iter = self._quality(s_iter)

        updates = {}

        for state, action, prob in s_best:
            p = updates.get((state, action), 0)
            updates[(state, action)] = p + q_best / (q_best + q_iter)

        for state, action, prob in s_iter:
            p = updates.get((state, action), 0)
            updates[(state, action)] = p + q_iter / (q_best + q_iter)

        for (state, action), p in updates.items():
            tau = self.pheromone.get((state, action), 0)
            self.pheromone[(state, action)] = (1 - self.rho) * tau + self.rho * updates[(state, action)]

    def solve(self):
        s_best = []
        for _ in range(self.iterations):
            s_iter = []

            for m in range(self.ants):
                s_p = []
                state = self.init_state

                for i in range(self.max_length):
                    probs = []
                    for op in self.operators:
                        probs.append((self._get_probability(state, op), op))
                    prob, a_k = self._choose_action(probs)
                    s_p.append((state, a_k, prob))
                    state = state.apply(a_k)

                if self._is_improvement(s_p, s_iter):
                    s_iter = s_p

            if self._is_improvement(s_iter, s_best):
                s_best = s_iter

            self._update_pheromones(s_best, s_iter)


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

    layers.reverse()
    actions.reverse()

    current_goals = set(goals)
    result = []
    for l, a in zip(layers[1:], actions):
        next_goals = set()
        result.append(set())
        for g in list(current_goals):
            if g in l:
                next_goals.add(g)
                continue
            for o in a:
                if g in o.effect_pos:
                    result[-1].add(o)
                    current_goals.remove(g)
                    next_goals.update(o.precondition_pos)
                    break
        next_goals.update(current_goals)
        current_goals = next_goals

    return sum(map(lambda s: len(s), result))
