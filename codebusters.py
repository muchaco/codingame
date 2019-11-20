import sys
import math
import pprint
from random import randint


MAP_HEIGHT = 9000
MAP_WIDTH = 16000
MAX_DISTANCE = 20000

GHOST_MAX_RANGE = 1760
GHOST_MIN_RANGE = 900

RELEASE_RANGE = 1600

FOG_DIST = 2200

BUSTER_COUNT = int(input())  # the amount of busters you control
GHOST_COUNT = int(input())  # the amount of ghosts on the map
TEAM_ID = int(input())  # if this is 0, your base is on the top left of the map, if it is one, on the bottom right

DESTINATION = {0: (0,0),
               1: (MAP_WIDTH, MAP_HEIGHT)}


class C(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def y(self):
        return int(self._y)

    @property
    def x(self):
        return int(self._x)

    def __str__(self):
        return '<' + str(self.x) + ',' + str(self.y) + '>'

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x

    def __repr__(self):
        return "C(%d, %d)" % (self.x, self.y)

    def dist(self, other):
        return (other-self).abs()

    def __add__(self, other):
        return C(self._x+other._x, self._y+other._y)

    def __sub__(self, other):
        return C(self._x-other._x, self._y-other._y)

    def abs(self):
        return math.sqrt(self._x**2+self._y**2)

    def __mul__(self, const):
        return C(self._x*const, self._y*const)

    def __truediv__(self, const):
        return C(self._x/const, self._y/const)

    # special methods

    def is_close_to_wall(self):
        if FOG_DIST < self._x < MAP_WIDTH-FOG_DIST and \
            FOG_DIST < self._y < MAP_HEIGHT-FOG_DIST:
            return False

        return True

    @staticmethod
    def random(max_x, max_y):
        return C(randint(0, max_x),
                 randint(0, max_y))


def random_coord(reference):
    while True:
        coords = C.random(MAP_WIDTH, MAP_HEIGHT)
        if coords.dist(reference) > FOG_DIST*2 and coords.is_close_to_wall():
            return coords


class Entity(object):
    instances = []

    def __init__(self, _id, x, y, _type, state, value):
        entity = self.__class__.get(_id)
        if entity is None:
            super(Entity, self).__init__(_id, x, y, _type, state, value)
            self.__class__.instances.append(self)
            self.initialize()
        else:
            entity.update(_id, x, y, _type, state, value)

    def __init__(self, _id, x, y, _type, state, value):
        self.update(_id, x, y, _type, state, value)

    def update(self, _id, x, y, _type, state, value):
        self._id = _id
        self.coords = C(x, y)
        self.type = _type
        self.state = state
        self.value = value

    def initialize(self):
        raise NotImplementedError

    def dist(self, entity):
        if isinstance(entity, C):
            return self.coords.dist(entity)
        else:
            return self.coords.dist(entity.coords)

    @classmethod
    def get(cls, _id):
        for entity in __class__.instances:
            if entity.id == _id:
                return entity
        else:
            return None

    @property
    def id(self):
        return self._id


class Buster(Entity):
    def initialize(self):
        self.next_coords = None
        self.next_action = None
        self.to_be_busted = None
        self.random = None

    def update(self, _id, x, y, _type, state, value):
        super(Buster, self).update(_id, x, y, _type, state, value)
        ghost = self.carried_ghost()
        if ghost is not None:
            ghost.set_busted()

    def is_enemy(self):
        return self.type != TEAM_ID

    def is_carrying(self):
        return self.state == 1

    def carried_ghost(self):
        if self.is_carrying():
            return Ghost.get(self.value)
        else:
            return None

    def set_next_action(self, action):
        self.next_action = action

    def set_random(self):
        self.random = random_coord(self.coords)
        self.set_next_coords(self.random)

    def get_random(self):
        random = self.random
        self.random = None
        return random

    def set_next_coords(self, coords):
        self.set_next_action('MOVE')
        self.next_coords = coords

    def set_to_be_busted(self, ghost_id):
        self.set_next_action('BUST')
        self.to_be_busted = ghost_id

    def get_next_action(self):
        if self.next_action == 'MOVE':
            return ' '.join([self.next_action, str(self.next_coords.x, self.next_coords.y)])
        if self.next_action == 'BUST':
            busting = self.to_be_busted
            self.to_be_busted = None
            return ' '.join([self.next_action, str(busting)])
        return 'RELEASE'

    @classmethod
    def my_busters(cls):
        return sorted([b for b in cls.instances if not b.is_enemy()], key=lambda i: i.id)

    # @classmethod
    # def enemy_busters(cls):
    #     return sorted([b for b in cls.instances if b.is_enemy()], key=lambda i: i.id)


class Ghost(Entity):
    def initialize(self):
        self.busted = False

    def update(self, _id, x, y, _type, state, value):
        super(Ghost, self).update(_id, x, y, _type, state, value)
        self.initialize()

    # @property
    # def trapping_busters(self):
    #     return self.value

    def set_busted(self):
        self.busted = True

    def is_free(self):
        return not self.busted

    @classmethod
    def get_free_ghosts(cls):
        return [ghost for ghost in cls.instances if ghost.is_free() and not ghost.is_targeted()]

    def is_targeted(self):
        for b in Buster.my_busters():
            if self.id == b.to_be_busted:
                return True
        else:
            return False

    def closest_buster(self):
        _id = -1
        dist = MAX_DISTANCE

        for b in Buster.my_busters():
            d = self.dist(b)
            if d < dist:
                dist = d
                _id = b.id

        if _id == -1:
            return None

        return Buster.get(_id)

    @classmethod
    def closest_ghost(cls, buster):
        _id = -1
        dist = MAX_DISTANCE

        for ghost in cls.get_free_ghosts():
            d = buster.dist(ghost)
            if d < dist:
                dist = d
                _id = ghost.id

        if _id == -1:
            return None

        return cls.get(_id)


def print_debug(**d):
    print(pprint.pformat(d), file=sys.stderr)


def entity_initializer(*args):
    entity_type = Ghost if args[3] < 0 else Buster
    entity_type(*args)


while True:
    num_of_entities = int(input())  # the number of busters and ghosts visible to you
    for i in range(num_of_entities):
        entity_initializer([int(j) for j in input().split()])

    for buster in Buster.my_busters():
        random = buster.get_random()
        closest_ghost = Ghost.closest_ghost(buster)

        if buster.carried_ghost() is not None and buster.dist(C(*DESTINATION[TEAM_ID])) < RELEASE_RANGE:
            buster.set_next_action('RELEASE')
        elif buster.carried_ghost() is not None:
            buster.set_next_coords(C(*DESTINATION[TEAM_ID]))
        elif closest_ghost is not None: # and closest_ghost.closest_buster() == buster.id:
            print_debug(closest_ghost=closest_ghost.id, my_id=buster.id, closest_buster=closest_ghost.closest_buster().id)
            if GHOST_MIN_RANGE < closest_ghost.dist(buster) < GHOST_MAX_RANGE:
                buster.set_to_be_busted(closest_ghost.id)
            else:
                buster.set_next_coords(closest_ghost.coords)
        else:
            if random is None:
                buster.set_random()
            else:
                if buster.dist(buster.next_coords) < FOG_DIST:
                    buster.set_random()
                else:
                    buster.random = buster.next_coords
                    buster.set_next_coords(buster.next_coords)

        print(buster.get_next_action())
