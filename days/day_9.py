from functools import reduce
from typing import Tuple, Dict, List

from . import path_to_input


def get_adjacent(height_map, row, col):
    adjacent = []
    if row - 1 >= 0:
        adjacent.append(height_map[row - 1][col])
    if row + 1 < len(height_map):
        adjacent.append(height_map[row + 1][col])
    if col - 1 >= 0:
        adjacent.append(height_map[row][col - 1])
    if col + 1 < len(height_map[row]):
        adjacent.append(height_map[row][col + 1])
    return adjacent


def part_one():
    path = path_to_input('9.txt')
    with open(path) as input_file:
        height_map = []
        for line in input_file:
            height_map.append([int(num) for num in line.strip()])
        low_points = []
        for row in range(len(height_map)):
            for col in range(len(height_map[row])):
                adjacent = get_adjacent(height_map, row, col)
                if height_map[row][col] < min(adjacent):
                    low_points.append(height_map[row][col])
        return sum([1 + point for point in low_points])


"""
Day 9 Part 2: Recursive Boogaloo
"""


def traverse_basin(height_map: List[List[int]],
                   point: Tuple[int, int],
                   visited: Dict[Tuple[int, int], bool]):
    """ Recursively walk through the basin """
    row, col = point
    current = height_map[row][col]
    basin_size = 1
    # go up
    if row - 1 != -1:
        up_point = (row - 1, col)
        up = height_map[up_point[0]][up_point[1]]
        if up_point not in visited and up != 9 and up > current:
            visited[up_point] = True
            basin_size += traverse_basin(height_map, up_point, visited)
    # go left
    if col - 1 != -1:
        left_point = (row, col - 1)
        left = height_map[left_point[0]][left_point[1]]
        if left_point not in visited and left != 9 and left > current:
            visited[left_point] = True
            basin_size += traverse_basin(height_map, left_point, visited)
    # go down
    if row + 1 != len(height_map):
        down_point = (row + 1, col)
        down = height_map[down_point[0]][down_point[1]]
        if down_point not in visited and down != 9 and down > current:
            visited[down_point] = True
            basin_size += traverse_basin(height_map, down_point, visited)
    # go right
    if col + 1 != len(height_map[row]):
        right_point = (row, col + 1)
        right = height_map[right_point[0]][right_point[1]]
        if right_point not in visited and right != 9 and right > current:
            visited[right_point] = True
            basin_size += traverse_basin(height_map, right_point, visited)
    return basin_size


def part_two():
    path = path_to_input('9.txt')
    with open(path) as input_file:
        height_map = []
        for line in input_file:
            height_map.append([int(num) for num in line.strip()])
        basin_sizes = []
        for row in range(len(height_map)):
            for col in range(len(height_map[row])):
                adjacent = get_adjacent(height_map, row, col)
                if height_map[row][col] < min(adjacent):
                    basin_sizes.append(traverse_basin(height_map, (row, col), {}))
        basin_sizes.sort(reverse=True)
        return reduce(lambda x, y: x * y, basin_sizes[:3])

