import sys
import math
import pprint
from random import randint


MAP_HEIGHT = 9000
MAP_WIDTH = 16000

GHOST_MAX_RANGE = 1760
GHOST_MIN_RANGE = 900

RELEASE_RANGE = 1600

FOG_DIST = 2200

BUSTER_COUNT = int(input())  # the amount of busters you control
GHOST_COUNT = int(input())  # the amount of ghosts on the map
TEAM_ID = int(input())  # if this is 0, your base is on the top left of the map, if it is one, on the bottom right

class C(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get(self):
        return (self.x, self.y)

    def direction(self, p):
        x, y = p.x, p.y
        return C(x-self.x, y-self.y)

    def transpose(self):
        return C(MAP_WIDTH - self.x, MAP_HEIGHT - self.y)

    def distance(self, p):
        p0 = self.direction(p)
        return p0.abs()

    def abs(self):
        return math.sqrt(self.x**2+self.y**2)

    def mul(self, i):
        return C(self.x*i, self.y*i)

    @staticmethod
    def average(list_of_coords):
        x, y = 0, 0
        for coord in list_of_coords:
            x += coord.x
            y += coord.y

        return C(int(x/len(list_of_coords)), int(y/len(list_of_coords)))

    def is_close_to_wall(self):
        if FOG_DIST < self.x < MAP_WIDTH-FOG_DIST and \
            FOG_DIST < self.y < MAP_HEIGHT-FOG_DIST:
            return False

        return True


def random_coord(coord):
    while True:
        c = C(randint(0, MAP_WIDTH),randint(0, MAP_HEIGHT))
        #print_debug(old_c = coord.get(), new_c = c.get())
        if c.distance(coord) > FOG_DIST*2 and c.is_close_to_wall():
            return c


DESTINATION = {0: C(0,0),
               1: C(MAP_WIDTH, MAP_HEIGHT)}


class Entity(object):
    def __init__(self, _id, x, y, _type, state, value):
        self.update(_id, x, y, _type, state, value)

    def update(self, _id, x, y, _type, state, value):
        self.id = _id
        self.coords = C(x, y)
        self.type = _type
        self.state = state
        self.value = value

    def distance(self, entity):
        return self.coords.distance(entity.coords)

    def get_id(self):
        return self.id


class Buster(Entity):
    instances = []

    def __init__(self, _id, x, y, _type, state, value):
        buster = self.__class__.get_seen_one(_id)
        if buster is None:
            super(Buster, self).__init__(_id, x, y, _type, state, value)
            self.__class__.instances.append(self)
            self.next_coords = None
            self.next_action = None
            self.to_be_busted = None
            self.random = None
        else:
            buster.update(_id, x, y, _type, state, value)

    def update(self, _id, x, y, _type, state, value):
        super(Buster, self).update(_id, x, y, _type, state, value)
        if self.is_carrying():
            ghost = Ghost.get_seen_one(self.carried_ghost_id())
            if ghost is not None:
                ghost.set_busted()

    @classmethod
    def get_seen_one(cls, _id):
        for buster in __class__.instances:
            if buster.get_id() == _id:
                return buster
        else:
            return None

    def is_enemy(self):
        return self.type != TEAM_ID

    def is_carrying(self):
        return self.state == 1

    def carried_ghost_id(self):
        if self.is_carrying():
            return self.value
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
            return ' '.join([self.next_action, *[str(c) for c in self.next_coords.get()]])
        if self.next_action == 'BUST':
            busting = self.to_be_busted
            self.to_be_busted = None
            return ' '.join([self.next_action, str(busting)])
        return 'RELEASE'

    @classmethod
    def my_sorted_busters(cls):
        return sorted([b for b in cls.instances if not b.is_enemy()], key=lambda i: i.id)

    @classmethod
    def enemy_sorted_busters(cls):
        return sorted([b for b in cls.instances if b.is_enemy()], key=lambda i: i.id)


class Ghost(Entity):
    instances = []

    def __init__(self, _id, x, y, _type, state, value):
        ghost = self.__class__.get_seen_one(_id)
        if ghost is None:
            super(Ghost, self).__init__(_id, x, y, _type, state, value)
            self.__class__.instances.append(self)
            self.busted = False
        else:
            ghost.update(_id, x, y, _type, state, value)
            ghost.busted=False

    @classmethod
    def get_seen_one(cls, _id):
        for ghost in __class__.instances:
            if ghost.get_id() == _id:
                return ghost
        else:
            return None

    def trapping_busters(self):
        return self.value

    def set_busted(self):
        self.busted = True

    def is_busted(self):
        return self.busted

    def is_free(self):
        return not self.busted

    @classmethod
    def get_free_ghosts(cls):
        return [ghost for ghost in cls.instances if ghost.is_free() and not ghost.is_targeted()]

    def is_targeted(self):
        for b in Buster.my_sorted_busters():
            if self.id == b.to_be_busted:
                return True
        else:
            return False

    def closest_buster(self):
        _id = -1
        dist = 10000000000

        for b in Buster.my_sorted_busters():
            d = self.coords.distance(b.coords)
            if d < dist:
                dist = d
                _id = b.id

        if _id == -1:
            return None

        return Buster.get_seen_one(_id)

    @classmethod
    def closest_ghost(cls, c):
        _id = -1
        dist = 10000000000

        for ghost in cls.get_free_ghosts():
            d = ghost.coords.distance(c)
            if d < dist:
                dist = d
                _id = ghost.id

        if _id == -1:
            return None

        return cls.get_seen_one(_id)


def print_debug(**d):
    print(pprint.pformat(d), file=sys.stderr)


while True:
    entities = int(input())  # the number of busters and ghosts visible to you
    ghosts = []
    busters = []

    for i in range(entities):
        entity_id, x, y, entity_type, state, value = [int(j) for j in input().split()]

        if entity_type < 0:
            ghosts.append(Ghost(entity_id, x, y, entity_type, state, value))
        else:
            busters.append(Buster(entity_id, x, y, entity_type, state, value))

    #print_debug(busters=[buster.id for buster in Buster.my_sorted_busters()])

    for buster in Buster.my_sorted_busters():

        random = buster.get_random()
        closest_ghost = Ghost.closest_ghost(buster.coords)

        if buster.carried_ghost_id() is not None and DESTINATION[TEAM_ID].distance(buster.coords) < RELEASE_RANGE:
            buster.set_next_action('RELEASE')
        elif buster.carried_ghost_id() is not None:
            buster.set_next_coords(DESTINATION[TEAM_ID])
        elif closest_ghost is not None: # and closest_ghost.closest_buster() == buster.id:
            print_debug(closest_ghost=closest_ghost.id, my_id=buster.id, closest_buster=closest_ghost.closest_buster().id)
            ghost = Ghost.closest_ghost(buster.coords)
            if GHOST_MIN_RANGE < ghost.coords.distance(buster.coords) < GHOST_MAX_RANGE:
                buster.set_to_be_busted(ghost.id)
            else:
                buster.set_next_coords(ghost.coords)
        else:
            if random is None:
                #print_debug(random=True)
                buster.set_random()
            else:
                if buster.next_coords.distance(buster.coords) < FOG_DIST:
                    buster.set_random()
                else:
                    buster.random = buster.next_coords
                    buster.set_next_coords(buster.next_coords)

        print(buster.get_next_action())
