import os 
import math
from copy import deepcopy

def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split(sep='\n')]


def part1(input, steps_to_take=64):
    """Implementation for part 1"""
    ROWS = len(input)
    COLS = len(input[0])
    start = (-1,-1)
    queue = [] 
    visited = set()
    grid = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(0)
            if input[r][c] == 'S':
                start = (r,c)
                queue.append(start)
        grid.append(row)
            
    done = steps_to_take
    for s in range(done):     
        curr_level_queue = deepcopy(queue)
        visited = set(deepcopy(queue))
        queue = []   
        while curr_level_queue:
            c_row, c_col = curr_level_queue.pop(0)           
            for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_r, new_c = c_row + dir[0], c_col + dir[1]
                if (new_r >= 0 and new_c >= 0 and new_r < ROWS and new_c < COLS
                    and (new_r, new_c) not in visited
                    and input[new_r][new_c] != "#"):
                    visited.add((new_r, new_c))
                    queue.append((new_r, new_c))  
    
    return len(queue)

def part2(input):
    ROWS = len(input)
    COLS = len(input[0])
    start = (-1,-1)
    queue = [] 
    visited = set()
    grid = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(0)
            if input[r][c] == 'S':
                start = (r,c)
                queue.append(start)
        grid.append(row)
    
    cycle_states = []
    mod = 26501365 % ROWS
    # we're just repeating the same grid over and over in both directions
    # and the start can go unimpeded up and down and left and right
    # over and over to infinity so can we use these attributes
    # to take advantage of some math mod out the grids and 
    # simulate going through the grid 65, 131 + 65 and 65 + 131 + 131
    # which are the numbers to hit the border from the center then loop back
    # a cycle.  This is VERY input dependent so studying the input is required
    # I admit I got help from tips on the internet to modify part 1 to handle this
    # lots of tips, I Would have never come up with this one on my own!
    for cycle in [mod, mod + ROWS, mod + ROWS * 2]:
        queue = [start]
        for _ in range(cycle):
            curr_level_queue = deepcopy(queue)
            visited = set(deepcopy(queue))
            queue = []   
            while curr_level_queue:
                c_row, c_col = curr_level_queue.pop(0)           
                for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    new_r, new_c = c_row + dir[0], c_col + dir[1]
                    if input[new_r % ROWS][new_c % COLS] != "#" and (new_r, new_c) not in visited:
                        visited.add((new_r, new_c))
                        queue.append((new_r, new_c))  
        
        cycle_states.append(len(queue))
    
    # and the math based on the quadratic equation this repeat through the grids causes which
    # the tips helped me get this big time, I felt like I cheated today except for my search logic
    # def needed help on the math and recognizing the pattern in the input.  Lesson learned, study the input
    # and don't assume the example input will give you any clues or have the same patterns - uggh!
    m = cycle_states[1] - cycle_states[0]
    n = cycle_states[2] - cycle_states[1]
    a = (n - m) // 2
    b = m - 3 * a
    c = cycle_states[0] - b - a

    ceiling = math.ceil(26501365 / ROWS)

    return a * ceiling ** 2 + b * ceiling + c

def get_from_file():
    with open(os.getcwd() + '/solutions/day21/bf.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    puzzle_input = get_from_file()
    input = parse(puzzle_input)
    part1ans = part1(input)
    part2ans = part2(input)
    print(part1ans)
    print(part2ans)
