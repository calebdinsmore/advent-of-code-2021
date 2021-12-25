from . import path_to_input


DELIMITER_MAP = {'(': ')', '[': ']', '{': '}', '<': '>'}


def part_one():
    delimiter_score = {')': 3, ']': 57, '}': 1197, '>': 25137}
    path = path_to_input('10.txt')
    with open(path) as input_file:
        score = 0
        for line in input_file:
            delim_stack = []
            for char in line.strip():
                if char in DELIMITER_MAP:
                    delim_stack.append(char)
                else:
                    opening_delim = delim_stack.pop()
                    if DELIMITER_MAP[opening_delim] != char:
                        score += delimiter_score[char]
        return score


def part_two():
    delimiter_score = {')': 1, ']': 2, '}': 3, '>': 4}
    path = path_to_input('10.txt')
    with open(path) as input_file:
        scores = []
        for line in input_file:
            delim_stack = []
            score = 0
            has_error = False
            for char in line.strip():
                if char in DELIMITER_MAP:
                    delim_stack.append(char)
                else:
                    opening_delim = delim_stack.pop()
                    if DELIMITER_MAP[opening_delim] != char:
                        has_error = True
            if not has_error and delim_stack:
                # if there isn't a syntax error, and the stack has items
                delim_stack.reverse()
                for delim in delim_stack:
                    score *= 5
                    score += delimiter_score[DELIMITER_MAP[delim]]
                scores.append(score)
        scores.sort()
        return scores[len(scores) // 2]
