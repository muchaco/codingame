import sys
import random
import inspect


_filter = lambda f, l: list(filter(f, l))


USER_DATA = ['target', 'eta', 'score',
             'storage_a', 'storage_b', 'storage_c', 'storage_d', 'storage_e',
             'expertise_a', 'expertise_b', 'expertise_c', 'expertise_d', 'expertise_e']
MOLECULES = ['a', 'b', 'c', 'd', 'e']
SAMPLE_DATA = ['id', 'carried_by', 'rank', 'expertise_gain', 'health',
               'cost_a', 'cost_b', 'cost_c', 'cost_d', 'cost_e']
MAX_SAMPLE = 3
MAX_MOLECULES = 10


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

    # debug(parsed)

    return parsed


PROJECT_COUNT = parse_input_line()[0]
PROJECTS = [parse_input_line(MOLECULES) for i in range(PROJECT_COUNT)]


def get_action(**d):
    for s in d['samples']:
        for m in MOLECULES:
            s['cost_'+m] = s['cost_'+m] - d['me']['expertise_'+m] - d['me']['storage_'+m]

    my_samples = sorted(_filter(lambda s: s['carried_by'] == 0, d['samples']), key = lambda s: -1*s['rank'])
    cloud_samples = sorted(_filter(lambda s: s['carried_by'] == -1, d['samples']), key = lambda s: -1*s['rank'])
    undiagnosed = _filter(lambda s: s['health'] == -1, my_samples)
    diagnosed = _filter(lambda s: s['health'] != -1, my_samples)
    empties = [k for k, v in d['available'].items() if v == 0]
    amount_in_storage = sum([d['me']['storage_'+m] for m in MOLECULES])
    cloud_candidates = _filter(
        lambda s: sum([s['cost_'+m] for m in MOLECULES if s['cost_'+m]>0]) + amount_in_storage <= MAX_MOLECULES,
        _filter(lambda s: all([s['cost_'+m] <= d['available'][m] for m in MOLECULES]), cloud_samples)
    )
    collected = [s for s in diagnosed if all([s['cost_'+m] <= 0 for m in MOLECULES])]
    expertise = sum([d['me']['expertise_'+m] for m in MOLECULES])
    still_needed_amount = lambda s: sum([s['cost_'+m] for m in MOLECULES if s['cost_'+m] > 0])

    for s in my_samples:
        debug(s)
    debug(d['me'])

    if d['me']['eta'] > 0:
        return ""

    if d['me']['target'] == 'SAMPLES':
        if len(my_samples + cloud_candidates) < MAX_SAMPLE:
            ranked = lambda n: len(_filter(lambda s: s['rank'] == n, my_samples + cloud_candidates))

            if expertise < 4:
                if ranked(1) < 2:
                    rank = 1
                elif ranked(2) == 0:
                    rank = 2
            elif expertise < 6:
                if ranked(3) == 0:
                    rank = 3
                elif ranked(1) < 2:
                    rank = 1
            else:
                if ranked(1) < 1:
                    rank = 1
                elif ranked(3) < 2:
                    rank = 3

            return "connect {}".format(rank)
        else:
            return "GOTO DIAGNOSIS"

    if d['me']['target'] == 'DIAGNOSIS':
        if len(undiagnosed) > 0:
            debug('diagnosis needed')
            return "CONNECT {}".format(undiagnosed[0]['id'])

        for s in diagnosed:
            for m in MOLECULES:
                if s["cost_"+m] > d['available'][m] + 1:
                    debug('send to cloud (costs more than we have)')
                    return 'CONNECT {}'.format(s['id'])

            if still_needed_amount(s) + amount_in_storage > MAX_MOLECULES +2:
                debug('send to cloud (couldnt fit in my pocket)')
                return 'CONNECT {}'.format(s['id'])

        if len(my_samples) < MAX_SAMPLE:
            if len(cloud_candidates) > 0:
                debug('get sample from cloud')
                return "CONNECT {}".format(cloud_candidates[0]['id'])

            if len(my_samples) >= 2:
                debug('dont be maximalist, two is enough for me')
                return "GOTO MOLECULES"

            debug('needs another sample')
            return 'GOTO SAMPLES'

        debug('ready to get molecules')
        return "GOTO MOLECULES"

    if d['me']['target'] == 'MOLECULES':
        if len(my_samples) == 0:
            debug('I have no samples')
            return 'GOTO SAMPLES'

        for s in diagnosed:
            if still_needed_amount(s) + amount_in_storage > MAX_MOLECULES:
                debug("this sample couldnt fit in my storage")
                continue

            needed_molecules = [m for m in MOLECULES if s['cost_'+m] > 0]

            if len(needed_molecules) != 0 and d['available'][needed_molecules[-1]] != 0:
                debug('I need a molecule to move on')
                return "CONNECT {}".format(needed_molecules[-1])

        if len(collected) > 0:
            debug('I have my mollecules, need to progress')
            return 'GOTO LABORATORY'

        if len(my_samples) < MAX_SAMPLE:
            debug('I can have more samples here')
            return "GOTO SAMPLES"

        debug('I have no idea, lets go to diagnosis')
        return 'GOTO DIAGNOSIS'

    if d['me']['target'] == 'LABORATORY':
        if len(collected) > 0:
            return "CONNECT {}".format(collected[-1]['id'])

        if len(diagnosed) > 0:
            any_molecules_missing_for_samples = [any([s['cost_'+m] > d['available'][m] for m in MOLECULES]) for s in diagnosed]
            if all(any_molecules_missing_for_samples):
                debug('all my samples are bad')
                if len(my_samples) < MAX_SAMPLE:
                    debug('I need another samples')
                    return "GOTO SAMPLES"
                else:
                    return "GOTO DIAGNOSIS"

            for s in diagnosed:

                if still_needed_amount(s) + amount_in_storage < MAX_MOLECULES:
                    debug('I can still collect some molecule')
                    return 'GOTO MOLECULES'

        if len(undiagnosed) > 0:
            debug('I have something to diagnose')
            return 'GOTO DIAGNOSIS'

        if len(cloud_candidates) > 1:
            debug('I can fetch something from the cloud')
            return "GOTO DIAGNOSIS"

        return 'GOTO SAMPLES'

    if d['me']['target'] == 'START_POS':
        return "GOTO SAMPLES"


while True:
    me = parse_input_line(USER_DATA)
    enemy = parse_input_line(USER_DATA)
    available = parse_input_line(MOLECULES)
    sample_count = parse_input_line()[0]
    samples = [parse_input_line(SAMPLE_DATA) for _ in range(sample_count)]

    action = get_action(me=me, enemy=enemy, available=available, samples=samples)
    print(action)
