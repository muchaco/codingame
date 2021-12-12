import random
import itertools
import sys

# tuning
PRECISION = 10
MAX_WIDTH = 10
MAX_DEPTH = 10

# game consts
GRAPH = {
    'A1': ['A4', 'D1'],
    'A4': ['A1', 'A7', 'B4'],
    'A7': ['A4', 'D7'],
    'B2': ['B4', 'D2'],
    'B4': ['A4', 'B2', 'B6', 'C4'],
    'B6': ['B4', 'D6'],
    'C3': ['C4', 'D3'],
    'C4': ['B4', 'C3', 'C5'],
    'C5': ['C4', 'D5'],
    'D1': ['A1', 'D2', 'G1'],
    'D2': ['B2', 'D1', 'D3', 'F2'],
    'D3': ['C3', 'D2', 'E3'],
    'D5': ['C5', 'D6', 'E5'],
    'D6': ['B6', 'D5', 'D7', 'F6'],
    'D7': ['A7', 'D6', 'G7'],
    'E3': ['D3', 'E4'],
    'E4': ['E3', 'E5', 'F4'],
    'E5': ['D5', 'E4'],
    'F2': ['D2', 'F4'],
    'F4': ['E4', 'F2', 'F6', 'G4'],
    'F6': ['D6', 'F4'],
    'G1': ['D1', 'G4'],
    'G4': ['F4', 'G1', 'G7'],
    'G7': ['D7', 'G4']
}
ALPHABET = 'ABCDEFG'


def debug(*args):
    print(', '.join(map(str, args)), file=sys.stderr)


class MaxDapthReached(Exception):
    pass


def append(t, i):
    assert isinstance(t, tuple)
    return t + (i,)


def main():
    previous_moves = {
        1: tuple(),   # player1 <- we are
        -1: tuple()   # player2
    }

    player_id = int(input())
    unneeded_data = int(input())
    for _ in range(unneeded_data):
        input()

    while True:
        last_move = get_last_move()
        state = get_state(player_id)

        unneeded_data = int(input())
        for _ in range(unneeded_data):
            input()

        if last_move is not None:
            previous_moves[-1] = append(previous_moves[-1], last_move)

        best_move = get_optimal_move(state, previous_moves)
        state = move(state, 1, best_move)
        previous_moves[1] = append(previous_moves[1], best_move)

        print(best_move)


def get_state(_player):
    inverter = {
        str(_player): 1,
        str(1 - _player): -1,
        '2': 0
    }

    state = {
        -1: set(),
        0: set(),
        1: set()
    }

    nodes = input().split(';')
    for node in nodes:
        splitted = node.split(':')
        state[
            inverter[
                splitted[1]
            ]
        ].add(
            splitted[0]
        )

    return state


def get_last_move():
    last_move = input()
    if last_move == '-':
        return None

    return last_move


def move(_state, _next_player, _move):
    state = {k: v.copy() for k, v in _state.items()}

    movement = _move.split(';')

    if 'MOVE' in movement[0]:
        state[_next_player].add(movement[2])
        state[_next_player].remove(movement[1])
        state[0].add(movement[1])
        state[0].remove(movement[2])
    if 'PLACE' in movement[0]:
        state[_next_player].add(movement[1])
        state[0].remove(movement[1])
    if 'TAKE' in movement[0]:
        state[-1 * _next_player].remove(movement[-1])
        state[0].add(movement[-1])

    assert _state != state

    return state


