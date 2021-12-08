import sys
import random


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
    print(', '.join(map(str, args)), file=sys.stderr)


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

    debug(parsed)

    return parsed



PROJECT_COUNT = parse_input_line()[0]
PROJECTS = [parse_input_line(MOLECULES) for i in range(PROJECT_COUNT)]


def get_action(**d):
    my_samples = sorted(
        _filter(lambda i: i['carried_by'] == 0, d['samples']),
        key = lambda i: -1*i['rank']
    )

    for i in my_samples:
        i['cost_a'] = i['cost_a'] - me['expertise_a']
        i['cost_b'] = i['cost_b'] - me['expertise_b']
        i['cost_c'] = i['cost_c'] - me['expertise_c']
        i['cost_d'] = i['cost_d'] - me['expertise_d']
        i['cost_e'] = i['cost_e'] - me['expertise_e']

    undiagnosed = _filter(lambda i: i['health'] == -1, my_samples)
    diagnosed = _filter(lambda i: i['health'] != -1, my_samples)
    empties = [k for k, v in d['available'].items() if v == 0]

    done = []
    for sample in diagnosed:
        if all([me['storage_'+i] >= sample['cost_'+i] for i in MOLECULES]):
            done.append(sample)

    if d['me']['eta'] > 0:
        return ""

    if d['me']['target'] == 'SAMPLES':
        if len(my_samples) < MAX_SAMPLE:
            expertise = sum([d['me']['expertise_'+i] for i in MOLECULES])
            if len(empties) > 0:
                rank = 2
            elif expertise < 3:
                rank = random.randrange(1,3)
            elif expertise < 6:
                rank = random.randrange(1,4)
            elif expertise < 9:
                rank = random.randrange(2,4)
            else:
                rank = 3

            return "connect {}".format(rank)
        else:
            return "GOTO DIAGNOSIS"

    if d['me']['target'] == 'DIAGNOSIS':
        if len(undiagnosed) > 0:
            return "connect {}".format(undiagnosed[0]['id'])

        if len(empties) > 0:
            for empty in empties:
                for sample in diagnosed:
                    if sample["cost_"+empty] - me['storage_'+empty] > 0:
                        debug('empty', empty, 'cost', sample["cost_"+empty], 'storage', me['storage_'+empty])
                        return 'CONNECT {}'.format(sample['id'])

        if len(my_samples) < MAX_SAMPLE:
            return 'GOTO SAMPLES'

        return "GOTO MOLECULES"

    if d['me']['target'] == 'MOLECULES':
        if len(my_samples) == 0:
            return 'GOTO SAMPLES'

        for sample in diagnosed:
            if sum([sample['cost_'+i]-me['storage_'+i] for i in MOLECULES if sample['cost_'+i]>me['storage_'+i]]) + sum([me['storage_'+i] for i in MOLECULES]) > MAX_MOLECULES:
                continue

            needed = [i for i in MOLECULES if me['storage_'+i] < sample['cost_'+i]]

            if d['available'][needed[-1]] != 0:
                return "CONNECT {}".format(needed[-1])

        if any([all([me['storage_'+i] >= sample['cost_'+i] for i in MOLECULES]) for sample in diagnosed]):
            return 'GOTO LABORATORY'

        if len(my_samples) < MAX_SAMPLE:
            return "GOTO SAMPLES"

        return 'GOTO DIAGNOSIS'

    if d['me']['target'] == 'LABORATORY':
        if len(done) > 0:
            return "CONNECT {}".format(done[-1]['id'])
        if len(diagnosed) > 0:
            return 'GOTO MOLECULES'
        if len(undiagnosed) > 0:
            return 'GOTO DIAGNOSIS'

        return 'GOTO SAMPLES'

    if d['me']['target'] == 'START_POS':
        return "GOTO SAMPLES"


while True:
    me = parse_input_line(USER_DATA)
    enemy = parse_input_line(USER_DATA)
    available = parse_input_line(MOLECULES)
    sample_count = parse_input_line()[0]
    samples = [parse_input_line(SAMPLE_DATA) for i in range(sample_count)]

    action = get_action(me=me, enemy=enemy, available=available, samples=samples)
    print(action)
