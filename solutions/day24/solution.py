import os 
import sympy
class Hailstone():
    def __init__(self, input) -> None:
        # 331197478571816, 419588808460341, 308994415019000 @ -91, -24, -6
        self.x = int(input.split(' @ ')[0].split(', ')[0])
        self.y = int(input.split(' @ ')[0].split(', ')[1])
        self.z = int(input.split(' @ ')[0].split(', ')[2])
        self.vx = int(input.split(' @ ')[1].split(', ')[0])
        self.vy = int(input.split(' @ ')[1].split(', ')[1])
        self.vz = int(input.split(' @ ')[1].split(', ')[2])
        self.point = [self.x,self.y,self.z]
        self.velocity = [self.vx, self.vy, self.vz]

    def line_intersection(self, other_hail_stone):
        # adopted from:
        # https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
        line1 = ((self.x, self.y), (self.x + self.vx, self.y + self.vy))
        line2 = ((other_hail_stone.x, other_hail_stone.y), (other_hail_stone.x + other_hail_stone.vx, other_hail_stone.y + other_hail_stone.vy))
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            return None, None

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        if self.is_future(x) and other_hail_stone.is_future(x):
            return x,y
        return None, None
    
    def is_future(self, inter_x):
        x = self.point[0]
        vx = self.velocity[0]
        return (inter_x - x) / vx >= 0

def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split(sep='\n')]
    
def part1(input):
    """Implementation for part 1"""
    total = 0
    test_area = (7,27) if len(input) < 10 else (200000000000000, 400000000000000)
    hail_stones = [Hailstone(input[i]) for i in range(len(input))]
    for i in range(len(hail_stones) - 1):
        for j in range(i+1, len(hail_stones)):
            x,y = hail_stones[i].line_intersection(hail_stones[j])
            if x == None: continue
            else: 
                #print(f'hailstone {i} intersects hailstone {j} at {x},{y}')
                if (x >= test_area[0] and x <= test_area[1] and 
                    y >= test_area[0] and y <= test_area[1]):
                    total += 1

    return total

def part2(input):
    """Implementation for part 2"""
    hail_stones = [Hailstone(input[i]) for i in range(len(input))]
    # using sympy as a solver to solve a system of equations.
    # this came from https://youtube.com/watch?v=guOyA7Ijqgk.
    # I had no idea on this one so I took the time to
    # learn about sympy and the concepts here which make sense thx to this video!
    xr, yr,zr,vxr,vyr,vzr = sympy.symbols('xr, yr, zr, vxr, vyr, vzr')
    equations = []
    for i, hstone in enumerate(hail_stones):
        hx = hstone.x 
        hy = hstone.y
        hz = hstone.z
        vx = hstone.vx
        vy = hstone.vy
        vz = hstone.vz 
        equations.append((xr - hx) * (vy - vyr) - (yr - hy) * (vx - vxr))
        equations.append((yr - hy) * (vz - vzr) - (zr - hz) * (vy - vyr))
        if i < 2:
            continue
        answers = [sol for sol in sympy.solve(equations) if all(x % 1 == 0 for x in sol.values())]
        if len(answers) == 1:
            break
        
    return answers[0][xr] + answers[0][yr] + answers[0][zr]

def get_from_file():
    with open(os.getcwd() + '/solutions/day24/g3.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    puzzle_input = get_from_file()
    input = parse(puzzle_input)
    part1ans = part1(input)
    part2ans = part2(input)
    print(part1ans)
    print(part2ans)
