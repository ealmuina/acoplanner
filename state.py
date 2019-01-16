class State:
    def __init__(self, predicates):
        self.predicates = predicates

    def apply(self, operator):
        # Check negative preconditions
        if self.predicates & operator.precondition_neg:
            return None

        # Check positive preconditions
        if not operator.precondition_pos.issubset(self.predicates):
            return None

        result = State(self.predicates)

        # Remove negative effects
        result.predicates -= operator.effect_neg

        # Add positive effects
        result.predicates |= operator.effect_pos

        return result
