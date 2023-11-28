from aocd import get_data
from aocd import submit
import collections

def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split(sep='\n')]

def build_stacks(input):
    """Builds stacks by stack number as represented in the input"""
    stacks = collections.defaultdict(list)
    for i in range(7, -1, -1):
        line = input[i].split(' ')
        i = 0
        stack = 1
        while i < len(line):
            if line[i] == '':
                # a blank item on this stack takes up 4 empty elements in the line array
                i += 4
            else:
                char = line[i].replace('[', '').replace(']', '')
                stacks[stack].append(char)
                i += 1
            stack += 1
    return stacks
    
def part1(input):
    """Implementation for part 1"""
    stacks = build_stacks(input)
    for move in input[10:]:
        move_parts = move.split(sep=' ')
        from_stack = int(move_parts[3])
        to_stack = int(move_parts[5])
        moves = int(move_parts[1])
        for _ in range(moves):
            pop_item = stacks[from_stack].pop()
            stacks[to_stack].append(pop_item)
    
    ans = ''
    for items in stacks.values():
        if len(items) > 0:
            ans += items.pop()
    
    return ans

    
def part2(input):
    """Implementation for part 2"""
    stacks = build_stacks(input)
    for move in input[10:]:
        move_parts = move.split(sep=' ')
        from_stack = int(move_parts[3])
        to_stack = int(move_parts[5])
        moves = int(move_parts[1])
        if moves > 1:
            queue = []
            for _ in range(moves):
                pop_item = stacks[from_stack].pop()
                queue.append(pop_item)
            while queue:
                item = queue.pop()       
                stacks[to_stack].append(item)
        else:
            pop_item = stacks[from_stack].pop()
            stacks[to_stack].append(pop_item)
    
    ans = ''
    for items in stacks.values():
        if len(items) > 0:
            ans += items.pop()
    
    return ans

if __name__ == "__main__":
    year = 2022
    day = 5
    puzzle_input = get_data(day=day, year=year)        
    input = parse(puzzle_input)
    submit(part1(input), part="a", day=day, year=year)
    submit(part2(input), part="b", day=day, year=year)