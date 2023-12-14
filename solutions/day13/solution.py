from aocd import get_data
from aocd import submit
import os

def parse(puzzle_input):
    """Parse input."""    
    return puzzle_input.splitlines()

def diff(s1, s2):
    str_pairs = zip(s1, s2)
    return sum(1 for x, y in str_pairs if x != y)

def find_reflect(pattern, smudge_limit):
    pattern_len = len(pattern[0])
    max_size = pattern_len // 2 + 1

    for vert_line in reversed(range(1, max_size)):
        for line_pt in [0, pattern_len - 2 * vert_line]:     
            smudges = smudge_limit      
            for row in pattern:
                smudges -= diff(row[line_pt:line_pt + vert_line], row[line_pt + vert_line:line_pt + 2 * vert_line][::-1])

            if smudges != 0:
                continue

            return line_pt + vert_line 
        
    return 0 

def total_pattern(pattern, smudges):
    # try veritical line
    ans = find_reflect(pattern, smudges)
    if ans:
        return ans
    
    # rotate so we can try horizontal but treat it like it is vertical
    pattern = list(map(''.join, zip(*pattern)))
    return find_reflect(pattern, smudges) * 100

def part1(input, smudges = 0):
    """ Implementation for Part 1.
    """
    input.append('')
    ans = 0
    pattern = []
    for line in input:
        if not line.strip():
            if pattern:
                ans += total_pattern(pattern, smudges)
                pattern = []
        else:
            pattern.append(line)

    return ans 

def part2(input):
    return part1(input, 1)

def get_from_file():
    with open(os.getcwd() + '/solutions/day13/g3.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    year = 2023
    day = 13
    processing_g3chad = False
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
        part1ans = part1(input)
        part2ans = part2(input)
        print(part1ans)
        print(part2ans)
