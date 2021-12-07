from typing import List, Dict
from collections import Counter
from . import path_to_input


EXAMPLE = '16,1,2,0,4,2,7,1,2,14'


def calculate_fuel_consumption(target: int, positions: Dict[int, int], p2=False):
    total = 0
    for position, num_crabs in positions.items():
        if p2:
            distance = abs(position - target)
            total += sum(range(1, distance + 1)) * num_crabs
        else:
            total += abs(position - target) * num_crabs
    return total


def binary_search(positions: Dict[int, int], p2=False):
    """
    Perform a binary search of the positions between the min crab and the max crab to find the optimal target
    :param positions: Dictionary of positions where key = position and value = number of crabs at that position
    :param p2: Is this part 2?
    :return: int representing the fuel consumption for the most optimal path
    """
    min_value = min(positions.keys())
    max_value = max(positions.keys())
    target = (max_value - min_value) // 2
    target_c = calculate_fuel_consumption(target, positions, p2)
    left_c = calculate_fuel_consumption(target - 1, positions, p2)
    right_c = calculate_fuel_consumption(target + 1, positions, p2)
    has_better_neighbor = right_c < target_c or left_c < target_c
    while has_better_neighbor:
        if left_c < target_c:
            max_value = target
            target = ((target - 1) - min_value) // 2
        elif right_c < target_c:
            min_value = target
            target = ((max_value - (target + 1)) // 2) + target
        target_c = calculate_fuel_consumption(target, positions, p2)
        left_c = calculate_fuel_consumption(target - 1, positions, p2)
        right_c = calculate_fuel_consumption(target + 1, positions, p2)
        has_better_neighbor = right_c < target_c or left_c < target_c
    return target_c


def part_one():
    path = path_to_input('7.txt')
    with open(path) as input_file:
        positions = [int(num) for num in input_file.readline().strip().split(',')]
        positions = Counter(positions)
        return binary_search(positions)


def part_two():
    path = path_to_input('7.txt')
    with open(path) as input_file:
        positions = [int(num) for num in input_file.readline().strip().split(',')]
        positions = Counter(positions)
        return binary_search(positions, True)
