# from functools import cache
import random


PRECISION = 10
MAX_WIDTH = 10
MAX_DEPTH = 10


class MaxDapthReached(Exception):
    pass


def append(t, i):
    assert isinstance(t, tuple)
    return t + (i,)


def main():
    next_player = None
    previous_moves = {
        1: tuple(),   # player1 <- we are
        -1: tuple()   # player2
    }

    state = get_init_state()
    next_player = 1

    while True:
        last_move = get_last_move()
        if last_move is not None:
            next_player = -1
            previous_moves[next_player] = append(previous_moves[next_player], last_move)
            state, next_player = move(state, next_player, last_move)

        best_move = get_optimal_move(state, previous_moves)
        state, next_player = move(state, next_player, best_move)
        previous_moves[next_player] = append(previous_moves[next_player], best_move)

        print(best_move)


def get_init_state():
    raise NotImplementedError()


def get_last_move():
    raise NotImplementedError()


def move(_state, _next_player, _move):
    state = _state.copy()
    next_player = -1 * _next_player

    raise NotImplementedError()

    return state, next_player


def get_optimal_move(_state, _previous_moves):
    possible_moves = get_possible_moves(_state, _previous_moves, player=1)
    assert len(possible_moves) != 0

    if len(possible_moves) == 1:
        return possible_moves[0]

    optimal_value = None
    optimal_move = None

    for move in possible_moves:
        if is_optimal_move(_state, move, player=1):
            return move

        candidate = evaluate_move(
            _state,
            move,
            _previous_moves
        )

        if optimal_move is None or game_comparer(candidate, optimal_value):
            optimal_value = candidate
            optimal_move = move

    return optimal_move


def get_possible_moves(_state, _previous_moves, _player):
    possible_moves = []

    raise NotImplementedError()

    if len(possible_moves) > MAX_WIDTH:
        return random.sample(possible_moves, MAX_WIDTH)

    return possible_moves


def is_optimal_move(_state, _move, _player):
    raise NotImplementedError()


def evaluate_move(_state, _move, _previous_moves):
    next_state = move(_state, 1, _move)  # my move
    best_value = None

    for _ in range(PRECISION):
        try:
            game_value = random_game_simulation(
                _state,
                -1,  # enemy's turn
                _previous_moves
            )
        except MaxDapthReached:
            continue

        if best_value is None or game_comparer(game_value, best_value):
            best_value = game_value

    return best_value


def game_comparer(g1, g2):
    return g1 < g2


def random_game_simulation(_state, _player, _previous_moves, _iteration=0):
    if _iteration >= MAX_DEPTH:
        raise MaxDapthReached()

    possible_moves = get_possible_moves(_state, _previous_moves, _player)

    if len(possible_moves) == 0:
        if _player == 1:
            return 1
        else:
            return 0

    if _player == 1:
        for possible_move in possible_moves:
            if is_optimal_move(_state, possible_move, _player):
                return 1

    random_move = random.choice(possible_moves)
    random_state = move(_state, _player, random_move)
    previous_moves = _previous_moves.copy()
    previous_moves[_player] = append(previous_moves[_player], random_move)

    simulation = random_game_simulation(
        random_state,
        -1 * _player,
        previous_moves,
        _iteration + 1
    )

    if _player == 1:
        return simulation + 1
    else:
        return simulation


if __name__ == "__main__":
    main()
