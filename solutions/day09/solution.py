from aocd import get_data
from aocd import submit
import os

def parse(puzzle_input):
    """Parse input."""    
    return puzzle_input.splitlines()

def find_missing(history):
    lines = [ history ]
    line_num = 0
    while True:
        all_zero = True
        new_line = ''
        cur_line = lines[line_num].split(' ')
        for i in range(0, len(cur_line) - 1):
            diff = int(cur_line[i + 1]) - int(cur_line[i])
            new_line += ' ' + str(diff)            
            if diff != 0:
                all_zero = False
        lines.append(new_line.strip())
        if all_zero:
            break
        else:
            line_num += 1
    
    # extrapolate
    lines[-1] = lines[-1] + ' 0'
    new_val = 0
    for i in range(len(lines) - 1, 0, -1):
        end_line = int(lines[i].split(' ')[-1])
        end_line_above = int(lines[i-1].split(' ')[-1])
        new_val = end_line_above + end_line
        lines[i-1] = lines[i-1] + ' ' + str(new_val)

    return new_val

# to do this could be updated in the one method to avoid the code dupes
def find_missing_backwards(history):
    lines = [ history ]
    line_num = 0
    while True:
        all_zero = True
        new_line = ''
        cur_line = lines[line_num].split(' ')
        for i in range(0, len(cur_line) - 1):
            diff = int(cur_line[i + 1]) - int(cur_line[i])
            new_line += ' ' + str(diff)            
            if diff != 0:
                all_zero = False
        lines.append(new_line.strip())
        if all_zero:
            break
        else:
            line_num += 1
    
    # extrapolate
    lines[-1] = '0 ' + lines[-1]
    new_val = 0
    for i in range(len(lines) - 1, 0, -1):
        start_line = int(lines[i].split(' ')[0])
        start_line_above = int(lines[i-1].split(' ')[0])
        new_val = start_line_above - start_line
        lines[i-1] = str(new_val) + ' ' + lines[i-1]

    return new_val

def part1(input):
    """ Implementation for Part 1.
    """
    missing_numbers = []
    for history in input:
        missing = find_missing(history)
        missing_numbers.append(missing)

    return sum(missing_numbers)

def part2(input):
    missing_numbers = []
    for history in input:
        missing = find_missing_backwards(history)
        missing_numbers.append(missing)

    return sum(missing_numbers)

def get_from_file():
    with open(os.getcwd() + '/solutions/day09/bf.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    year = 2023
    day = 9
    processing_g3chad = True
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
