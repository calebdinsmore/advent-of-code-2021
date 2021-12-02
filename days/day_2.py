from . import path_to_input


def run_part_one():
    path = path_to_input('2.txt')
    with open(path) as input_file:
        h_pos, depth = 0, 0
        for line in input_file:
            direction, amount = line.split()
            amount = int(amount)
            if direction == 'forward':
                h_pos += amount
            elif direction == 'up':
                depth -= amount
            elif direction == 'down':
                depth += amount
        return h_pos * depth


def run_part_two():
    path = path_to_input('2.txt')
    with open(path) as input_file:
        h_pos, depth, aim = 0, 0, 0
        for line in input_file:
            direction, amount = line.split()
            amount = int(amount)
            if direction == 'forward':
                depth += aim * amount
                h_pos += amount
            elif direction == 'up':
                aim -= amount
            elif direction == 'down':
                aim += amount
        return h_pos * depth
