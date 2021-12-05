import pprint
from typing import Tuple

from . import path_to_input

printer = pprint.PrettyPrinter(indent=4)


class SeaFloor:
    def __init__(self):
        self.floor_grid = [[0 for _ in range(1000)] for _ in range(1000)]

    def print(self):
        printer.pprint(self.floor_grid)

    def add_vent(self, point_a: Tuple[int, int], point_b: Tuple[int, int], ignore_diag=True):
        if ignore_diag and point_a[0] != point_b[0] and point_a[1] != point_b[1]:
            return
        current_point = point_a
        while current_point != point_b:
            self.floor_grid[current_point[0]][current_point[1]] += 1
            if current_point[0] != point_b[0]:
                current_point[0] += 1 if current_point[0] < point_b[0] else -1
            if current_point[1] != point_b[1]:
                current_point[1] += 1 if current_point[1] < point_b[1] else -1
        self.floor_grid[current_point[0]][current_point[1]] += 1

    def get_num_overlaps(self):
        return sum([1
                    for row in self.floor_grid
                    for num in row if num > 1])


def part_one():
    path = path_to_input('5.txt')
    with open(path) as input_file:
        sea_floor = SeaFloor()
        for line in input_file:
            # convert lines into arrays of Tuple[int, int]
            points = line.strip().split(' -> ')
            points = [[int(x) for x in point_str.split(',')] for point_str in points]
            point_a, point_b = points
            sea_floor.add_vent(point_a, point_b)
        return sea_floor.get_num_overlaps()


def part_two():
    path = path_to_input('5.txt')
    with open(path) as input_file:
        sea_floor = SeaFloor()
        for line in input_file:
            # convert lines into arrays of Tuple[int, int]
            points = line.strip().split(' -> ')
            points = [[int(x) for x in point_str.split(',')] for point_str in points]
            point_a, point_b = points
            sea_floor.add_vent(point_a, point_b, ignore_diag=False)
        return sea_floor.get_num_overlaps()
