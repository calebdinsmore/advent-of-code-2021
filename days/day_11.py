from typing import Tuple, List, Set

from . import path_to_input


def get_adjacent(octopuses, row, col) -> List[Tuple[int, int]]:
    adjacent = []
    if row - 1 >= 0:
        adjacent.append((row - 1, col))
        # add diagonals
        if col - 1 >= 0:
            adjacent.append((row - 1, col - 1))
        if col + 1 < len(octopuses[row]):
            adjacent.append((row - 1, col + 1))
    if row + 1 < len(octopuses):
        adjacent.append((row + 1, col))
        if col - 1 >= 0:
            adjacent.append((row + 1, col - 1))
        if col + 1 < len(octopuses[row]):
            adjacent.append((row + 1, col + 1))
    if col - 1 >= 0:
        adjacent.append((row, col - 1))
    if col + 1 < len(octopuses[row]):
        adjacent.append((row, col + 1))
    return adjacent


def process_step(octopuses: List[List[int]]):
    has_flashed: Set[Tuple[int, int]] = set()
    to_flash = []
    for row in range(len(octopuses)):
        for col in range(len(octopuses[row])):
            octopuses[row][col] += 1
            if octopuses[row][col] > 9:
                to_flash.append((row, col))
    while to_flash:
        flash = to_flash.pop()
        if flash in has_flashed:
            continue
        has_flashed.add(flash)
        f_row, f_col = flash
        adjacent_pts = get_adjacent(octopuses, f_row, f_col)
        for adj_row, adj_col in adjacent_pts:
            octopuses[adj_row][adj_col] += 1
            if (adj_row, adj_col) not in has_flashed and octopuses[adj_row][adj_col] > 9:
                to_flash.append((adj_row, adj_col))
    for f_row, f_col in has_flashed:
        octopuses[f_row][f_col] = 0
    return len(has_flashed)


def part_one():
    path = path_to_input('11.txt')
    octopuses = []
    with open(path) as input_file:
        for line in input_file:
            octopuses.append([int(octopus) for octopus in line.strip()])
    num_flashes = 0
    for _ in range(100):
        num_flashes += process_step(octopuses)
    return num_flashes


def part_two():
    path = path_to_input('11.txt')
    octopuses = []
    with open(path) as input_file:
        for line in input_file:
            octopuses.append([int(octopus) for octopus in line.strip()])
    num_octopuses = len(octopuses) * len(octopuses[0])
    step = 0
    while True:
        step += 1
        if process_step(octopuses) == num_octopuses:
            return step
