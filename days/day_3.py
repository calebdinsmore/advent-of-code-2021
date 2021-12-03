from typing import Dict

from . import path_to_input


def part_one():
    path = path_to_input('3.txt')
    with open(path) as input_file:
        # initialize sum_positions as array of 12 0s
        sum_positions = [0] * 12
        report_length = 0
        gamma_rate = ''
        epsilon_rate = ''
        for line in input_file:
            report_length += 1
            for i in range(len(line.strip())):
                sum_positions[i] += int(line[i])
        for p_sum in sum_positions:
            minority_amount = report_length // 2
            if p_sum <= minority_amount:
                # if there are more 0s than 1s
                gamma_rate += '0'
                epsilon_rate += '1'
            else:
                gamma_rate += '1'
                epsilon_rate += '0'
        gamma_rate = int(gamma_rate, 2)
        epsilon_rate = int(epsilon_rate, 2)
        return gamma_rate * epsilon_rate


'''
Part Two

The most optimal solution I could think of for this one is to use a trie data structure, 
where each node keeps track of how many descendants it has.
'''


class TrieNode:
    children: Dict[str, "TrieNode"]

    def __init__(self):
        self.children = {}
        self.num_descendants = 0

    def insert(self, string: str):
        if not string:
            return
        bit = string[0]
        if bit in self.children:
            next_node = self.children[bit]
        else:
            next_node = TrieNode()
            self.children[bit] = next_node
        if len(string) > 1:
            next_node.insert(string[1:])
        self.num_descendants += 1


def find_o2_rating(node: TrieNode):
    rating = ''
    current_node = node
    while current_node.num_descendants > 0:
        num_0 = current_node.children['0'].num_descendants if '0' in current_node.children else 0
        num_1 = current_node.children['1'].num_descendants if '1' in current_node.children else 0
        if num_1 >= num_0:
            rating += '1'
            current_node = current_node.children['1']
        else:
            rating += '0'
            current_node = current_node.children['0']
    return rating


def find_co2_scrubber_rating(node: TrieNode):
    rating = ''
    current_node = node
    while current_node.num_descendants > 0:
        num_0 = current_node.children['0'].num_descendants if '0' in current_node.children else 0
        num_1 = current_node.children['1'].num_descendants if '1' in current_node.children else 0
        if num_0 <= num_1 and '0' in current_node.children:
            rating += '0'
            current_node = current_node.children['0']
        elif '1' in current_node.children:
            rating += '1'
            current_node = current_node.children['1']
    return rating


def part_two():
    path = path_to_input('3.txt')
    with open(path) as input_file:
        root_node = TrieNode()
        for line in input_file:
            root_node.insert(line.strip())
        o2_rating = int(find_o2_rating(root_node), 2)
        co2_rating = int(find_co2_scrubber_rating(root_node), 2)
        return o2_rating * co2_rating
