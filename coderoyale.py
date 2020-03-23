import sys
import math
import pprint


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

HEIGHT = 1000
WIDTH = 1920
QUEEN_RADIUS = 30
MAX_HP = 100
MAX_ROUNDS = 250

QUEEN = -1
KNIGHT = 0
ARCHER = 1

NEUTRAL = -1
FRIENDLY = 0
ENEMY = 1

BARRACK = 2
TOWER = 1

STRIDE = 60


PRICE = {KNIGHT: 80, ARCHER: 100}


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
        return str(self.x) + ' ' + str(self.y)

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


class Site:
    sites = []

    def __init__(self, id, coords, radius):
        self.id = int(id)
        self.coords = coords
        self.radius = int(radius)
        self.type = None
        self.owner = None
        self.param1 = None
        self.param2 = None

        print_debug(sites_len=len(self.__class__.sites))
        self.__class__.sites.append(self)

    def update(self, _, __, type, owner, param1, param2):
        self.type = int(type)
        self.owner = int(owner)
        self.param1 = int(param1)
        self.param2 = int(param2)


    @classmethod
    def get(cls, id):
        return cls.filter(id=id)[0]

    def is_structured(self):
        return self.type == -1

    def is_barrack(self):
        return self.type == 2

    def is_friendly(self):
        return self.owner == FRIENDLY

    def is_enemy(self):
        return self.owner == ENEMY

    def get_rounds_until_training(self):
        if self.is_barrack():
            return self.param1
        else:
            return None

    def get_creep_type(self):
        if self.is_barrack():
            return self.param2
        else:
            return None

    @classmethod
    def filter(cls, id=None, owner=None, type=None, creep=None, rounds=None):
        filtered = []
        for site in cls.sites:
            if id is not None:
                if id != site.id:
                    continue
            if owner is not None:
                if owner != site.owner:
                    continue
            if type is not None:
                if type != site.type:
                    continue
            if creep is not None:
                if creep != site.get_creep_type():
                    continue
            if rounds is not None:
                if rounds < site.get_rounds_until_training():
                    continue

            filtered.append(site)
        return filtered

    @classmethod
    def get_closest_to(cls, coords, **kwargs):
        closest_id = None
        closest_dist = None

        for site in cls.filter(**kwargs):
            dist = coords.dist(site.coords) - site.radius
            if closest_id is None or dist < closest_dist:
                closest_id = site.id
                closest_dist = dist

        return Site.get(closest_id)

    # @classmethod
    # def get_farest_to(cls, coords, **kwargs):
    #     farest_id = None
    #     farest_dist = None
    #
    #     for site in cls.filter(**kwargs):
    #         dist = coords.dist(site.coords) - site.radius
    #         if farest_id is None or dist > farest_dist:
    #             farest_id = site.id
    #             farest_dist = dist
    #
    #     return Site.get(farest_id)

    def dist(self, other):
        if isinstance(other, C):
            return self.coords.dist(other)
        elif isinstance(other, Unit) or isinstance(other, Site):
            return self.coords.dist(other.coords)
        else:
            raise Exception('wrong type: ' +str(type(other)))


class Unit:
    units = []

    def __init__(self, coords, owner, type, health):
        self.coords = coords
        self.owner = owner
        self.type = type
        self.health = health
        print_debug(units_len=len(self.__class__.units))
        self.__class__.units.append(self)

    def is_queen(self):
        return self.type == QUEEN

    def is_knight(self):
        return self.type == KNIGHT

    def is_archer(self):
        return self.type == ARCHER

    def is_friendly(self):
        return self.owner == FRIENDLY

    def is_enemy(self):
        return self.owner == ENEMY

    @classmethod
    def my_queen(cls):
        return cls.filter(owner=FRIENDLY, type=QUEEN)[0]

    @classmethod
    def filter(cls, owner=None, type=None, health=None):
        filtered = []
        for unit in cls.units:
            if owner is not None:
                if owner != unit.owner:
                    continue
            if type is not None:
                if type != unit.type:
                    continue
            if health is not None:
                if health > unit.health:
                    continue
            filtered.append(unit)
        return filtered

    def dist(self, other):
        if isinstance(other, C):
            return self.coords.dist(other)
        elif isinstance(other, Unit) or isinstance(other, Site):
            return self.coords.dist(other.coords)
        else:
            raise Exception('wrong type: ' + str(type(other)))

    @classmethod
    def clear(cls):
        cls.units = []


