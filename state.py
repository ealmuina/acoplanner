class State:
    def __init__(self, predicates):
        self.predicates = predicates

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return self.predicates == other.predicates

    def __hash__(self):
        return hash(self.predicates)

    def apply(self, operator, relaxed=False):
        # Check negative preconditions
        if self.predicates & operator.precondition_neg:
            return None

        # Check positive preconditions
        if not operator.precondition_pos.issubset(self.predicates):
            return None

        result = set(self.predicates)

        if not relaxed:
            # Remove negative effects
            result -= operator.effect_neg

        # Add positive effects
        result |= operator.effect_pos

        return State(frozenset(result))

    def applicable_actions(self, operators):
        for op in operators:
            # Check negative preconditions
            if self.predicates & op.precondition_neg:
                continue

            # Check positive preconditions
            if not op.precondition_pos.issubset(self.predicates):
                continue

            yield op

    def is_goal(self, goals):
        return goals.issubset(self.predicates)


class Plan:
    def __init__(self):
        self.states = []
        self.actions = []
        self.t_min = None
        self.h_min = None
