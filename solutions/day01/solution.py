from aocd import get_data
from aocd import submit
import re

def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split(sep='\n')]

def convert_to_easy_numbers(input):
    # Hi Barry, I know you like to keep things simple, so this is for you!
    # I think this could be a one liner but it runs fine and I think is easier to read
    input = re.sub("one", "o1e", input, flags=re.IGNORECASE)
    input = re.sub("two", "t2o", input, flags=re.IGNORECASE)
    input = re.sub("three", "t3ree", input, flags=re.IGNORECASE)
    input = re.sub("four", "f4ur", input, flags=re.IGNORECASE)
    input = re.sub("five", "f5ve", input, flags=re.IGNORECASE)
    input = re.sub("six", "s6x", input, flags=re.IGNORECASE)
    input = re.sub("seven", "s7ven", input, flags=re.IGNORECASE)
    input = re.sub("eight", "e8ght", input, flags=re.IGNORECASE)
    input = re.sub("nine", "n9ne", input, flags=re.IGNORECASE)
    input = re.sub("zero", "z0ro", input, flags=re.IGNORECASE)

    return input
    
def part1(input):
    """Implementation for part 1"""
    total = 0
    for calibration in input:
        just_digits = re.sub("[^0-9]", "", calibration)
        first_two = just_digits[0] + just_digits[-1]
        total += int(first_two)

    return total
    
def part2(input):
    """Implementation for part 2"""
    total = 0
    for calibration in input:
        easy_numbers = convert_to_easy_numbers(calibration)
        just_digits = re.sub("[^0-9]", "", easy_numbers, flags=re.IGNORECASE)
        first_two = just_digits[0] + just_digits[-1]
        total += int(first_two)

    return total
    

if __name__ == "__main__":
    year = 2023
    day = 1
    puzzle_input = get_data(day=day, year=year)        
    input = parse(puzzle_input)
    submit(part1(input), part="a", day=day, year=year)
    part2ans = part2(input)
    print(f'Part 2: {part2ans}')
    submit(part2ans, part="b", day=day, year=year)