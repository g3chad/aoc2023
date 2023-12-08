from aocd import get_data
from aocd import submit
import os
import math

def parse(puzzle_input):
    """Parse input."""    
    return puzzle_input.splitlines()


def part1(input, start, must_be_all_Z):
    """ Implementation for Part 1.
    """
    moves = [c for c in input[0]]
    tree_nodes = input[2:]
    tree_map = {}
    for entry in tree_nodes:
        key = entry.split(' = ')[0]
        left,right = entry.split(' = ')[1].replace('(','').replace(')','').split(', ')
        tree_map[key] = (left, right)
    
    cur_move = 0
    last_move = len(moves) - 1
    cur_node = start
    steps = 0
    while True: 
        left, right = tree_map[cur_node]
        move = moves[cur_move]
        cur_move += 1
        if cur_move > last_move:
            cur_move = 0
        cur_node = right if move == 'R' else left
        steps += 1
        if cur_node == 'ZZZ' or (cur_node[-1] == 'Z' and not must_be_all_Z):
            break
    
    return steps

def part2(input):
    tree_nodes = input[2:]
    starts = []
    for entry in tree_nodes:
        key = entry.split(' = ')[0]
        # if this key ends with an A it is a starts node
        if key[-1] == 'A':
            starts.append(key)
    steps = []
    for key in starts:
        steps.append(part1(input, key, False))
    ans = math.lcm(*steps)
    return ans

def get_from_file():
    with open(os.getcwd() + '/solutions/day08/bf.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    year = 2023
    day = 8
    processing_g3chad = True
    if processing_g3chad:
        # processing for my personal leaderboard, get data using my configured login
        puzzle_input = get_data(day=day, year=year)
        input = parse(puzzle_input)        
        submit(part1(input), part="a", day=day, year=year)
        submit(part2(input), part="b", day=day, year=year)
    else:
        # processing for the other leaderboard via file input
        puzzle_input = get_from_file()
        input = parse(puzzle_input)
        part1ans = part1(input, 'AAA', True)
        part2ans = part2(input)
        print(part1ans)
        print(part2ans)
