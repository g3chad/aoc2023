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
    with open(os.getcwd() + '/solutions/day/input.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    puzzle_input = get_from_file()
    input = parse(puzzle_input)
    part1ans = part1(input)
    part2ans = part2(input)
    print(part1ans)
    print(part2ans)
