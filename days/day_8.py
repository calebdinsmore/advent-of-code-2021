import select
from typing import Dict, Optional

from . import path_to_input


"""
Day 8
-----

Part 1 is pretty straight-forward: just count up how many of the known numbers there are.

Part 2 is where things get interesting.
The DisplayInfo class builds two key dictionaries:
    - number_map: a map from the 10 digits to the set of signals corresponding with their output values
    - segment_map: a map from the 7 original letter segments (a-f) to the letter that now corresponds with that
      segment

Everywhere I refer to the letters 'a' - 'f' (like in segment_map), I'm referring to the official placement indicated
here:
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
 
---
The Deduction Algorithm:
I'm sure there's a better way to do this, but here's how I deduce each of the segments and number sets:

1. Get the set corresponding to the number 2 by doing the following:
    a. Get signal patterns of length 5 (2, 3, 5)
    b. Subtract the 4-set and 7-set from each of those signal patterns
    c. The 2-set is the result with length 2, since the e and g segments would remain
2. The intersection of 2-set and 1-set gives us c
3. We get f by getting the remaining segment when we remove c from the 1-set
4. A is easy: get the difference of the 7-set and the 1-set
5. The 5-set is the set of length 5 that does not contain the c segment
6. The 3-set is the set of length 5 that isn't the 2-set or 5-set (which we both now know)

Quick recap:
We now know the following number-sets and segment maps:
1, 2, 3, 4, 5, 7, 8 (missing 0, 6, 9)
a, c, f (missing b, d, e, g)

7. D is the intersection of the 3-set and 4-set minus the 1-set
8. B is the 4-set minus a set of segments (c, f, d)
9. G is the 5-set minus a set of segments (a, b, d, f)
10. E is the 8-set minus a set of segments (a, b, c, d, f, g)

And that's it!
"""


class DisplayInfo:
    number_map: Dict[int, Optional[set]]
    segment_map: Dict[str, Optional[str]]
    output_number: int

    def __init__(self, input_line: str):
        signal_str, output_str = input_line.strip().split('|')
        self.signals = signal_str.strip().split()
        self.outputs = output_str.strip().split()
        self.num_unique = len([out for out in self.outputs if len(out) in [2, 4, 3, 7]])

        self.deduce_mappings()

    @property
    def output(self):
        final_output = ''
        for output in self.outputs:
            output_set = set(output)
            for number, number_set in self.number_map.items():
                if output_set == number_set:
                    final_output += str(number)
        return int(final_output)

    def deduce_mappings(self):
        self.segment_map = dict([(letter, None) for letter in set('abcdefg')])
        self.number_map = dict([(num, None) for num in range(0, 10)])
        self.populate_known_numbers()

        self.deduce_c_f_2()
        self.deduce_a_5()
        self.deduce_3()
        self.deduce_d()
        self.deduce_b()
        self.deduce_g()
        self.deduce_e()
        self.populate_remaining_numbers()

    def populate_known_numbers(self):
        one = next(filter(lambda x: len(x) == 2, self.signals))
        four = next(filter(lambda x: len(x) == 4, self.signals))
        seven = next(filter(lambda x: len(x) == 3, self.signals))
        eight = next(filter(lambda x: len(x) == 7, self.signals))
        self.number_map[1] = set(one)
        self.number_map[4] = set(four)
        self.number_map[7] = set(seven)
        self.number_map[8] = set(eight)

    def deduce_c_f_2(self):
        """ Find the signals mapping to c and f, as well as the number:set mapping for 2 """
        one_set = self.number_map[1]
        four_set = self.number_map[4]
        seven_set = self.number_map[7]
        # 2 is the only number with length 5 that when you subtract 4 and 7 segments, you have two remaining segments
        two = next(filter(lambda sig: len(sig) == 5 and len(set(sig) - four_set - seven_set) == 2, self.signals))
        two_set = set(two)
        # c is the intersection of 1 and 2, since 2 does not activate f
        self.segment_map['c'] = (two_set & one_set).pop()
        # f is the other signal in one that's not c - duh
        self.segment_map['f'] = next(filter(lambda x: x != self.segment_map['c'], one_set))
        self.number_map[2] = two_set

    def deduce_a_5(self):
        # a is the difference from set(7) - set(1)
        self.segment_map['a'] = (self.number_map[7] - self.number_map[1]).pop()

        # knowing c, we can deduce 5 by getting the 5-length signal without c
        five = next(filter(lambda x: len(x) == 5 and self.segment_map['c'] not in x, self.signals))
        self.number_map[5] = set(five)

    def deduce_3(self):
        len_5 = filter(lambda x: len(x) == 5, self.signals)
        three = next(filter(lambda x: set(x) != self.number_map[2] and set(x) != self.number_map[5], len_5))
        self.number_map[3] = set(three)

    def deduce_d(self):
        cf = self.build_signal_from_map('cf')
        d = (self.number_map[3] & self.number_map[4]) - set(cf)
        self.segment_map['d'] = d.pop()

    def deduce_b(self):
        cfd = self.build_signal_from_map('cfd')
        b = (self.number_map[4] - set(cfd)).pop()
        self.segment_map['b'] = b

    def deduce_g(self):
        abdf = self.build_signal_from_map('abdf')
        g = (self.number_map[5] - set(abdf)).pop()
        self.segment_map['g'] = g

    def deduce_e(self):
        abcdfg = self.build_signal_from_map('abcdfg')
        e = (self.number_map[8] - set(abcdfg)).pop()
        self.segment_map['e'] = e

    def populate_remaining_numbers(self):
        """ Now that we know how the segments map, populate 0, 6, and 9 """
        self.number_map[0] = set(self.build_signal_from_map('abcefg'))
        self.number_map[6] = set(self.build_signal_from_map('abdefg'))
        self.number_map[9] = set(self.build_signal_from_map('abcdfg'))

    def build_signal_from_map(self, segments: str):
        signal = ''
        for part in segments:
            signal += self.segment_map[part]
        return signal


def part_one():
    path = path_to_input('8.txt')
    with open(path) as input_file:
        display_infos = []
        for line in input_file:
            display_infos.append(DisplayInfo(line))
        return sum([info.num_unique for info in display_infos])


def part_two():
    path = path_to_input('8.txt')
    with open(path) as input_file:
        display_infos = []
        for line in input_file:
            display_infos.append(DisplayInfo(line))
        return sum([info.output for info in display_infos])
