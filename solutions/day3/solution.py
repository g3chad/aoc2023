from aocd import get_data
from aocd import submit
import os

def parse(puzzle_input):
    """Parse input."""    
    return puzzle_input.splitlines()

def is_adjacent(cur_number, line, number_end, symbol_row, symbol_col):
    num_start = (number_end - len(cur_number)) + 1
    for index in range(len(cur_number)):
        col_to_check = num_start + index
        # is this digit in the number adjacent to our target row,col of the symbol?
        # check left and right in case we're at first digit or last digit
        if (line, col_to_check - 1) == (symbol_row, symbol_col):
            return True
        if (line, col_to_check + 1) == (symbol_row, symbol_col):
            return True
        
        # check back a row, back a row to left, back a row to right
        if (line - 1, col_to_check) == (symbol_row, symbol_col):
            return True
        if (line - 1, col_to_check - 1) == (symbol_row, symbol_col):
            return True
        if (line - 1, col_to_check + 1) == (symbol_row, symbol_col):
            return True

        # check down a row, down a row to left, down a row to right
        if (line + 1, col_to_check) == (symbol_row, symbol_col):
            return True
        if (line + 1, col_to_check - 1) == (symbol_row, symbol_col):
            return True
        if (line + 1, col_to_check + 1) == (symbol_row, symbol_col):
            return True

    return False 

def get_adj_lines(input, row): 
    """
        To check potential adjacent numbers for the symbol's row
        we just want to get the row before it, its row, then row after
        but make sure we're not going out of bounds!
    """
    lines_to_check = []
    if row > 0:
        lines_to_check.append(row - 1)
    lines_to_check.append(row)
    if row < len(input) - 1:
        lines_to_check.append(row + 1)
    
    return lines_to_check

def get_adj_parts(input, symbol_row, symbol_col, visited):
    """ 
        input is the grid board we're navigating
        symbol_row and symbol_col are the coords of the symbol 
            
        Check for adjacent numbers by going through adjacent lines
            that are in scope for potential adjacency to this symbol coord
            and finding numbers on those lines and seeing if those numbers
            are adjacent to the symbol we're checking
    """
    lines_to_check = get_adj_lines(input, symbol_row)
    adj_parts = []

    # just check the lines adjacent to the row,col of the symbol
    # should never be more than 3 lines to check and would be
    # 2 lines if we're on the border
    for line in lines_to_check:
        # for each char in this line (a line is row in the grid), 
        # build up each specific number going char by char
        # then see if that number is adjacent to the symbol at row,col
        # we have our number if we hit a non digit or the last char in the line
        cur_number = ''
        for c,char in enumerate(input[line]):
            if char.isdigit():
                cur_number += char
            if cur_number != '' and (not char.isdigit() or c == len(input[line]) - 1):
                number_end = c - 1
                if char.isdigit():
                    number_end = c
                if (not (cur_number, line, number_end) in visited and 
                    is_adjacent(cur_number, line, number_end, symbol_row, symbol_col)):
                    adj_parts.append(int(cur_number))
                    visited.add((cur_number, line, number_end))
                cur_number = ''

    return adj_parts

def part1(input):
    """ Implementation for Part 1.
        Navigate the grid and find relevant symbols then 
        get numbers that are adjacent to the symbol but careful not to
        process the same part number twice.  Searching with the symbol as
        the starting point is more efficient than going through all the 
        numbers since there are fewer symbols and we can avoid any 
        numbers that are invalid and not waste time looking at them.
    """
    parts = []
    visited = set()
    for row, line in enumerate(input):
        for col, char in enumerate(line):
            if char != '.' and not char.isdigit():
                neighbor_parts = get_adj_parts(input, row, col, visited)
                parts.extend(neighbor_parts)

    return sum(parts)
    
def part2(input):
    """Implementation for Part 2
       Reuse part 1 but only look at the * symbol ignoring any others
       since those are not gears and we only care about gears
    """
    gear_ratios = []
    visited = set()
    for row, line in enumerate(input):
        for col, char in enumerate(line):
            if char == '*':
                neighbor_parts = get_adj_parts(input, row, col, visited)
                if len(neighbor_parts) == 2:
                    gear_ratios.append(neighbor_parts[0] * neighbor_parts[1])

    return sum(gear_ratios)

def get_from_file():
    with open(os.getcwd() + '/solutions/day3/bf.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    year = 2023
    day = 3
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
        part1ans = part1(input)
        part2ans = part2(input)
        print(part1ans)
        print(part2ans)
