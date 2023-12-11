from aocd import get_data
from aocd import submit
import os

def parse(puzzle_input):
    """Parse input."""    
    return puzzle_input.splitlines()

def get_galaxy_info(input):
    """
        just need to know where to expand cols and rows to offset our galaxy points later
    """
    raw_galaxy_points = []
    rows_with = set()
    cols_with = set()
    rows_all = set()
    cols_all = set()
    for i in range(len(input)):
        rows_all.add(i)        
        for j in range(len(input[0])):
            cols_all.add(j)
            if input[i][j] == '#':
                rows_with.add(i)
                cols_with.add(j)
                raw_galaxy_points.append((i,j))

    missing_rows = (sorted(set(rows_all).difference(rows_with)))
    missing_cols = (sorted(set(cols_all).difference(cols_with)))
                
    return (missing_rows, missing_cols, raw_galaxy_points)

def get_distance(raw_galaxy_points, start, end, missing_rows, missing_cols, multiplier=1):
    orig_x1, orig_y1 = raw_galaxy_points[start]
    orig_x2, orig_y2 = raw_galaxy_points[end]
    missing_before_x1 = len([x for x in missing_rows if x < orig_x1])
    missing_before_y1 = len([x for x in missing_cols if x < orig_y1])
    missing_before_x2 = len([x for x in missing_rows if x < orig_x2])
    missing_before_y2 = len([x for x in missing_cols if x < orig_y2])
    new_x1 = (missing_before_x1 * multiplier) + raw_galaxy_points[start][0]
    new_y1 = (missing_before_y1 * multiplier) + raw_galaxy_points[start][1]
    new_x2 = (missing_before_x2 * multiplier) + raw_galaxy_points[end][0]
    new_y2 = (missing_before_y2 * multiplier) + raw_galaxy_points[end][1]

    return abs(new_x1 - new_x2) + abs(new_y1 - new_y2)


def part1(input, multiplier=1):
    """ Implementation for Part 1.
    """
    missing_rows, missing_cols, raw_galaxy_points = get_galaxy_info(input)
    total_pairs = 0
    sum_of_shortest_paths = 0
    for start in range(len(raw_galaxy_points)):
        for end in range(start + 1, len(raw_galaxy_points)):            
            total_pairs += 1
            distance = get_distance(raw_galaxy_points, start, end, missing_rows, missing_cols, multiplier)
            sum_of_shortest_paths += distance

    print(f'Processed {total_pairs} pairs with a sum of all shortest paths of {sum_of_shortest_paths}')

    return sum_of_shortest_paths

def part2(input):
    return part1(input, 999999)

def get_from_file():
    with open(os.getcwd() + '/solutions/day11/g3.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    year = 2023
    day = 11
    processing_g3chad = False
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
