from aocd import get_data
from aocd import submit
import os

cache = {}

def parse(puzzle_input):
    """Parse input."""    
    return puzzle_input.splitlines()

def get_arrangements(springs, groups):

    # base case
    if not groups:
        if '#' not in springs:
            return 1
        else:
            return 0
    if not springs:
        return 0
    
    # check cache
    if (springs, groups) in cache:
        return cache[(springs, groups)]
    
    next_spring_char = springs[0]
    next_group = groups[0]

    def pound_sign():
        cur_grp = springs[:next_group].replace('?', '#')
        if cur_grp != next_group * '#':
            return 0
        if len(springs) == next_group:
            if len(groups) == 1:
                return 1
            else:
                return 0
        if springs[next_group] in '?.':
            return get_arrangements(springs[next_group + 1:], groups[1:])
        
        return 0

    def dot_sign():
        return get_arrangements(springs[1:], groups)
    
    if next_spring_char == '#':
        val = pound_sign()
    elif next_spring_char == '.':
        val = dot_sign()
    elif next_spring_char == '?':
        val = dot_sign() + pound_sign()
    
    cache[(springs, groups)] = val
    print(springs, groups, "->", val)

    return val

def part1(input, fold=False):
    """ Implementation for Part 1.
    """

    total_arrangements = 0
    for line in input:
        springs = line.split()[0]
        groups = [int(x) for x in line.split()[1].split(',')]
        if fold:
            springs = ((springs + '?') * 4) + springs
            groups = groups * 5
        total_arrangements += get_arrangements(springs, tuple(groups))

    return total_arrangements

def part2(input):
    return part1(input, fold=True)

def get_from_file():
    with open(os.getcwd() + '/solutions/day12/bf.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    year = 2023
    day = 12
    processing_g3chad = False
    if processing_g3chad:
        # processing for my personal leaderboard, get data using my configured login
        puzzle_input = get_data(day=day, year=year)
        input = parse(puzzle_input)        
        #submit(part1(input), part="a", day=day, year=year)
        submit(part2(input), part="b", day=day, year=year)
    else:
        # processing for the other leaderboard via file input
        puzzle_input = get_from_file()
        input = parse(puzzle_input)
        part1ans = part1(input)
        part2ans = part2(input)
        print(part1ans)
        print(part2ans)
