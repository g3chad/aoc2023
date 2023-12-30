import random
import os
import networkx as nx 

# def karger_min_cut(graph):
#     while len(graph) > 2:
#         node1, node2 = random.choice(list(graph.items()))
#         graph[node1].extend(graph[node2])
#         for node in graph[node2]:
#             graph[node].remove(node2)
#             graph[node].append(node1)
#         del graph[node2]
#     return len(list(graph.values())[0])

# def find_min_cut(graph, iterations):
#     min_cut = float('inf')
#     for _ in range(iterations):
#         new_graph = defaultdict(list, {k: v[:] for k, v in graph.items()})
#         cut = karger_min_cut(new_graph)
#         min_cut = min(min_cut, cut)
#     return min_cut

# cuts=[]
# def kargerMinCut(graph):
#     while len(graph) > 2:
#          v = random.choice(list(graph.keys()))
#          w = random.choice(graph[v])
#          contract(graph, v, w)
#     mincut = len(graph[list(graph.keys())[0]])
#     cuts.append(mincut)
#     return mincut

# def contract(graph, v, w):
#     if w not in graph:
#         return
#     for node in graph[w]:  # merge the nodes from w to v
#          if node != v:  # we dont want to add self-loops
#              graph[v].append(node)
#          if node in graph and w in graph[node]:
#             graph[node].remove(w)  # delete the edges to the absorbed 
#          if node in graph and node != v:
#               graph[node].append(v)
#     del graph[w]  # delete the absorbed vertex 'w'

def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split(sep='\n')]
    
def part1(input):
    """Implementation for part 1"""
    G = nx.Graph()
    for line in input:
        left, right = line.split(': ')
        for other in right.split(' '):
            G.add_edge(left, other)

    cc = nx.spectral_bisection(G)
    return len(cc[0]) * len(cc[1])    
    
def part2(input):
    """Implementation for part 2"""
    return 0

def get_from_file():
    with open(os.getcwd() + '/solutions/day25/bf.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    puzzle_input = get_from_file()
    input = parse(puzzle_input)
    part1ans = part1(input)
    part2ans = part2(input)
    print(part1ans)
    print(part2ans)