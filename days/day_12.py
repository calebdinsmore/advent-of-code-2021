from typing import List, Set, Dict
from collections import deque, defaultdict

from . import path_to_input


def build_graph(edges: List[str]) -> Dict[str, List[str]]:
    graph = defaultdict(lambda: [])
    for edge in edges:
        vertex_a, vertex_b = edge.split('-')
        graph[vertex_a].append(vertex_b)
        graph[vertex_b].append(vertex_a)
    return graph


def part_one():
    path = path_to_input('12.txt')
    with open(path) as input_file:
        graph = build_graph([line.strip() for line in input_file.readlines()])
    paths: Set[str] = set()
    queue = deque([('start', '')])
    while queue:
        vertex, path_to_vertex = queue.popleft()
        for edge in graph[vertex]:
            if edge == 'start':
                continue
            elif edge == 'end':
                paths.add(f'{path_to_vertex},{vertex},end')
            elif edge.isupper() or (edge.islower() and edge not in path_to_vertex):
                queue.append((edge, f'{path_to_vertex},{vertex}'))
    return len(paths)


def part_two():
    path = path_to_input('12.txt')
    with open(path) as input_file:
        graph = build_graph([line.strip() for line in input_file.readlines()])
    paths: Set[str] = set()
    small_caves = list(filter(lambda x: x.islower() and x not in {'start', 'end'}, graph.keys()))
    for cave in small_caves:
        queue = deque([('start', '')])
        while queue:
            vertex, path_to_vertex = queue.popleft()
            for edge in graph[vertex]:
                if edge == 'start':
                    continue
                elif edge == 'end':
                    paths.add(f'{path_to_vertex},{vertex},end')
                elif edge.islower() and path_to_vertex.count(edge) == 1 and edge != cave:
                    continue
                elif edge == cave and path_to_vertex.count(edge) == 2:
                    continue
                else:
                    queue.append((edge, f'{path_to_vertex},{vertex}'))
    return len(paths)
