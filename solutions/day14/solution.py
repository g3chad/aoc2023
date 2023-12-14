from aocd import get_data
from aocd import submit
import os 
import numpy as np
from copy import copy

def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split(sep='\n')]

def shift_rocks(matrix):
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] == ".":
                # bubble up the Os
                for next_row in range(row + 1, len(matrix)):
                    if matrix[next_row][col] == "O":
                        matrix[next_row][col] = "."
                        matrix[row][col] = "O"
                        break
                    # we hit a wall
                    elif matrix[next_row][col] == "#":
                        break
def get_total(matrix):
    total = 0
    for row_num in range(len(matrix) - 1, -1, -1):
        cnt = len([i for i in matrix[row_num] if i == 'O'])
        row = abs((row_num + 1) - len(matrix))
        line_tot = (row + 1) * cnt
        total += line_tot
    
    return total

def matrix_to_str(matrix):
    str = "\n".join("".join(row) for row in matrix)
    return str

def part1(input):
    """Implementation for part 1"""
    matrix = [[c for c in line] for line in input]
    shift_rocks(matrix)
    return get_total(matrix)
    
def part2(input):
    """Implementation for part 2"""
    cache = {}
    matrix = np.array([[c for c in line] for line in input])
    matrix_entries = []
    cycle_offset = 0
    cur_cycle = 0
    final_matrix = None
    max_cycles = 1_000_000_000
    for cycle in range(max_cycles):
        mat_str = matrix_to_str(matrix)
        mat_copy = copy(matrix)
        if mat_str in cache:
            cycle_offset = cache[mat_str]
            cur_cycle = cycle
            break
        # go through a cycle
        for _ in range(4):
            shift_rocks(matrix)
            # rotate so when we shift we can reuse our north shifting logic
            matrix = np.rot90(matrix, k=3)

        cache[mat_str] = cycle
        matrix_entries.append(mat_copy)

    t = cycle_offset + ((max_cycles - cycle_offset) % (cur_cycle-cycle_offset))
    final_matrix = matrix_entries[t]
    return get_total(final_matrix)

def get_from_file():
    with open(os.getcwd() + '/solutions/day14/g3.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    year = 2023
    day = 14
    processing_g3chad = False
    if processing_g3chad:
        # processing for my personal leaderboard, get data using my configured login
        puzzle_input = get_data(day=day, year=year)
        input = parse(puzzle_input)        
        submit(part1(input), part="a", day=day, year=year)
        #submit(part2(input), part="b", day=day, year=year)
    else:
        # processing for the other leaderboard via file input
        puzzle_input = get_from_file()
        input = parse(puzzle_input)
        part1ans = part1(input)
        part2ans = part2(input)
        print(part1ans)
        print(part2ans)
