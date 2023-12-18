import os 

def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split(sep='\n')]

def shoelace(verts):    
    vert_count = len(verts)
    sum1 = 0
    sum2 = 0
    
    for i in range(0,vert_count-1):
        sum1 = sum1 + verts[i][0] *  verts[i+1][1]
        sum2 = sum2 + verts[i][1] *  verts[i+1][0]
    
    sum1 = sum1 + verts[vert_count-1][0]*verts[0][1]   
    sum2 = sum2 + verts[0][0]*verts[vert_count-1][1]   
    
    area = abs(sum1 - sum2) / 2

    return area   

def picks(b, a):
    return (2 * a - b + 2) // 2

def part1(input):
    """Implementation for part 1
        Another polygon problem like day 10 but easier
        looking up area of polygon led me to picks theorem
        and the shoelace formula making this much easier
        than my original plan
    """
    outer_perim = 0
    vertices = []
    curr_x = 500 # aribitrary starting pt
    curr_y = 500 # aribitrary starting pt
    vertices.append((curr_x, curr_y))
    for row in input:
        positions = int(row.split(' ')[1])
        outer_perim += positions
        dir = row.split(' ')[0]
        match dir:
            case 'R':
                vertices.append([curr_x + positions, curr_y])
                curr_x = curr_x + positions
            case 'L':
                vertices.append([curr_x - positions, curr_y])
                curr_x = curr_x - positions
            case 'U':
                vertices.append([curr_x, curr_y - positions])
                curr_y = curr_y - positions
            case 'D':
                vertices.append([curr_x, curr_y + positions])
                curr_y = curr_y + positions

    area = shoelace(vertices)
    ans = outer_perim + picks(outer_perim, area)

    return ans

def get_dir(val):
    if val == '0':
        return 'R'
    elif val == '1':
        return 'D'
    elif val == '2':
        return 'L'
    else:
        return 'U'

def part2(input):
    """Implementation for part 2"""
    outer_perim = 0
    vertices = []
    curr_x = 500 # aribitrary starting pt
    curr_y = 500 # aribitrary starting pt
    vertices.append((curr_x, curr_y))
    for row in input:
        hex_dist = row.split(' ')[2].replace('(', '').replace(')', '').replace('#', '')[0:5]
        dir = get_dir(row.split(' ')[2].replace('(', '').replace(')', '').replace('#', '')[-1])
        positions = int(hex_dist, 16)
        outer_perim += positions
        match dir:
            case 'R':
                vertices.append([curr_x + positions, curr_y])
                curr_x = curr_x + positions
            case 'L':
                vertices.append([curr_x - positions, curr_y])
                curr_x = curr_x - positions
            case 'U':
                vertices.append([curr_x, curr_y - positions])
                curr_y = curr_y - positions
            case 'D':
                vertices.append([curr_x, curr_y + positions])
                curr_y = curr_y + positions

    area = shoelace(vertices)
    ans = outer_perim + picks(outer_perim, area)

    return ans

def get_from_file():
    with open(os.getcwd() + '/solutions/day18/bf.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    puzzle_input = get_from_file()
    input = parse(puzzle_input)
    part1ans = part1(input)
    part2ans = part2(input)
    print(part1ans)
    print(part2ans)
