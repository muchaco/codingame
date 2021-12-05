import sys


def debug(*args):
    print(', '.join(map(str, args)), file=sys.stderr)


def parse_input_line(keywords=None):
    _isdigit = lambda i: str(i).isdigit() if str(i)[0] != '-' else str(i)[1:].isdigit()

    raw_line = input()
    splitted_line = raw_line.split()

    if keywords is None:
        parsed = list()
        keywords = [i for i in range(len(splitted_line))]
        parsed = [None for _ in keywords]
    else:
        parsed = dict()
        if len(splitted_line) != len(keywords):
            raise Exception('wrong keywords')

    for kw in keywords:
        _next = splitted_line.pop(0)
        if _isdigit(_next):
            _next = int(_next)

        parsed[kw] = _next

    debug(parsed)

    return parsed
