from aocd import get_data
from aocd import submit
import os 

def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split(sep='\n')]
    
def part1(input):
    """Implementation for part 1"""
    pass
    
def part2(input):
    """Implementation for part 2"""
    pass

def get_from_file():
    with open(os.getcwd() + '/solutions/day14/input.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    year = 2023
    day = 14
    processing_g3chad = False
    if processing_g3chad:
        # processing for my personal leaderboard, get data using my configured login
        puzzle_input = get_data(day=day, year=year)
        input = parse(puzzle_input)        
        #submit(part1(input), part="a", day=day, year=year)
        #submit(part2(input), part="b", day=day, year=year)
    else:
        # processing for the other leaderboard via file input
        puzzle_input = get_from_file()
        input = parse(puzzle_input)
        part1ans = part1(input)
        part2ans = part2(input)
        print(part1ans)
        print(part2ans)
