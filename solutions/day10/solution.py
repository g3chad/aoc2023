from aocd import get_data
from aocd import submit
import os
from collections import deque

def parse(puzzle_input):
    """Parse input."""    
    return puzzle_input.splitlines()

def get_start_point(input):
    for r in range(len(input)):
        for c in range(len(input[r])):
            if input[r][c] == 'S':
                return (r,c)


def part1(input):
    """ Implementation for Part 1.
    """
    ROWS = len(input)
    COLS = len(input[0])
    def can_move(cr,cc,nr,nc,visited):
        if nr < 0 or nr >= ROWS or nc < 0 or nc >= COLS:
            return False
        if (nr,nc) in visited:
            return False        
        cur_char = input[cr][cc]
        next_char = input[nr][nc] 

        # Barry, man this is some ugly code and I'm sorry you had to see this.  I'll clean this up
        # but was coding fast to get done and this worked to handle our S special case
        if cur_char == 'S':
            can_queue = False
            # left from the S
            if (cr == nr and nc == cc - 1 
                and (next_char == '-' or next_char == 'L' or next_char == 'F')):
                    can_queue = True
            # up from the S
            elif (nr == cr - 1 and cc == nc 
                and (next_char == '|' or next_char == '7' or next_char == 'F')):
                    can_queue = True
            # down from the S
            elif (nr == cr + 1 and cc == nc 
                and (next_char == '|' or next_char == 'L' or next_char == 'J')):
                    can_queue = True
            else:
                # right from the S
                if (next_char == '-' or next_char == 'J' or next_char == '7'):
                    can_queue = True
            return can_queue
        else:
            dirs = dir_map[cur_char]
            if (nr-cr, nc-cc) in dirs:
                # can go this dir from cur location
                # can this dest char connect to cur char
                if (cr-nr, cc-nc) in dir_map[next_char]:
                    return True
            return False

    moves = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    N, S, E, W = (-1, 0), (1, 0), (0, 1), (0, -1)
    dir_map = {
            '|': (N, S),   
            '-': (E, W), 
            'L': (N, E), 
            'J': (N, W), 
            '7': (S, W),   
            'F': (S, E), 
            '.': ()
         }
    s_row, s_col = get_start_point(input)
    queue = deque()
    queue.append((s_row, s_col))
    visited = set()
    visited.add((s_row, s_col))
    levels = 0
    row_min_max = {}
    minrow = 999999999
    maxrow = -1
    while queue:
        q_len = len(queue)
        for _ in range(q_len):
            row, col = queue.popleft()
            if row in row_min_max:
                row_min_max[row] = (min(col, row_min_max[row][0]), max(col, row_min_max[row][1]))
            else:
                row_min_max[row] = (col, col)
            minrow = min(minrow, row)
            maxrow = max(maxrow, row)
            # try to move every direction
            for move in moves:
                nr = row + move[0]
                nc = col + move[1]
                if can_move(row, col, nr, nc, visited):
                    queue.append((nr,nc))
                    visited.add((nr,nc))
                    
        if queue:
            levels += 1
        else:
            break

    # so not clean but can use this to plug in what the S should be for this input
    print(f'start is at {s_row}, {s_col}')
    if (s_row - 1, s_col) in visited:
        print(f'start point goes to {s_row - 1},{s_col} which is a {input[s_row - 1][s_col]}')
    if (s_row + 1, s_col) in visited:
        print(f'start point goes to {s_row + 1},{s_col} which is a {input[s_row + 1][s_col]}')
    if (s_row, s_col - 1) in visited:
        print(f'start point goes to {s_row},{s_col - 1} which is a {input[s_row][s_col - 1]}')
    if (s_row, s_col + 1) in visited:
        print(f'start point goes to {s_row},{s_col + 1} which is a {input[s_row][s_col + 1]}')

    # return some needed info for part2 so avoid a recalc of this
    # row_min_max is a row map, entry for each row num with the lowest col and highest col number for this row
    # visited represents our pipe network
    # minrow and maxrow is so we ignore parts of the input that are outside the range of the pipe network. IE if the 
    # network starts at row 10 we don't care about row 9
    return [levels, row_min_max, visited, minrow, maxrow]

def part2(input, row_map, visited, minrow, maxrow):
    count = 0
    inside = False
    for i in range(len(input)):
        # go through the puzzle input, only process rows in scope of the network        
        if i < minrow or i > maxrow:
            continue
        for j in range(len(input[i])):            
            # go through each column in this row but if we're before the min column for this row or beyond the max, skip
            if j < row_map[i][0] or j > row_map[i][1]:
                continue
            # this is a part of the network
            if (i,j) in visited:
                # only north facing - S should not always be here though, depends if it is north facing in this input
                # so may have to remove it to get the right input.  
                # to do - dynamically decide if S is needed here
                if input[i][j] in ['|', 'L', 'J', 'S']:
                    inside = not inside
            else:
                # not part of the network, if we're inside count it
                if inside:
                    count += 1
            if i not in row_map or i == row_map[i][1]:
                inside = False

    return count

def get_from_file():
    #with open(os.getcwd() + '/solutions/day10/g3.txt') as f:
    with open(os.getcwd() + '/solutions/day10/bf.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    puzzle_input = get_from_file()
    input = parse(puzzle_input)
    part1ans = part1(input)
    part2ans = part2(input, part1ans[1], part1ans[2], part1ans[3], part1ans[4])
    print(part1ans[0])
    print(part2ans)
