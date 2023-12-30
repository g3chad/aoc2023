import random
import os
import networkx as nx 

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