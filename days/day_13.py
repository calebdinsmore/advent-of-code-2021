from typing import List
from operator import add
from itertools import chain

from . import path_to_input, path_to_output


def build_paper(input_lines: List[str]):
    coords = []
    instructions = []
    for line in input_lines:
        line = line.strip()
        if not line:
            continue
        if ',' in line:
            coords.append(tuple([int(digit) for digit in line.split(',')]))
        else:
            instructions.append(tuple(line[11:].split('=')))
    max_x = max([coord[0] for coord in coords])
    max_y = max([coord[1] for coord in coords])
    grid = [[0 for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for x, y in coords:
        grid[y][x] = 1
    return grid, instructions


def fold_up(fold_line: int, grid: List[List[int]]):
    half_1 = grid[0:fold_line]
    half_2 = grid[fold_line + 1:]
    half_2.reverse()
    offset = abs(len(half_1) - len(half_2))
    larger_half = half_1 if len(half_1) >= len(half_2) else half_2
    smaller_half = half_1 if larger_half is half_2 else half_2
    for y in range(offset, len(larger_half)):
        larger_half[y] = list(map(add, larger_half[y], smaller_half[y]))
    return larger_half


def fold_left(fold_line: int, grid: List[List[int]]):
    half_1 = [row[0: fold_line] for row in grid]
    half_2 = [row[fold_line + 1:] for row in grid]
    for row in half_2:
        row.reverse()
    offset = abs(len(half_1[0]) - len(half_2[0]))
    larger_half = half_1 if len(half_1[0]) >= len(half_2[0]) else half_2
    smaller_half = half_1 if larger_half is half_2 else half_2
    for y in range(len(larger_half)):
        larger_half[y] = larger_half[y][0:offset] + list(map(add, larger_half[y][offset:], smaller_half[y]))
    return larger_half


def print_grid(grid: List[List[int]]):
    pretty_grid = ''
    for row in grid:
        line = ''
        for element in row:
            if element:
                line += '#'
            else:
                line += '.'
        line += '\n'
        pretty_grid += line
    return pretty_grid


def part_one():
    path = path_to_input('13.txt')
    with open(path) as input_file:
        grid, instructions = build_paper(input_file.readlines())
        if instructions[0][0] == 'x':
            grid = fold_left(int(instructions[0][1]), grid)
        else:
            grid = fold_up(int(instructions[0][1]), grid)
        total_places = len(grid) * len(grid[0])
        blank_places = len(list(filter(lambda x: x == 0, chain.from_iterable(grid))))
        return total_places - blank_places


def part_two():
    path = path_to_input('13.txt')
    with open(path) as input_file:
        grid, instructions = build_paper(input_file.readlines())
        for plane, fold_line in instructions:
            if plane == 'x':
                grid = fold_left(int(fold_line), grid)
            else:
                grid = fold_up(int(fold_line), grid)
        with open(path_to_output('13.txt'), 'w') as output_file:
            output_file.write(print_grid(grid))
