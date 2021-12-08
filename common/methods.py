import sys
import inspect


def debug(*args):
    line_number = inspect.getframeinfo(inspect.currentframe().f_back).lineno
    print(line_number, ', '.join(map(str, args)), file=sys.stderr)


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
