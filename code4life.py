import sys
import math
import pprint

# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!


USER_DATA = ['target', 'eta', 'score',
             'storage_a', 'storage_b', 'storage_c', 'storage_d', 'storage_e',
             'expertise_a', 'expertise_b', 'expertise_c', 'expertise_d', 'expertise_e']
MOLECULES = ['a', 'b', 'c', 'd', 'e']
SAMPLE_DATA = ['id', 'carried_by', 'rank', 'expertise_gain', 'health',
               'cost_a', 'cost_b', 'cost_c', 'cost_d', 'cost_e']
MAX_SAMPLE = 3
MAX_MOLECULES = 10


def print_debug(*args, **kwargs):
    if len(args) != 0:
        kwargs['__log__'] = args
    print(pprint.pformat(kwargs), file=sys.stderr)


def parse_input_line(keywords=None):
    if keywords is not None:
        _return = dict()

        try:
            _input = input()
        except Exception as e:
            print_debug(exception=str(e))
        else:
            splitted = _input.split()
            if len(splitted) != len(keywords):
                raise Exception('wrong parameters')

            for i in range(len(splitted)):
                try:
                    _return[keywords[i]] = int(splitted[i])
                except ValueError:
                    _return[keywords[i]] = splitted[i]

        return _return
    else:
        try:
            _input = input()
        except Exception as e:
            print_debug(exception=str(e))
        else:
            try:
                return int(_input)
            except:
                return _input


class Sample(object):
    instances = []
    ready = []

    def __init__(self, _id, _dict):
        sample = self.__class__.get(_id)
        if sample is None:
            self.__class__.instances.append(self)
            self.initialize(_id, _dict)
        else:
            sample.update(_dict)

    def __repr__(self):
        return 'samp_{}'.format(self.id)

    def initialize(self, _id, _dict):
        self.id = _id
        self.data = _dict

    def update(self, _dict):
        self.data = _dict

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return self.id

    @classmethod
    def get(cls, _id):
        for sample in __class__.instances:
            if sample.id == _id:
                return sample
        else:
            return None

    @classmethod
    def reset(cls):
        cls.instances = []

    @classmethod
    def sorted_samples(cls):
        return sorted([s for s in cls.instances if s['carried_by'] == -1], key=lambda j: j.value())[::-1]

    def value(self):
        return self['health']*1000/self.get_needed_count()

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        if key in dir(self):
            return getattr(self, key)
        else:
            return None

    @classmethod
    def get_my_samples(cls):
        return [s for s in cls.instances if s['carried_by'] == 0]

    def pop(self):
        self.__class__.instances.remove(self)

    def get_needed_count(self):
        needed = 0
        needed += self['cost_a'] - User.instances[0]['expertise_a']
        needed += self['cost_b'] - User.instances[0]['expertise_b']
        needed += self['cost_c'] - User.instances[0]['expertise_c']
        needed += self['cost_d'] - User.instances[0]['expertise_d']
        needed += self['cost_e'] - User.instances[0]['expertise_e']
        return needed

    def would_full(self):
        carriing = User.instances[0]['storage_a'] + \
                   User.instances[0]['storage_b'] + \
                   User.instances[0]['storage_c'] + \
                   User.instances[0]['storage_d'] + \
                   User.instances[0]['storage_e']
        return carriing + self.get_needed_count() > MAX_MOLECULES

    def all_expertise(self):
        return User.instances[0]['expertise_a'] + \
               User.instances[0]['expertise_b'] + \
               User.instances[0]['expertise_c'] + \
               User.instances[0]['expertise_d'] + \
               User.instances[0]['expertise_e']

