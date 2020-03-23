import sys
import math
import pprint

from collections import defaultdict
from itertools import starmap, combinations


class Map(object):
    def __init__(self, edges=None):
        self._graph = {}

    def add_edge(self, edge):
        n1 = edge.pop()
        n2 = edge.pop()

        if n1 not in self._graph:
            self._graph[n1] = list()
        if n2 not in self._graph:
            self._graph[n2] = list()

        self._graph[n1].append(n2)
        self._graph[n2].append(n1)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def print_debug(*args, **kwargs):
    if len(args) != 0:
        kwargs['__log__'] = args
    print(pprint.pformat(kwargs), file=sys.stderr)


def debug(fn):
    def decorated_func(*args, **kwargs):
        _args = list(args)

        for arg in _args:
            if hasattr(arg, '__dict__'):
                _args.remove(arg)
        parameters = {}

        if len(_args) != 0:
            parameters['positional_args'] = _args

        if len(kwargs) != 0:
            parameters['named_args'] = kwargs

        print_debug(method=fn.__name__, **parameters)

        return fn(*args, **kwargs)
    return decorated_func


DISCOVERY_PHASE = 0
BUILDING_PHASE = 1
FIGHT_PHASE = 2


class Game(object, metaclass=Singleton):
    def __init__(self):
        game_params = [int(j) for j in input().split()]
        self.player_count = game_params[0]
        self.my_id = game_params[1]
        self.zone_count = game_params[2]
        self.link_count = game_params[3]
        self.my_platinum = 0
        self.action = ''
        self.loop = 0
        self.phase = FIGHT_PHASE
        self.map = Map()

        for i in range(self.zone_count):
            zone_id, platinum_source = [int(j) for j in input().split()]
        for i in range(self.link_count):
            zone_1, zone_2 = [int(j) for j in input().split()]
            self.map.add_edge([zone_1, zone_2])


    def start_loop(self):
        while True:
            self.__parse_data()
            self.__calculate_action()
            self.__action()

            self.loop += 1

    def __parse_data(self):
        self.my_platinum = int(input())  # your available Platinum
        for i in range(self.zone_count):
            z_id, owner_id, pods_p0, pods_p1, visible, platinum = [int(j) for j in input().split()]
            Tile(z_id, owner_id, pods_p0, pods_p1, visible, platinum)

        if self.loop == 0:
            Tile.set_base(owner=0, id=Tile.filter(owner=0)[0].id)
            Tile.set_base(owner=1, id=Tile.filter(owner=1)[0].id)

    def check_discovery_finished(self):
        pass # return Tile.seen()

    def bolyongas(self):
        pass

    def __calculate_action(self):
        if self.phase == DISCOVERY_PHASE:
            self.bolyongas()
            self.check_discovery_finished()

        elif self.phase == BUILDING_PHASE:
            platinum = lambda x: x.platinum

            tiles_with_platinum = Tile.filter(owner=-1, platinum=1)
            if len(tiles_with_platinum) == 0:
                self.bolyongas()
            else:
                _sorted = sorted(tiles_with_platinum, key=platinum)
                _sorted = _sorted[::-1]
            self.check_building_finished()

        elif self.phase == FIGHT_PHASE:
            my_base_id = Tile.base_of(self.my_id).id
            enemy_base_id = Tile.base_of(1-self.my_id).id

            print_debug(self.map.depth_first_search(my_base_id, enemy_base_id))

            #self.mozgositas()

    def __action(self):
        #print(self.action.strip())
        print('WAIT')
        print('WAIT')
        self.action = ''

    def move(self, count, _from, to):
        key = 'pods_p' + self.my_id
        param = {key: count}
        Tile.filter(owner=Game().my_id,
                    id=_from,
                    **param)
        self.action += '{} {} {} '.format(count, _from, to)


class Pod(object):
    pass


class Tile(object):
    instances = []

    def __init__(self, _id, owner, pods_p0, pods_p1, visible, platinum):
        tile = self.__class__.get(_id)
        if tile is None:
            self.set(_id, owner, pods_p0, pods_p1, visible, platinum)
            self.base=None
            self.platinum=platinum
            self.__class__.instances.append(self)
        else:
            tile.set(_id, owner, pods_p0, pods_p1, visible, platinum)

    def set(self, _id, owner, pods_p0, pods_p1, visible, platinum):
        self.id = _id
        self.owner = owner
        self.pods_p0 = pods_p0
        self.pods_p1 = pods_p1
        self.visible = visible
        if bool(visible):
            self.platinum = platinum

    @classmethod
    def set_base(cls, id, owner):
        cls.get(id).base = owner

    @classmethod
    def get(cls, id):
        try:
            return cls.filter(id=id)[0]
        except IndexError:
            return None

    @classmethod
    def base_of(cls, id):
        return cls.filter(base=id)[0]

    @classmethod
    @debug
    def filter(cls, id=None, owner=None, pods_p0=None, pods_p1=None,
               visible=None, platinum=None, base=None):
        filtered = []
        for tile in cls.instances:
            if id is not None:
                if id != tile.id:
                    continue
            if owner is not None:
                if owner != tile.owner:
                    continue
            if pods_p0 is not None:
                if pods_p0 > tile.pods_p0:
                    continue
            if pods_p1 is not None:
                if pods_p1 > tile.pods_p1:
                    continue
            if visible is not None:
                if visible != tile.visible:
                    continue
            if platinum is not None:
                if platinum > tile.platinum:
                    continue
            if base is not None:
                if base != tile.base:
                    continue

            filtered.append(tile)

        return filtered

if __name__ == '__main__':
    game = Game()
    game.start_loop()
