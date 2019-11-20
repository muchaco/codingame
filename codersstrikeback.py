import sys
import math
import pprint


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

    def rotate(self, center, angle):
        angle = angle*math.pi/180
        x = (self._x-center._x)*math.cos(angle) - (self._y-center._y)*math.sin(angle) + center._x
        y = (self._x-center._x)*math.sin(angle) + (self._y-center._y)*math.cos(angle) + center._y
        return C(x, y)

    def unit_vector(self):
        return C(self._x, self._y)/self.dist(C(0,0))

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


class Pod(object):
    radius = 400

    def __init__(self):
        self.coordinates = None
        self.last_coordinates = None

    def set_coordinates(self, coordinates):
        self.last_coordinates = self.coordinates
        self.coordinates = coordinates

    def get_actual_speed_vector(self):
        if self.last_coordinates is not None:
            return self.coordinates-self.last_coordinates
        else:
            return C(0,0)

    def get_next_coordinates(self, destination, thrust):
        speed = self.get_actual_speed_vector()
        return self.coordinates+speed

    def coords_in_pod(self, coords):
        return self.coordinates.dist(coords) <= 400

    def pod_dist(self, other):
        return (self.coordinates-other.coordinates).abs() - 800

    def cp_dist(self, coords):
        return (self.coordinates-coords).abs() - 1000


def get_input_data():
    inputs_1 = [int(i) for i in input().split()]
    inputs_2 = [int(i) for i in input().split()]

    data = {'self': C(inputs_1[0], inputs_1[1]),
            'cp': C(inputs_1[2], inputs_1[3]),
            'opponent': C(inputs_2[0], inputs_2[1]),
            'dist': inputs_1[4],
            'angle': inputs_1[5]}

    return data


def count_output(data, self_pod, opponent_pod):
    speed = self_pod.get_actual_speed_vector()

    print_debug(speed_vector=speed,
                speed=speed.abs())
    # x, y = rotate_coords(data['x'], data['y'], x, y, -1*data['angle'])
    destination = data['cp']

    if -20 < data['angle'] < 20:
        if data['dist'] > 6000:
            thrust = 'BOOST'

    thrust = 0 if abs(data['angle']) > 100 else 100-abs(data['angle'])

    return destination, thrust


def print_debug(**d):
    print(pprint.pformat(d), file=sys.stderr)


self_pod = Pod()
opponent_pod = Pod()

while True:
    data = get_input_data()

    self_pod.set_coordinates(data['self'])
    opponent_pod.set_coordinates(data['opponent'])

    print_debug(angle=data['angle'])
    destination, thrust = count_output(data, self_pod, opponent_pod)
    print_debug(next=self_pod.get_next_coordinates(destination, thrust))

    print("{} {} {}".format(destination.x, destination.y, thrust))
