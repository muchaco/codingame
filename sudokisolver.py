import sys
from collections import OrderedDict
from itertools import chain
from copy import deepcopy

ALL = {1, 2, 3, 4, 5, 6, 7, 8, 9}


class FillException(Exception):
    pass


def debug(*d):
    print(d, file=sys.stderr, flush=True)


def main():
    matrix = parse_input()
    available = get_availability_matrix(matrix)
    matrix, _ = fill(matrix, available)

    print(printer(matrix))

    return 0


def parse_input():
    matrix = []
    for i in range(9):
        matrix.append([int(i) for i in input()])

    return matrix


def get_availability_matrix(matrix):
    available = dict()
    for i, row in enumerate(matrix):
        for j, num in enumerate(row):
            if num != 0:
                continue
            row = get_row_values(matrix, i, j).difference({0})
            column = get_column_values(matrix, i, j).difference({0})
            square = get_square_values(matrix, i, j).difference({0})
            _all = row.union(column).union(square)
            available[(i, j)] = ALL.difference(_all)

    return OrderedDict(sorted(available.items(), key=lambda i: len(i[1])))


def get_column_indexes(_i, _):
    return (
        (_i, j)
        for j in range(9)
    )


def get_column_values(matrix, _i, _j):
    return set(matrix[i][j] for i, j in get_column_indexes(_i, _j))


def get_row_indexes(_, _j):
    return (
        (i, _j)
        for i in range(9)
    )


def get_row_values(matrix, _i, _j):
    return set(matrix[i][j] for i, j in get_row_indexes(_i, _j))


def get_square_indexes(_i, _j):
    return (
        (i, j)
        for i in range(_i-_i % 3, 3+_i-_i % 3)
        for j in range(_j-_j % 3, 3+_j-_j % 3)
    )


def get_square_values(matrix, _i, _j):
    return set(matrix[i][j] for i, j in get_square_indexes(_i, _j))


def fill(_matrix, _available):
    matrix = deepcopy(_matrix)
    available = deepcopy(_available)

    while len(available) > 0:
        first = next(iter(available))

        if len(available[first]) == 0:
            raise FillException()

        if len(available[first]) == 1:
            matrix, available = update(matrix, available, first)

        else:
            for num_candidate in available[first]:
                matrix_candidate, available_candidate = update(
                    matrix, available, first, num_candidate)
                try:
                    matrix_candidate, available_candidate = fill(
                        matrix_candidate, available_candidate)
                except FillException:
                    continue
                else:
                    matrix = matrix_candidate
                    available = available_candidate
                    break
            else:
                raise FillException()

    return matrix, available


def update(_matrix: list, _available: OrderedDict, _ij: tuple, num=None) -> tuple:
    matrix = deepcopy(_matrix)
    available = deepcopy(_available)

    ij = available.pop(_ij)
    if num is None:
        num = ij.pop()

    matrix[_ij[0]][_ij[1]] = num

    column = get_column_indexes(*_ij)
    row = get_row_indexes(*_ij)
    square = get_square_indexes(*_ij)

    for i, j in chain(column, row, square):
        try:
            available[(i, j)].remove(num)
        except KeyError:
            continue

    available = OrderedDict(sorted(available.items(), key=lambda i: len(i[1])))

    return matrix, available


def printer(matrix):
    out = ''
    for i in matrix:
        for j in i:
            out += str(j)
        out += '\n'
    return out.strip()


if __name__ == '__main__':
    sys.exit(main())
