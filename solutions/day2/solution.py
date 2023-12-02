from aocd import get_data
from aocd import submit
import os 

def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split(sep='\n')]

def check_counts(counts):
    red = counts['red']
    green = counts['green']
    blue = counts['blue']
    if red > 12 or green > 13 or blue > 14:
        return False 
    
    return True

def valid_game(subsets):    
    for subset in subsets:
        total_counts = { 'red': 0, 'green': 0, 'blue': 0 }
        #18 red, 8 green, 7 blue
        colors = subset.split(sep=', ')
        for color in colors:
            color_count = color.strip().split(' ')
            this_count = int(color_count[0])
            this_color = color_count[1]
            total_counts[this_color] += this_count

        if not check_counts(total_counts):
            return False
    
    return True
    
def part1(input):
    """Implementation for part 1"""
    valid_games = []
    for game in input:
        game_data = game.split(sep=': ')
        game_id = int(game_data[0].replace('Game ', ''))
        subsets = game_data[1].split(sep=';')
        if valid_game(subsets):
            valid_games.append(game_id)
    
    return sum(valid_games)

def get_power(subsets):
    max_counts = { 'red': 0, 'green': 0, 'blue': 0 }
    for subset in subsets:
        colors = subset.split(sep=', ')
        for color in colors:
            color_count = color.strip().split(' ')
            this_count = int(color_count[0])
            this_color = color_count[1]
            max_counts[this_color] = max(this_count, max_counts[this_color])
    
    return max_counts['red'] * max_counts['green'] * max_counts['blue']
    
def part2(input):
    """Implementation for part 2"""
    total = 0
    for game in input:
        game_data = game.split(sep=': ')
        subsets = game_data[1].split(sep=';')
        total += get_power(subsets)
    
    return total

def get_from_file():
    with open(os.getcwd() + '/solutions/day2/input.txt') as f:
        return f.readlines()

if __name__ == "__main__":
    year = 2023
    day = 2
    puzzle_input = get_data(day=day, year=year)
    input = parse(puzzle_input)
    #input = get_from_file()
    print(part1(input))
    #submit(part1(input), part="a", day=day, year=year)
    print(part2(input))
    #submit(part2(input), part="b", day=day, year=year)