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
