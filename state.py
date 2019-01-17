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

    def is_goal(self, goals):
        return goals.issubset(self.predicates)
