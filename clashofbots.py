import sys
import itertools


def debug(*args):
    print(', '.join(map(str, args)), file=sys.stderr)


def count(lmbd, lst):
    return len(list(filter(lmbd, lst)))


def transform_data(m, lmbd=None):
    if lmbd == None:
        def lmbd(i): return i
    return list(map(lmbd, itertools.chain(*m)))


def decision_tree(m):
    def enemy(i): return i < 0
    def ally(i): return i > 0

    commands = ['attack up',
                'attack right',
                'attack left',
                'attack down',
                'move up',
                'move right',
                'move left',
                'move down',
                'guard']

    if all([m[7] > 0, m[11] > 0, m[13] > 0, m[17] > 0]):
        return "guard"
    if m[12] + 2 * count(ally, [m[6], m[7], m[8], m[11], m[13], m[16], m[17], m[18]]) < 2 * count(enemy, [m[6], m[7], m[8], m[11], m[13], m[16], m[17], m[18]]):
        return 'selfdestruction'
    if m[14] > 0 and m[13] < 0:
        return 'attack right'
    if m[10] > 0 and m[11] < 0:
        return 'attack left'
    if m[9] > 0 and m[8] < 0 and m[7] != 0 and m[14] == 0 and m[18] == 0 and m[13] == 0:
        return "move right"
    if m[5] > 0 and m[6] < 0 and m[7] != 0 and m[10] == 0 and m[16] == 0 and m[11] == 0:
        return "move left"
    if m[8] < 0 and m[7] > 0 and m[14] == 0 and m[13] == 0 and m[18] == 0:
        return "move right"
    if m[6] < 0 and m[7] > 0 and m[10] == 0 and m[16] == 0 and m[11] == 0:
        return "move left"

    if m[7] != 0:
        commands.remove('move up')
    if m[13] != 0:
        commands.remove('move right')
    if m[11] != 0:
        commands.remove('move left')
    if m[17] != 0:
        commands.remove('move down')
    if m[7] >= 0:
        commands.remove('attack up')
    if m[13] >= 0:
        commands.remove('attack right')
    if m[11] >= 0:
        commands.remove('attack left')
    if m[17] >= 0:
        commands.remove('attack down')

    return commands[0]


# game loop
while True:
    number_of_robots = int(input())
    minimaps = []
    for i in range(number_of_robots):
        minimap = []
        for j in range(5):
            minimap.append(list(map(int, input().split())))
        minimaps.append(minimap)

    for minimap in minimaps:
        transformed = transform_data(minimap)
        result = decision_tree(transformed)
        print(result)
