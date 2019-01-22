import random

from heuristics import ff


class ACO:
    def __init__(self, init_state, operators, goals, config):
        self.init_state = init_state
        self.operators = operators
        self.goals = goals

        for key, value in config.items():
            self.__setattr__(key, value)

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

    def _evaluate_plan(self, plan):
        t = 0
        for i, (_, _, prob) in enumerate(plan):
            if prob > plan[t][2]:
                t = i
        return t, plan[t][2] if plan else -1

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

        pheromone = self.pheromone.get((state, action), 1)

        num = pheromone ** a * self._evaluate_step(state, action) ** b
        den = sum(
            (pheromone ** a * self._evaluate_step(state, op) ** b for op in state.applicable_actions(self.operators))
        )
        return num / den if den else 0

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
            tau = self.pheromone.get((state, action), 1)
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
                    for op in state.applicable_actions(self.operators):
                        p = self._get_probability(state, op)
                        probs.append((p, op))
                    if not probs:
                        continue
                    prob, a_k = self._choose_action(probs)
                    s_p.append((state, a_k, prob))
                    state = state.apply(a_k)

                if self._is_improvement(s_p, s_iter):
                    s_iter = s_p

            if self._is_improvement(s_iter, s_best):
                s_best = s_iter

            plan = cut_plan(s_best, self.goals)
            if plan[-1][0].apply(plan[-1][1]).is_goal(self.goals):
                break

            self._update_pheromones(s_best, s_iter)

        return cut_plan(s_best, self.goals)


def cut_plan(plan, goals):
    solution = []
    for state, action, prob in plan:
        solution.append((state, action, prob))
        if prob > 1.0 - 1e-5 and state.apply(action).is_goal(goals):
            break
    return solution
