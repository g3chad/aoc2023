import os 
import heapq

dir_map = { 'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0) }
turns = { 'RL': ('D', 'U'), 'UD': ('L', 'R'), 'I': ('R', 'D') }

def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split(sep='\n')]

def get_next_pos(pos, offset):
    return (pos[0] + offset[0], pos[1] + offset[1])

def get_next_pos_4_turns(pos, offset):
    return (pos[0] + 4*offset[0], pos[1] + 4*offset[1])

def inbounds(grid, pos):
    ROWS = len(grid)
    COLS = len(grid[0])
    r = pos[0]
    c = pos[1]
    if r < 0 or c < 0 or r >= ROWS or c >= COLS:
        return False
    else:
        return True

def get_neigh(grid, pos, dir, steps, min_turn=1, max_steps=3):
    neighbors = []

    if dir != 'I':
        # to keep going in our current direction
        next_pos = get_next_pos(pos, dir_map[dir])
        if inbounds(grid, next_pos) and steps + 1 <= max_steps:
            neighbors.append(((next_pos, dir, steps + 1), int(grid[next_pos[0]][next_pos[1]])))
    
    # handle turns
    turns_key = 'I'
    if dir in ('R', 'L'):
        turns_key = 'RL'
    elif dir in ('U', 'D'):
        turns_key = 'UD'
    for next_turn in turns[turns_key]:
        next_pos = get_next_pos_4_turns(pos, dir_map[next_turn]) if min_turn == 4 else get_next_pos(pos, dir_map[next_turn])
        if inbounds(grid, next_pos): 
            cost = 0           
            if min_turn == 4:
                r,c = pos
                match next_turn:
                    case 'R': cost = grid[r][c+1] + grid[r][c+2] + grid[r][c+3] + grid[r][c+4]
                    case 'L': cost = grid[r][c-1] + grid[r][c-2] + grid[r][c-3] + grid[r][c-4]
                    case 'U': cost = grid[r-1][c] + grid[r-2][c] + grid[r-3][c] + grid[r-4][c]
                    case 'D': cost = grid[r+1][c] + grid[r+2][c] + grid[r+3][c] + grid[r+4][c]
            else:
                cost = int(grid[next_pos[0]][next_pos[1]])
            neighbors.append(((next_pos, next_turn, min_turn), cost))

    return neighbors

def part1(input, min_turn = 1, max_steps = 3):
    """Implementation for part 1
        Dijkstra with a twist
    """
    grid = [[int(c) for c in row] for row in input]
    shortest = {}
    minHeap = [(0, (0,0), 'I', 0)]
    while minHeap:
        cost, pos, direction, steps = heapq.heappop(minHeap)
        if pos == (len(grid) - 1, len(grid[0]) -1):
            return cost
        path_info = (pos, direction, steps)
        if path_info in shortest:
            continue
        else:
            shortest[path_info] = cost
        for new_path_info, neigh_weight in get_neigh(grid, *path_info, min_turn, max_steps):
            if new_path_info not in shortest:
                next_pos = new_path_info[0]
                next_dir = new_path_info[1]
                next_steps = new_path_info[2]
                heapq.heappush(minHeap, (cost + neigh_weight, next_pos, next_dir, next_steps))


def part2(input):
    """Implementation for part 2"""
    return part1(input, 4, 10)

def get_from_file():
    with open(os.getcwd() + '/solutions/day17/g3.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    puzzle_input = get_from_file()
    input = parse(puzzle_input)
    part1ans = part1(input)
    part2ans = part2(input)
    print(part1ans)
    print(part2ans)
