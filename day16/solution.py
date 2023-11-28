from aocd import get_data
from aocd import submit

def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split(sep='\n')]
    
def part1(input):
    """Implementation for part 1"""
    pass
    
def part2(input):
    """Implementation for part 2"""
    pass

if __name__ == "__main__":
    year = 2023
    day = 16
    puzzle_input = get_data(day=day, year=year)        
    input = parse(puzzle_input)
    submit(part1(input), part="a", day=day, year=year)
    #submit(part2(input), part="b", day=day, year=year)