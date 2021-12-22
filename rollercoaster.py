from copy import deepcopy


def memoize(f):
    memory = {}

    def inner(places, times_per_day, _queue, earning):
        _key = tuple(_queue)
        if _key not in memory:
            retval = f(places, times_per_day, _queue, earning)
            memory[_key] = retval, retval[2]-earning
            return memory[_key][0]
        else:
            pv_times_per_day, pv_groups, pv_earning = memory[_key][0]
            times_difference = (pv_times_per_day+1)-times_per_day
            earning_difference = earning-(pv_earning-memory[_key][1])

            how_many_times = times_per_day//times_difference
            how_many_times = how_many_times-1 if how_many_times > 0 else how_many_times

            next_times_per_day = times_per_day - times_difference * how_many_times - 1
            next_earning = earning + earning_difference * \
                how_many_times + memory[_key][1]
            return next_times_per_day, pv_groups, next_earning

    return inner


def main():
    places, times_per_day, groups = parse_input()
    earnings = calculate_earnings(places, times_per_day, groups)
    print(earnings)


def parse_input() -> tuple[int, int, list[int]]:
    l, c, n = [int(i) for i in input().split()]
    groups = [int(input()) for _ in range(n)]

    return l, c, groups


def calculate_earnings(places: int, times_per_day: int, groups: list[int]):
    earning = 0
    while times_per_day > 0:
        times_per_day, groups, earning = looping(
            places, times_per_day, groups, earning)
    return earning


@memoize
def looping(places: int, times_per_day: int, _groups: list[int], earning):
    groups = deepcopy(_groups)
    next_groups = []
    next_sum = 0

    while len(groups) > 0:
        next_group = groups.pop(0)
        if next_sum + next_group <= places:
            next_groups.append(next_group)
            next_sum += next_group
        else:
            groups.insert(0, next_group)
            break

    groups.extend(next_groups)

    return times_per_day-1, groups, earning+next_sum


if __name__ == "__main__":
    main()
