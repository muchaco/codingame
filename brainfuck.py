def parse_input():
    l, s, n = [int(i) for i in input().split()]
    bf_code = []
    bf_input = []

    for i in range(l):
        bf_code.append(input())
    for i in range(n):
        bf_input.append(int(input()))

    return s, bf_code, bf_input


def bf_interpreter(S, bf_code, _bf_input):
    code_line = ''.join(bf_code)
    bf_input = _bf_input.copy()
    array = [0 for _ in range(S)]
    pointer = 0
    output = ''
    deep = 0
    i = 0

    while i < len(code_line):
        code_char = code_line[i]

        if code_char == '>':
            pointer += 1
            if pointer > S-1:
                return 'POINTER OUT OF BOUNDS'
        elif code_char == '<':
            pointer -= 1
            if pointer < 0:
                return 'POINTER OUT OF BOUNDS'
        elif code_char == '+':
            array[pointer] += 1
            if array[pointer] > 255:
                return 'INCORRECT VALUE'
        elif code_char == '-':
            array[pointer] -= 1
            if array[pointer] < 0:
                return 'INCORRECT VALUE'
        elif code_char == '.':
            output += chr(array[pointer])
        elif code_char == ',':
            array[pointer] = bf_input.pop(0)
        elif code_char == '[':
            if array[pointer] == 0:
                in_deep = 0
                while i < len(code_line):
                    if code_line[i] == '[':
                        in_deep += 1
                    if code_line[i] == ']':
                        in_deep -= 1
                    if in_deep == 0:
                        break
                    i += 1
                else:
                    return 'SYNTAX ERROR'
            else:
                deep += 1

        elif code_char == ']':
            if array[pointer] != 0:
                in_deep = 0
                while i >= 0:
                    if code_line[i] == ']':
                        in_deep += 1
                    if code_line[i] == '[':
                        in_deep -= 1
                    if in_deep == 0:
                        break
                    i -= 1
                else:
                    return 'SYNTAX ERROR'
            else:
                deep -= 1

        i += 1

    if deep != 0:
        return 'SYNTAX ERROR'

    return output


if __name__ == '__main__':
    S, bf_code, bf_input = parse_input()
    result = bf_interpreter(S, bf_code, bf_input)

    print(result)
