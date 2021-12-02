from . import path_to_input


def run_part_one():
    path = path_to_input('1.txt')
    with open(path) as input_file:
        last_reading = None
        num_increased = 0
        for line in input_file:
            reading = int(line.strip())
            if last_reading is not None and reading > last_reading:
                num_increased += 1
            last_reading = reading
        return num_increased


def run_part_two():
    path = path_to_input('1.txt')
    with open(path) as input_file:
        measurements = [int(line.strip()) for line in input_file]
        start, end = 0, 3
        last_reading = None
        num_increased = 0
        while end <= len(measurements):
            reading = sum(measurements[start:end])
            if last_reading is not None and reading > last_reading:
                num_increased += 1
            last_reading = reading
            start += 1
            end += 1
        return num_increased
