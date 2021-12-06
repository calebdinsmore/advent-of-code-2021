from typing import List, Dict

from . import path_to_input

"""
Day 6 - Lanternfish


"""


def bad_simulate_fish(days: int, initial_state: List[int]):
    """
    If you implement the algorithm from the prompt, you get this, which takes 20 years to run
    """
    current_state = initial_state
    for _ in range(days):
        new_state = []
        newborns = []
        for fish in current_state:
            fish -= 1
            if fish == -1:
                new_state.append(6)
                newborns.append(8)
            else:
                new_state.append(fish)
            current_state = new_state + newborns
    return current_state


def simulate_fish(days: int, egg_dict: Dict[int, int]):
    current_state = egg_dict
    for _ in range(days):
        new_state = dict([(stage, 0) for stage in range(0, 9)])
        for stage, num_fish in current_state.items():
            if stage == 0:
                new_state[8] += num_fish
                new_state[6] += num_fish
            else:
                new_state[stage - 1] += num_fish
        current_state = new_state
    return current_state


def create_egg_groups(initial_state):
    """
    Creates a dictionary where each key is the stage that an egg group is in (0-8) and the values are how many fish are
    in that egg group.
    :param initial_state: List of numbers, each representing a fish at that number's egg stage
    :return: Fish dictionary
    """
    egg_dict = {}
    for fish in initial_state:
        if fish not in egg_dict:
            egg_dict[fish] = 0
        egg_dict[fish] += 1
    return egg_dict


def part_one():
    path = path_to_input('6.txt')
    with open(path) as input_file:
        initial_state = input_file.readline().strip().split(',')
        initial_state = [int(fish) for fish in initial_state]
        egg_groups = create_egg_groups(initial_state)
        final_state = simulate_fish(80, egg_groups)
        return sum(final_state.values())


def part_two():
    path = path_to_input('6.txt')
    with open(path) as input_file:
        initial_state = input_file.readline().strip().split(',')
        initial_state = [int(fish) for fish in initial_state]
        egg_groups = create_egg_groups(initial_state)
        final_state = simulate_fish(256, egg_groups)
        return sum(final_state.values())
