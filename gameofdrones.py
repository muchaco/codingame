import sys
import math
import inspect

def debug(*args):
    line_number = inspect.getframeinfo(inspect.currentframe().f_back).lineno
    print(line_number, ', '.join(map(str, args)), file=sys.stderr)


def parse_input_line(keywords=None):
    _isdigit = lambda i: i.isdigit() if i[0] != '-' else i[1:].isdigit()

    raw_line = input()
    splitted_line = raw_line.split()

    if keywords is None:
        parsed = list()
        keywords = [i for i, _ in enumerate(splitted_line)]
        parsed = [None for _ in splitted_line]
    else:
        parsed = dict()
        if len(splitted_line) != len(keywords):
            raise Exception('Wrong keywords were given')

    for kw in keywords:
        _next = splitted_line.pop(0)
        if _isdigit(_next):
            _next = int(_next)

        parsed[kw] = _next

    return parsed

def main():
    base = parse_input_line(['number_of_players', 'player_id', 'number_of_drones', 'number_of_zones'])
    assert 2 <= base['number_of_players'] <= 4
    assert 0 <= base['player_id'] <= base['number_of_players']-1
    assert 3 <= base['number_of_drones'] <= 11
    assert 4 <= base['number_of_zones'] <= 8
    zones = []


    for _ in range(base['number_of_zones']):
        zones.append(parse_input_line(['x', 'y']))  # x: corresponds to the position of the center of a zone. A zone is a circle with a radius of 100 units.
        assert 0 <= zones[-1]['x'] <= 4000
        assert 0 <= zones[-1]['y'] <= 1800

    # game loop
    while True:
        zone_controls = []
        for _ in range(base['number_of_zones']):
            zone_controls.append(parse_input_line()[0])
            assert -1 <= zone_controls[-1] <= base['number_of_players']-1

        drones = dict()
        for i in range(base['number_of_players']):
            drones[i] = list()
            for _ in range(base['number_of_drones']):
                drones[i].append(parse_input_line(['x', 'y']))
                assert 0 <= drones[i][-1]['x'] <= 4000
                assert 0 <= drones[i][-1]['y'] <= 1800

        drone_tree = build_tree(base, zones, drones)
        actions = get_all_action(base['player_id'], drone_tree, zone_controls)

        for i in actions:
            print('{x} {y}'.format(**zones[i]))


def build_tree(_base, _zones, _drones):
    tree = [
        [
            [
                distance(zone, _drones[j][k])
                for k in range(_base['number_of_drones'])
            ]
            for j in range(_base['number_of_players'])
        ]
        for zone in _zones
    ]
    return tree

def get_all_action(_id, _tree, _controls):
    actions = [None for _ in _tree[0][_id]]

    reserving_zone = [
        len([d for d in _tree[i][_controls[i]] if d <= 100])
        for i in range(len(_tree))
    ]
    debug(reserving_zone)

    for i in range(len(reserving_zone)):
        easy, min_reserving = _min(reserving_zone, i+1)
        tmp = [d if actions[i] is None else 100000 for i, d in enumerate(_tree[easy][_id])]
        ids = get_id_of_mins(tmp, min_reserving+1)
        for i in ids:
            assert actions[i] is None
            actions[i] = easy

    while None in actions:
        none_index = actions.index(None)
        i, _ = _min([i[_id][none_index] for i in _tree], 1)
        actions[none_index] = i

    debug(actions)

    assert all((i is not None for i in actions))
    return actions

def _min(l, n):
    assert len(l) >= n
    assert n > 0
    t = l.copy()
    for _ in range(n-1):
        t[t.index(min(t))] = max(t)+1
    return t.index(min(t)), min(t)

def get_id_of_mins(l, n):
    assert n > 0
    assert len(l) > n

    if len(l) - l.count(100000) < n:
        return []

    return [_min(l, i+1)[0] for i in range(n)]

def distance(a, b):
    assert 'x' in a.keys()
    assert 'x' in b.keys()
    assert isinstance(a['x'], int)
    assert isinstance(b['x'], int)

    d = {'x': a['x']-b['x'],
         'y': a['y']-b['y']}

    return math.sqrt(d['x']**2+d['y']**2)


if __name__ == "__main__":
    main()