def print_debug(**d):
    print(pprint.pformat(d), file=sys.stderr)


def init_sites(num_sites):
    num_sites = int(num_sites)
    for i in range(num_sites):
        site_id, x, y, radius = parse_input_line()
        Site(site_id, C(x, y), radius)


def game_loop(num_sites):
    round = 0

    while True:
        round += 1
        gold, touched_site = parse_input_line()
        for i in range(num_sites):
            site_id, ignore_1, ignore_2, structure_type, owner, param_1, param_2 = parse_input_line()
            Site.get(site_id).update(ignore_1, ignore_2, structure_type, owner, param_1, param_2)

        num_units = parse_input_line()
        for i in range(num_units):
            x, y, owner, unit_type, health = parse_input_line()
            Unit(C(x, y), owner, unit_type, health)

        action(gold, touched_site)
        Unit.clear()


def action(gold, touched_site):
    if touched_site != -1 and len(Site.filter(id=touched_site,
                                              owner=NEUTRAL)) == 1:
        # archers = len(Site.filter(owner=FRIENDLY,
        #                           creep=ARCHER,
        #                           type=BARRACK))
        knights = len(Site.filter(owner=FRIENDLY,
                                  creep=KNIGHT,
                                  type=BARRACK))
        towers =  len(Site.filter(owner=FRIENDLY,
                                  type=TOWER))
        if knights > towers:
            barrack_type = 'TOWER'
        else:
            barrack_type = 'BARRACKS-KNIGHT'

        if Unit.my_queen().health < 50:
            tower = Site.get_closest_to(Unit.my_queen(), owner=FRIENDLY, type=TOWER)
            print('MOVE ' + str(tower.coords))
        else:
            print(' '.join(['BUILD', str(touched_site), barrack_type]))
    else:
        my_queen = Unit.my_queen()
        closest_site = Site.get_closest_to(my_queen.coords,
                                           owner=NEUTRAL)
        if Unit.my_queen().health < 50:
            tower = Site.get_closest_to(Unit.my_queen(), owner=FRIENDLY, type=TOWER)
            if tower is not None:
                print('MOVE ' + str(tower.coords))
            else:
                print('MOVE ' + str(closest_site.coords))
        else:
            print('MOVE ' + str(closest_site.coords))

    # archers = len(Unit.filter(owner=FRIENDLY,
    #                           type=ARCHER))
    knights = len(Unit.filter(owner=FRIENDLY,
                              type=KNIGHT))

    wanted = KNIGHT

    if len(Site.filter(owner=FRIENDLY,
                       type=BARRACK,
                       rounds=0)) == 1:
        wanted = Site.filter(owner=FRIENDLY,
                             type=BARRACK,
                             rounds=0)[0].get_creep_type()

    site = None

    # if gold > 100:
        # if wanted == ARCHER:
        #     site = Site.get_closest_to(Unit.my_queen(),
        #                                owner=FRIENDLY,
        #                                type=BARRACK,
        #                                rounds=0,
        #                                creep=ARCHER)
    if gold > 80:
        if wanted == KNIGHT:
            site = Site.get_closest_to(Unit.filter(owner=ENEMY,
                                                   type=QUEEN)[0],
                                       owner=FRIENDLY,
                                       type=BARRACK,
                                       rounds=0,
                                       creep=KNIGHT)

    sites = [] if site is None else [str(site.id)]
    print(" ".join(["TRAIN"] + sites))


def count_price(sites):
    cost = 0
    for site in sites:
        if site.get_creep_type() == KNIGHT:
            cost += PRICE[KNIGHT]
        elif site.get_creep_type() == ARCHER:
            cost += PRICE[ARCHER]

    return cost


def parse_input_line():
    try:
        _input = input()
    except Exception as e:
        print_debug(exception=str(e))
    else:
        print_debug(input=_input)
        splitted = _input.split()
        if len(splitted) > 1:
            return (int(i) for i in splitted)
        else:
            return int(splitted[0])


if __name__ == '__main__':
    num_sites = parse_input_line()
    init_sites(num_sites)
    game_loop(num_sites)