def get_optimal_move(_state, _previous_moves):
    possible_moves = get_possible_moves(_state, _previous_moves, _player=1)
    assert len(possible_moves) != 0

    if len(possible_moves) == 1:
        return possible_moves[0]

    optimal_value = None
    optimal_move = None

    for move in possible_moves:
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

    if len(_state[0]) >= 23:
        for p1 in _state[0]:
            possible_moves.append('PLACE;{}'.format(p1))
    elif len(_previous_moves[_player]) == 0:
        for p in _state[-1 * _player]:
            for p1 in GRAPH[p]:
                possible_moves.append('PLACE;{}'.format(p1))
    elif len(_previous_moves[_player]) < 9:
        for p1 in _state[0]:
            if any((p2 not in _state[0] for p2 in GRAPH[p1])):  # adjacent to someone
                if in_mill(_state[_player], p1):
                    millless = not_in_mill(_state[-1 * _player])
                    if len(millless) > 0:
                        for p2 in millless:
                            possible_moves.append(
                                'PLACE&TAKE;{};{}'.format(p1, p2))
                    else:
                        for p2 in _state[-1 * _player]:
                            possible_moves.append(
                                'PLACE&TAKE;{};{}'.format(p1, p2))
                else:
                    possible_moves.append('PLACE;{}'.format(p1))
    else:
        for p1 in _state[_player]:
            if len(_state[_player]) == 3:  # flying
                g = _state[0]
            else:
                g = GRAPH[p1]

            for p2 in g:  # TODO flying
                if p2 not in _state[0]:
                    continue
                if in_mill(_state[_player] - {p1}, p2):
                    millless = not_in_mill(_state[-1 * _player])
                    if len(millless) > 0:
                        for p3 in millless:
                            possible_moves.append(
                                'MOVE&TAKE;{};{};{}'.format(p1, p2, p3))
                    else:
                        for p3 in _state[-1 * _player]:
                            possible_moves.append(
                                'MOVE&TAKE;{};{};{}'.format(p1, p2, p3))
                else:
                    possible_moves.append('MOVE;{};{}'.format(p1, p2))

    possible_moves = get_prefered_moves(_state, possible_moves, _player)

    return possible_moves


def not_in_mill(_player_placed):
    not_in_mill = []

    for p1 in _player_placed:
        for p2 in GRAPH[p1]:
            if p2 not in _player_placed:
                continue
            if third_in_mill(p1, p2) in _player_placed:
                break
        else:
            not_in_mill.append(p1)

    return not_in_mill


def in_mill(player_placed, place):
    for p in GRAPH[place]:
        if p in player_placed:
            if third_in_mill(place, p) in player_placed:
                return True
    return False


def third_in_mill(p1, p2):
    if len(GRAPH[p1]) > len(GRAPH[p2]):
        middle = p1
        edge = p2
    else:
        middle = p2
        edge = p1

    return ALPHABET[ALPHABET.index(middle[0]) + (ALPHABET.index(middle[0]) - ALPHABET.index(edge[0]))] + str(int(middle[1]) + (int(middle[1]) - int(edge[1])))


def get_prefered_moves(_state, _possible_moves, _player):
    possible_moves = _possible_moves.copy()
    if any((is_optimal_move(m) for m in possible_moves)):
        possible_moves = [m for m in possible_moves if is_optimal_move(m)]

    if len(possible_moves) > MAX_WIDTH:
        return random.sample(possible_moves, MAX_WIDTH)

    return possible_moves


def is_optimal_move(_move):
    if 'TAKE' in _move:
        return True

    return False


def evaluate_move(_state, _move, _previous_moves):
    previous_moves = _previous_moves.copy()
    previous_moves[1] = append(previous_moves[1], _move)
    next_state = move(_state, 1, _move)  # my move

    winners = {
        -1: 0,
        1: 0
    }

    while sum(winners.values()) != PRECISION:
        try:
            winner = random_game_simulation(
                next_state,
                -1,  # enemy's turn
                previous_moves
            )
        except MaxDapthReached:
            continue

        winners[winner] += 1

    return winners[1]/(winners[1]+winners[-1])


def game_comparer(g1, g2):
    return g1 > g2


def random_game_simulation(_state, _player, _previous_moves, _iteration=0):
    if _iteration >= MAX_DEPTH:
        raise MaxDapthReached()

    possible_moves = get_possible_moves(_state, _previous_moves, _player)

    for possible_move in possible_moves:
        if is_optimal_move(possible_move):
            return _player

    if len(possible_moves) == 0:
        return _player * -1

    random_move = random.choice(possible_moves)
    random_state = move(_state, _player, random_move)
    previous_moves = _previous_moves.copy()
    previous_moves[_player] = append(previous_moves[_player], random_move)

    winner = random_game_simulation(
        random_state,
        -1 * _player,
        previous_moves,
        _iteration + 1
    )

    return winner


if __name__ == "__main__":
    main()