class User(object):
    instances = []

    def __init__(self, _id, _dict):
        user = self.__class__.get(_id)
        if user is None:
            self.__class__.instances.append(self)
            self.initialize(_id, _dict)
        else:
            user.update(_dict)

    def initialize(self, _id, _dict):
        self.id = _id
        self.data = _dict

    def update(self, _dict):
        self.data = _dict

    @classmethod
    def get(cls, _id):
        for user in __class__.instances:
            if user.id == _id:
                return user
        else:
            return None

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        if key in dir(self):
            return getattr(self, key)
        else:
            return None

    @classmethod
    def get_my_robot(cls):
        return cls.instances[0]


dist = {
    'START_POS':
        {'SAMPLES': 2,
         'DIAGNOSIS': 2,
         'MOLECULES': 2,
         'LABORATORY': 2},
    'SAMPLES':
        {'SAMPLES': 0,
         'DIAGNOSIS': 3,
         'MOLECULES': 3,
         'LABORATORY': 3},
    'DIAGNOSIS':
        {'SAMPLES': 3,
         'DIAGNOSIS': 0,
         'MOLECULES': 3,
         'LABORATORY': 4},
    'MOLECULES':
        {'SAMPLES': 3,
         'DIAGNOSIS': 3,
         'MOLECULES': 0,
         'LABORATORY': 3},
    'LABORATORY':
        {'SAMPLES': 3,
         'DIAGNOSIS': 4,
         'MOLECULES': 3,
         'LABORATORY': 0},
}
queue = []

def go_to(destination):
    global queue
    place = User.get_my_robot()['target']
    print('GOTO {}'.format(destination))
    for i in range(1, dist[place][destination]):
        queue.append('WAIT')


def samples_analyzed():
    samples = Sample.get_my_samples()
    for i in samples:
        if i['health'] == -1:
            return False
    else:
        return True


project_count = int(input())
for i in range(project_count):
    a, b, c, d, e = [int(j) for j in input().split()]



# game loop
while True:
    for i in range(2):
        User(i, parse_input_line(USER_DATA))

    available_molecules = parse_input_line(MOLECULES)

    sample_count = parse_input_line()
    for i in range(sample_count):
        sample_data = parse_input_line(SAMPLE_DATA)
        Sample(sample_data['id'], sample_data)

    my_robot = User.get_my_robot()

    if len(queue) > 0:
        command = queue.pop(0)
        print(command)
        continue

    if my_robot['target'] == 'START_POS':
        go_to('SAMPLES')
    elif my_robot['target'] == 'SAMPLES':
        if len(Sample.get_my_samples()) == 0:
            print('CONNECT 3')
        elif len(Sample.get_my_samples()) == 1:
            print('CONNECT 2')
        elif len(Sample.get_my_samples()) == 2:
            print('CONNECT 1')
        else:
            go_to('DIAGNOSIS')
    elif my_robot['target'] == 'DIAGNOSIS':
        if samples_analyzed():
            go_to('MOLECULES')
        else:
            my_samples = Sample.get_my_samples()
            for s in my_samples:
                if s['health'] == -1:
                    print('CONNECT {}'.format(s['id']))
                    break
    elif my_robot['target'] == 'MOLECULES':
        print_debug(ready = Sample.ready)
        my_samples = Sample.get_my_samples()
        print_debug(my_samples)
        for s in set(my_samples) - set(Sample.ready):
            print_debug(s.data)
            if s.would_full():
                print_debug('would full')
                continue
            else:
                for m in MOLECULES:
                    needed = s['cost_{}'.format(m)]
                    expertise = User.get_my_robot()['expertise_{}'.format(m)]
                    for k in range(needed-expertise):
                        queue.append('CONNECT {}'.format(m.upper()))

                command = queue.pop(0)
                print(command)
                Sample.ready.append(s)
                break
        else:
            go_to('LABORATORY')
    elif my_robot['target'] == 'LABORATORY':
        print_debug(ready = Sample.ready)
        my_samples = Sample.ready

        if len(Sample.ready) == 0:
            go_to('SAMPLES')
        else:
            sample = Sample.ready.pop()
            print('CONNECT {}'.format(sample['id']))
    print_debug(User.get_my_robot().data)
    Sample.reset()
