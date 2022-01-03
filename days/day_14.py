from typing import Dict, Optional
from collections import Counter
from multiprocessing import Pool

from . import path_to_input
import asyncio


class Monomer:
    next: Optional["Monomer"]
    value: str

    def __init__(self, value: str):
        self.next = None
        self.value = value

    @property
    def pair(self):
        if not self.next:
            return self.value
        return self.value + self.next.value


class PolymerChain:
    rules: Dict[str, str]
    first: Optional[Monomer]
    last: Optional[Monomer]

    def __init__(self, template: str):
        self.rules = {}
        self.first = None
        self.last = None
        for value in template:
            self.append(value)

    def append(self, value: str):
        monomer = Monomer(value)
        if not self.first:
            self.first = monomer
        if self.last:
            self.last.next = monomer
        self.last = monomer

    def add_rule(self, rule: str):
        """ Expects str formatted like 'AB -> C' """
        key, value = rule.strip().split(' -> ')
        self.rules[key] = value

    def run_polymerization(self, steps: int):
        for i in range(steps):
            current = self.first
            print(i)
            while current:
                to_insert = self.rules.get(current.pair)
                next_monomer = current.next
                if to_insert:
                    current.next = Monomer(to_insert)
                    current.next.next = next_monomer
                current = next_monomer

    def answer_count(self):
        counter = Counter()
        current = self.first
        while current:
            counter[current.value] += 1
            current = current.next
        common = counter.most_common()
        return common[0][1] - common[-1][1]


class PolymerChainStringBuilder:
    rules: Dict[str, str]
    chain: str
    cache: Dict[str, str]

    def __init__(self, template: str):
        self.rules = {}
        self.cache = {}
        self.chain = template

    def add_rule(self, rule: str):
        """ Expects str formatted like 'AB -> C' """
        key, value = rule.strip().split(' -> ')
        self.rules[key] = value

    def run_polymerization_step(self, chain: str):
        cached = self.cache.get(chain)
        if cached:
            return cached
        new_chain = ''
        for i in range(len(chain)):
            new_chain += chain[i]
            if i + 1 == len(chain):
                break
            pair = chain[i:i + 2]
            to_insert = self.rules.get(pair)
            if to_insert:
                new_chain += to_insert
        self.cache[chain] = new_chain
        return new_chain

    def run_polymerization(self, steps: int, len_chunks=8):
        for _ in range(steps):
            print(_)
            chunks = [self.chain[i:i + len_chunks] for i in range(0, len(self.chain), len_chunks)]
            with Pool(10) as pool:
                results = pool.map(self.run_polymerization_step, chunks)
            new_chain = ''
            for i in range(len(results)):
                new_chain += results[i]
                if i + 1 == len(results):
                    break
                pair = new_chain[-1] + results[i + 1][0]
                if self.rules.get(pair):
                    new_chain += self.rules[pair]
            self.chain = new_chain

    def answer_count(self):
        counter = Counter(self.chain)
        common = counter.most_common()
        return common[0][1] - common[-1][1]


def part_one():
    path = path_to_input('14.txt')
    with open(path) as input_file:
        template = input_file.readline().strip()
        chain = PolymerChainStringBuilder(template)
        for line in input_file:
            if line.strip():
                chain.add_rule(line)
        chain.run_polymerization(10)
        return chain.answer_count()


async def part_two():
    path = path_to_input('14.txt')
    with open(path) as input_file:
        template = input_file.readline().strip()
        chain = PolymerChainStringBuilder(template)
        for line in input_file:
            if line.strip():
                chain.add_rule(line)
        chain.run_polymerization(40)
        print(chain.answer_count())
